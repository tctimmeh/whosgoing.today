from django.utils import timezone
from django.views.generic import DetailView
from whosgoing.forms.invite import InviteForm
from whosgoing.models import Event, EventOccurrence


class EventDetailView(DetailView):
    model = Event
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user_is_member'] = self.object.is_member(self.request.user)
        data['inviteForm'] = InviteForm(initial={
            'from_name': ' '.join([self.request.user.first_name, self.request.user.last_name]).strip()
        })
        data['members'] = self.object.members.order_by('username')
        data['occurrence'] = self.object.next_occurrence

        return data


eventDetailView = EventDetailView.as_view()
