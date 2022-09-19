from django.db import transaction
from django.utils import timezone
from django.utils.encoding import force_str
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.utils.serializer_helpers import ReturnDict

from .models import Event, Participant


class SerializerErrorMessagesMixin:
    """
    A serializer mixin which formats the `serializer.ValidationError` message
    according to friendly format.
    """

    @property
    def errors(self):
        ugly_errors = super(SerializerErrorMessagesMixin, self).errors
        pretty_errors = self.build_pretty_errors(ugly_errors)
        return ReturnDict(pretty_errors, serializer=self)

    def to_string(self, msg):
        msg = force_str(msg)
        if isinstance(msg, ErrorDetail):
            msg = str(msg)
        return msg

    def get_error_details(self, data, default_code="invalid"):
        message = self.to_string(data)
        code = getattr(data, "code", default_code)
        return {"message": message, "code": code}

    def resolve_errors(self, errors):
        pretty = {}
        for error_type in errors:
            field_errors = errors[error_type]
            pretty[error_type] = [self.get_error_details(error) for error in field_errors]
        return pretty

    def build_pretty_errors(self, errors):
        pretty = self.resolve_errors(errors)
        if pretty:
            return {"errors": pretty}
        return {}


class EventSerializer(SerializerErrorMessagesMixin, serializers.ModelSerializer):
    event_id = serializers.UUIDField(format="hex_verbose", source="id", read_only=True)
    total_participants = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ["event_id", "title", "description", "date", "creator", "total_participants"]

    def __init__(self, *args, **kwargs):
        super(EventSerializer, self).__init__(*args, **kwargs)
        self.user = self.context["request"].user
        if "data" in kwargs:
            kwargs["data"]["creator"] = self.user.pk

    def validate_date(self, event_date):
        if event_date and event_date.date() < timezone.now().date():
            raise RestValidationError("Provided date has already passed, please select a date in future.")

        query = Event.objects.filter(creator=self.user, date=event_date)
        if self.instance:
            query = query.exclude(id=self.instance.pk)

        query = query.count()
        if query:
            raise RestValidationError(f"You already have another event on date: {event_date}.")

        return event_date

    @transaction.atomic
    def create(self, validated_data):
        event = super(EventSerializer, self).create(validated_data)
        event.participants.create(user=self.user)
        return event


class ParticipantSerializer(SerializerErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ("event", "user")
