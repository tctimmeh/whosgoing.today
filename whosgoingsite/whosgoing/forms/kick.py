from django.contrib.auth.models import User
from django.forms import Form, ModelChoiceField, HiddenInput


class KickForm(Form):
    kick_user = ModelChoiceField(queryset=User.objects.all(), widget=HiddenInput())

    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kick_user'].queryset = instance.members.all()
