from django.core.urlresolvers import reverse
from django.db.models import Model, CharField, TextField


class Event(Model):
    name = CharField(max_length=50, verbose_name='Event Name')
    description = TextField(blank=True, default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('eventDetail', kwargs={'id': self.id})

