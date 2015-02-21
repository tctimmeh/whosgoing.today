import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Model, CharField, TextField, ManyToManyField, DateTimeField
from django.utils.timezone import get_current_timezone
from django.utils.translation import ugettext as _
from whosgoing.models import EventMember


def default_event_time():
    t = datetime.datetime.now(get_current_timezone())
    return t.replace(hour=12, minute=0, second=0)


class Event(Model):
    name = CharField(max_length=50, verbose_name=_('Event Name'))
    description = TextField(blank=True, default='')
    members = ManyToManyField(User, through='EventMember', related_name='events')
    time = DateTimeField(
        verbose_name=_('Default Time'),
        default=default_event_time,
        help_text=_('Time when this event normally occurs')
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('eventDetail', kwargs={'id': self.id})

    def add_member(self, user):
        EventMember.objects.create(event=self, user=user)

    def remove_member(self, user):
        try:
            EventMember.objects.get(event=self, user=user).delete()
        except EventMember.DoesNotExist:
            pass

    def is_member(self, user):
        return self.members.filter(id=user.id).exists()
