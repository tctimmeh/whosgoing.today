import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Model, CharField, TextField, ManyToManyField, DateTimeField
from django.utils.timezone import get_current_timezone
from django.utils.translation import ugettext as _
from django.utils import timezone
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
        return reverse('whosgoing:event:detail', kwargs={'eventId': self.id})

    def add_member(self, user):
        EventMember.objects.create(event=self, user=user)
        occurrence = self.next_occurrence
        if occurrence and not occurrence.is_past:
            occurrence.add_member(user)

    def remove_member(self, user):
        try:
            EventMember.objects.get(event=self, user=user).delete()
        except EventMember.DoesNotExist:
            pass

        occurrence = self.next_occurrence
        if occurrence and not occurrence.is_past:
            occurrence.remove_member(user)

    def is_member(self, user):
        return self.members.filter(id=user.id).exists()

    @property
    def next_occurrence(self):
        from whosgoing.models import EventOccurrence
        try:
            return self.occurrences.order_by('time').reverse()[0:1].get()
        except EventOccurrence.DoesNotExist:
            return None

    @property
    def next_occurrence_time(self):
        now = timezone.now()
        next_time = now.replace(hour=self.time.hour, minute=self.time.minute, second=self.time.second)
        if next_time < now:
            next_time += datetime.timedelta(days=1)
        return next_time
