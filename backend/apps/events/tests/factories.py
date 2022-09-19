import factory
from django.contrib.auth.models import User

from apps.events.models import Event, Participant


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    # Generating random name to avoid collisions.
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    creator = factory.SubFactory(UserFactory)
    title = factory.Faker("pystr")
    description = factory.Faker("pystr")
    date = factory.Faker("date_object")

    @factory.post_generation
    def participant(self, create, *args, **kwargs):
        if not create:
            return
        self.participants.create(user=self.creator)


class ParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Participant
        django_get_or_create = ("event", "user")

    event = factory.SubFactory(EventFactory)
    user = factory.SubFactory(UserFactory)
