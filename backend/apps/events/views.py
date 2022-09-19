from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import swagger
from .models import Event
from .serializers import EventSerializer, ParticipantSerializer


class ListEventsPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return super().has_permission(request, view)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


@method_decorator(name="create", decorator=swagger.create_event_schema)
@method_decorator(name="list", decorator=swagger.get_events_schema)
@method_decorator(name="update", decorator=swagger.update_event_schema)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (ListEventsPermission,)
    pagination_class = StandardResultsSetPagination
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        queryset = super().get_queryset()
        creator = self.request.query_params.get("creator")
        if creator is not None:
            queryset = queryset.filter(creator=creator)
        return queryset

    def update(self, *args, **kwargs):
        event = self.get_object()
        if event.creator_id != self.request.user.pk:
            return Response({"detail": "Cannot edit others event."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(*args, **kwargs)

    @swagger.get_participants_schema
    @action(detail=True, methods=["get"])
    def participants(self, request, *args, **kwargs):
        queryset = self.get_object().participants.select_related("user").values_list("user__username", flat=True)
        paginator = self.pagination_class()
        paginator.page_size = self.request.query_params.get("page_size") or paginator.page_size
        return paginator.get_paginated_response(paginator.paginate_queryset(queryset, request))

    @swagger.signup_for_event_schema
    @action(detail=True, methods=["post"])
    def signup_for_event(self, request, *args, **kwargs):
        data = {"event": self.get_object().pk, "user": self.request.user.pk}
        serializer = ParticipantSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger.withdraw_from_event_schema
    @action(detail=True, methods=["delete"])
    def withdraw_from_event(self, request, *args, **kwargs):
        event = self.get_object()
        if event.creator_id == self.request.user.pk:
            return Response({"detail": "Cannot withdraw from own event."}, status=status.HTTP_403_FORBIDDEN)

        participant = event.participants.filter(event_id=self.get_object().pk, user_id=self.request.user.pk)
        if not participant:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        participant.delete()
        return Response({"detail": "Deleted."}, status=status.HTTP_200_OK)
