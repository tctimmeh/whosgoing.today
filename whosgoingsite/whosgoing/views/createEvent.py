from django.views.generic import CreateView
from whosgoing.models import Event


class CreateEventView(CreateView):
    model = Event
    fields = ['name', 'description']
