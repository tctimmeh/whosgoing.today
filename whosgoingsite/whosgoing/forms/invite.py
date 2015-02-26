from django.forms import ModelForm
from django.utils.translation import ugettext as _
from whosgoing.models import Invitation


class InviteForm(ModelForm):
    class Meta:
        model = Invitation
        fields = ['address', 'from_name', 'message']
        labels = {
            'address': _('User or Email Address'),
            'from_name': _('From'),
            'message': _('Invite Message')
        }
        help_texts = {
            'address': _('Email address of the user to invite'),
        }

