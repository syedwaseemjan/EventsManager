import pytest

from .factories import EventFactory


@pytest.mark.django_db
class TestEvent:
    def test_str(self):
        event = EventFactory()
        assert event.title in str(event)


@pytest.mark.django_db
class TestParticipant:
    def test_str(self):
        event = EventFactory()
        participant = event.participants.first()
        assert str(participant) == f"{participant.event} - {participant.user}"
