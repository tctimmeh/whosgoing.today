from django.views.generic import DetailView
from whosgoing.models import Event


class EventDetailView(DetailView):
    model = Event
    pk_url_kwarg = 'id'

eventDetailView = EventDetailView.as_view()
