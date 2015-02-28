from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms import CharField, Form, Textarea
from django.utils.translation import ugettext as _


class InviteForm(Form):
    address = CharField(max_length=254, label=_('User or Email Address'),
                        help_text=_('User name or Email of user to invite'),
    )
    from_name = CharField(max_length=50, label=_('From'), required=False)
    message = CharField(max_length=500, required=False, widget=Textarea(attrs={'rows': 2}))

    def clean_address(self):
        value = self.cleaned_data['address']
        try:
            validate_email(value)
        except ValidationError:
            try:
                value = User.objects.get(username=value)
            except User.DoesNotExist:
                raise ValidationError('Enter a user name or valid email address')
        return value
