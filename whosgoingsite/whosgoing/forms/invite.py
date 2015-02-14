from django import forms


class InviteForm(forms.Form):
    user = forms.CharField(min_length=1)

