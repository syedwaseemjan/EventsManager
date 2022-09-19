import datetime
from unittest.mock import Mock

import pytest
from django.utils import timezone

from apps.events.models import Event, Participant
from apps.events.serializers import EventSerializer, ParticipantSerializer

from .factories import EventFactory, UserFactory


@pytest.mark.django_db
class TestEventSerializer:
    def get_payload(self, **kwargs):
        payload = {
            "title": "Test event",
            "description": "Test event description",
            "date": timezone.now().isoformat(),
        }
        payload.update(kwargs)
        return payload

    def get_context(self):
        return {"request": Mock(user=UserFactory())}

    def test_create_event(self):
        payload = self.get_payload()
        serializer = EventSerializer(data=payload, context=self.get_context())
        assert serializer.is_valid()
        event = serializer.save()

        assert Event.objects.exists() is True
        assert event.title == payload["title"]
        assert event.description == payload["description"]
        assert event.date.isoformat() == payload["date"]
        assert event.participants.count() == 1

    def test_event_creation_fails_for_past_date(self):
        payload = self.get_payload(date=(timezone.now() - datetime.timedelta(days=1)))
        serializer = EventSerializer(data=payload, context=self.get_context())
        assert serializer.is_valid() is False
        errors = serializer.errors["errors"]
        assert errors["date"][0]["message"] == "Provided date has already passed, please select a date in future."
        assert str(errors["date"][0]["code"]) == "invalid"

    def test_event_creation_fails_for_same_datetime_by_same_user(self):
        datetime = timezone.now()
        payload = self.get_payload(date=datetime.isoformat())
        context = self.get_context()
        serializer = EventSerializer(data=payload, context=context)
        assert serializer.is_valid()
        serializer.save()

        payload = self.get_payload(date=datetime.isoformat())
        serializer = EventSerializer(data=payload, context=context)
        assert serializer.is_valid() is False
        errors = serializer.errors["errors"]
        assert set(errors.keys()) == {"date"}
        assert errors["date"][0]["message"] == f"You already have another event on date: {datetime}."
        assert str(errors["date"][0]["code"]) == "invalid"


@pytest.mark.django_db
class TestParticipantSerializer:
    def test_create_participant(self):
        user = UserFactory()
        event = EventFactory()
        serializer = ParticipantSerializer(data={"event": event.id, "user": user.id})
        assert serializer.is_valid()
        participant = serializer.save()

        assert Participant.objects.count() == 2
        assert participant.event_id == event.id
        assert participant.user_id == user.id
        assert event.participants.count() == 2
