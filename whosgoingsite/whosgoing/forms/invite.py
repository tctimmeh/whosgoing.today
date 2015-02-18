from django.forms import ModelForm
from whosgoing.models import Invitation


class InviteForm(ModelForm):
    class Meta:
        model = Invitation
        fields = ['address', 'from_name', 'message']

