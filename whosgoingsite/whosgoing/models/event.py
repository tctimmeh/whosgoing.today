from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Model, CharField, TextField, ManyToManyField
from whosgoing.models import EventMember


class Event(Model):
    name = CharField(max_length=50, verbose_name='Event Name')
    description = TextField(blank=True, default='')
    members = ManyToManyField(User, through='EventMember', related_name='events')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('eventDetail', kwargs={'id': self.id})

    def add_member(self, user):
        EventMember.objects.create(event=self, user=user)

    def is_member(self, user):
        return self.members.filter(id=user.id).exists()
