from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, DateTimeField


class EventMember(Model):
    user = ForeignKey(User)
    event = ForeignKey('Event')

    class Meta:
        unique_together = ('user', 'event')
