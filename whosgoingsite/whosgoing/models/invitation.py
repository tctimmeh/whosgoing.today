import uuid
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
import re

from django.core.urlresolvers import reverse
from django.db.models import Model, DateTimeField, ForeignKey, EmailField, CharField, Manager, TextField
from django.db.models.signals import pre_save
from django.utils import timezone
from django.dispatch import receiver


class InvitationManager(Manager):
    def for_user(self, user):
        if user.is_anonymous():
            return None
        emails = [record.email for record in user.emailaddress_set.only('email')]
        emails = [email.lower() for email in emails]
        return self.filter(address__in=emails)


class Invitation(Model):
    event = ForeignKey('Event', related_name='invitations')
    inviteId = CharField(max_length=36, default=uuid.uuid4)
    sent = DateTimeField(auto_now_add=True)
    sent_by = ForeignKey(User, default=1)
    address = EmailField(max_length=254)
    from_name = CharField(max_length=50, blank=True)
    message = TextField(blank=True)

    objects = InvitationManager()

    def __str__(self):
        return 'Invitation to {} for {}'.format(self.event.name, self.address)

    def get_absolute_url(self):
        return reverse('whosgoing:invitation', kwargs={'inviteId': self.inviteId})

    @property
    def event_name(self):
        return self.event.name

    @property
    def since_last_sent(self):
        return timezone.now() - self.sent

    @property
    def masked_address(self):
        if not hasattr(Invitation, 'rxMaskedEmail'):
            Invitation.rxMaskedEmail = re.compile(r'''(.{1,3}).*@(.{1,3}).*\.(.*)$''')
        return self.rxMaskedEmail.sub(r'''\1*****.\2*****.\3''', self.address)

    @property
    def invited_user(self):
        try:
            email = EmailAddress.objects.get(email__iexact=self.address)
        except EmailAddress.DoesNotExist:
            return None
        return email.user


@receiver(pre_save, sender=Invitation)
def invitation_pre_save(sender, instance, raw, using, update_fields, **kwargs):
    if raw:
        return
    instance.address = instance.address.lower()