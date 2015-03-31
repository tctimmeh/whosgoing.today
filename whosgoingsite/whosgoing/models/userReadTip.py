from django.db.models import Model, ForeignKey
from zinnia.models import Entry


class UserReadTip(Model):
    user = ForeignKey('auth.User')
    entry = ForeignKey(Entry)

    def __str__(self):
        return '{} read {}'.format(self.user, self.entry)
