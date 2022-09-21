import uuid

from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Event(BaseModel):

    title = models.CharField(max_length=120)
    description = models.TextField()
    date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def total_participants(self):
        return self.participants.count()

    @property
    def creator_username(self):
        return self.creator.username

    def is_participant(self, user):
        return self.participants.filter(user_id=user.id).exists()

    class Meta:
        default_related_name = "events"
        ordering = ("date",)

    def __str__(self):
        return f"{self.title} - {self.date} - {self.creator}"


class Participant(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="going_to")

    class Meta:
        default_related_name = "participants"
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.event} - {self.user}"
