from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from whosgoing.models import Event


class CreateEventView(CreateView):
    model = Event
    fields = ['name', 'description']

createEventView = login_required(CreateEventView.as_view())
