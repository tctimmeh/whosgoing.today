import datetime
from django.forms import ModelForm, TimeField
from django.forms.utils import from_current_timezone
from django.utils.translation import ugettext as _
from whosgoing.models import Event


class EventForm(ModelForm):
    time = TimeField(label=_('Default Time'), help_text=_('Time when this event normally occurs'))

    class Meta:
        model = Event
        fields = ['name', 'description']

    def clean_time(self):
        t = self.cleaned_data['time']
        dt = datetime.datetime.now()
        dt = dt.replace(hour=t.hour, minute=t.minute, second=t.second)
        dt = from_current_timezone(dt)
        return dt

    def save(self, commit=True):
        self.instance.time = self.cleaned_data['time']
        return super().save(commit)

