import uuid
from django.core.urlresolvers import reverse
from django.db.models import Model, DateTimeField, ForeignKey, EmailField, CharField


class EmailInvitation(Model):
    event = ForeignKey('Event')
    inviteId = CharField(max_length=36, default=uuid.uuid4)
    sent = DateTimeField(auto_now_add=True)
    address = EmailField(max_length=254)

    def __str__(self):
        return 'Invitation to {} for {}'.format(self.event.name, self.address)

    def get_absolute_url(self):
        return reverse('invitation', kwargs={'inviteId': self.inviteId})
