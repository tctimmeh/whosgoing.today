from django.utils import timezone
from django.views.generic import DetailView
from whosgoing.forms.invite import InviteForm
from whosgoing.models import Event, EventOccurrence


class EventDetailView(DetailView):
    model = Event
    template_name = 'whosgoing/pages/event_detail.html'
    pk_url_kwarg = 'eventId'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user_is_member'] = self.object.is_member(self.request.user)
        data['inviteForm'] = InviteForm(initial={
            'from_name': ' '.join([self.request.user.first_name, self.request.user.last_name]).strip()
        })
        data['members'] = self.object.members.order_by('username')

        occurrence = self.object.next_occurrence
        if occurrence:
            data['occurrence'] = occurrence
            data['occurrenceMembers'] = occurrence.member_details_by_user

        return data


eventDetailView = EventDetailView.as_view()
