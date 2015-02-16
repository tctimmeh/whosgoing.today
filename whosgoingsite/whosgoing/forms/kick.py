from django.contrib.auth.models import User
from django.forms import Form, ModelChoiceField


class KickForm(Form):
    user = ModelChoiceField(queryset=User.objects.all())

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = event.members.all()
