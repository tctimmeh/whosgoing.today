from django.forms import ModelForm, SplitDateTimeWidget, SplitDateTimeField
from whosgoing.models import EventOccurrence


class OccurrenceForm(ModelForm):
    time = SplitDateTimeField(input_time_formats=['%I:%M %p'],
                              widget=SplitDateTimeWidget(attrs={'class': 'split-date-time'})
    )

    class Meta:
        model = EventOccurrence
        fields = ['time']
        labels = {
            'time': 'Occurrence Time',
        }
