from django.db.models import Model, CharField, TextField


class Event(Model):
    name = CharField(max_length=50, verbose_name='Event Name')
    description = TextField(blank=True, default='')

