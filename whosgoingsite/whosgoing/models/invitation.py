import uuid

from django.core.urlresolvers import reverse
from django.db.models import Model, DateTimeField, ForeignKey, EmailField, CharField, Manager, TextField
from django.utils import timezone


class InvitationManager(Manager):
    def for_user(self, user):
        emails = [record.email for record in user.emailaddress_set.only('email')]
        return self.filter(address__in=emails)

class Invitation(Model):
    event = ForeignKey('Event')
    inviteId = CharField(max_length=36, default=uuid.uuid4)
    sent = DateTimeField(auto_now_add=True)
    address = EmailField(max_length=254)
    from_name = CharField(max_length=50, blank=True)
    message = TextField(blank=True)

    objects = InvitationManager()

    def __str__(self):
        return 'Invitation to {} for {}'.format(self.event.name, self.address)

    def get_absolute_url(self):
        return reverse('invitation', kwargs={'inviteId': self.inviteId})

    @property
    def event_name(self):
        return self.event.name

    @property
    def since_last_sent(self):
        return timezone.now() - self.sent

