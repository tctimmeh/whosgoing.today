from django.db.models import Model, ForeignKey, DateTimeField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from whosgoing.models import Event


class EventOccurrence(Model):
    event = ForeignKey(Event, related_name='occurrences')
    time = DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} occurrence at {}'.format(self.event.name, self.time)

