from django.views.generic import DetailView
from whosgoing.forms.invite import InviteForm
from whosgoing.models import Event


class EventDetailView(DetailView):
    model = Event
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['inviteForm'] = InviteForm()
        return data


eventDetailView = EventDetailView.as_view()
