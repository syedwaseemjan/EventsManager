import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.events.models import Event
from apps.events.views import EventViewSet

from .factories import EventFactory, ParticipantFactory, UserFactory


@pytest.mark.django_db
class TestEventViewSet:
    @pytest.fixture(autouse=True)
    def setup_tests(self):
        self.factory = APIRequestFactory()
        self.event = EventFactory()
        self.user = self.event.creator
        self.token = "Token {}".format(Token.objects.create(user=self.user))
        self.date = timezone.now()

        self.detail_endpoint = reverse("events:events-detail", kwargs={"version": "v1", "pk": self.event.pk})
        self.list_endpoint = reverse("events:events-list", kwargs={"version": "v1"})

    @pytest.fixture
    def user2(self):
        return UserFactory()

    @pytest.fixture
    def user2_token(self, user2):
        return "Token {}".format(Token.objects.create(user=user2))

    def get_detail_endpoint(self, participant):
        return reverse(
            "events:events-detail",
            kwargs={
                "event_pk": self.event.pk,
                "pk": participant.pk,
            },
        )

    def get_payload(self, **kwargs):
        payload = {
            "title": "Test event",
            "description": "Test event description",
            "date": self.date.isoformat(),
        }
        payload.update(kwargs)
        return payload

    def test_create_event(self):
        payload = self.get_payload()
        request = self.factory.post(self.detail_endpoint, payload, HTTP_AUTHORIZATION=self.token, format="json")
        response = EventViewSet.as_view({"post": "create"})(request)
        event = Event.objects.filter(creator_id=self.user.id).first()
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["event_id"] == str(event.id)
        assert response.data["title"] == payload["title"]
        assert response.data["description"] == payload["description"]
        assert response.data["creator"] == self.user.id
        assert response.data["creator_username"] == self.user.username
        assert response.data["date"] == payload["date"].replace("+00:00", "Z")
        assert response.data["total_participants"] == 1

    def test_update_event(self):
        payload = self.get_payload(title="Test event 2")
        request = self.factory.put(self.detail_endpoint, payload, HTTP_AUTHORIZATION=self.token, format="json")
        response = EventViewSet.as_view({"put": "update"})(request, pk=self.event.pk)
        assert response.status_code == status.HTTP_200_OK
        event = response.data
        assert event["title"] == "Test event 2"

    def test_cannot_update_other_user_event(self, user2, user2_token):
        payload = self.get_payload(title="Test event 2")
        request = self.factory.put(self.detail_endpoint, payload, HTTP_AUTHORIZATION=user2_token, format="json")
        response = EventViewSet.as_view({"put": "update"})(request, pk=self.event.pk)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "Cannot edit others event."

    def test_retrieve_event(self):
        request = self.factory.get(self.detail_endpoint, HTTP_AUTHORIZATION=self.token, format="json")
        response = EventViewSet.as_view({"get": "retrieve"})(request, pk=self.event.pk)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["event_id"] == str(self.event.pk)
        assert response.data["creator"] == self.user.id
        assert response.data["creator_username"] == self.user.username
        assert response.data["total_participants"] == 1

    def test_list_events(self):
        request = self.factory.get(self.list_endpoint)
        response = EventViewSet.as_view({"get": "list"})(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["event_id"] == str(self.event.pk)
        assert response.data["results"][0]["title"] == str(self.event.title)
        assert response.data["results"][0]["description"] == str(self.event.description)

    def test_list_participants(self, user2):
        ParticipantFactory(user=user2, event=self.event)
        request = self.factory.get(self.list_endpoint)
        response = EventViewSet.as_view({"get": "participants"})(request, pk=self.event.pk)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_signup_as_event_participant(self, user2, user2_token):
        request = self.factory.post(self.detail_endpoint, HTTP_AUTHORIZATION=user2_token, format="json")
        response = EventViewSet.as_view({"post": "signup_for_event"})(request, pk=self.event.pk)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["event"] == self.event.id
        assert response.data["user"] == user2.id

    def test__multiple_signups_for_same_event_should_fail(self):
        request = self.factory.post(self.detail_endpoint, HTTP_AUTHORIZATION=self.token, format="json")
        force_authenticate(request, user=self.user)
        response = EventViewSet.as_view({"post": "signup_for_event"})(request, pk=self.event.pk)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        errors = response.data["errors"]
        assert errors["non_field_errors"][0]["message"] == "The fields event, user must make a unique set."
        assert len(errors) == 1

    def test_withdraw_from_event(self, user2, user2_token):
        ParticipantFactory(user=user2, event=self.event)
        request = self.factory.delete(self.detail_endpoint, HTTP_AUTHORIZATION=user2_token, format="json")
        response = EventViewSet.as_view({"delete": "withdraw_from_event"})(request, pk=self.event.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "Deleted."

    def test_creator_cannot_withdraw_from_his_own_event(self):
        participant = self.event.participants.first()
        assert participant.user == self.event.creator
        request = self.factory.delete(self.detail_endpoint, HTTP_AUTHORIZATION=self.token, format="json")
        response = EventViewSet.as_view({"delete": "withdraw_from_event"})(request, pk=self.event.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "Cannot withdraw from own event."
