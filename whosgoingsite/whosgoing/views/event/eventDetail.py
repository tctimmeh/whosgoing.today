from django.views.generic import DetailView
from whosgoing.forms.invite import InviteForm
from whosgoing.models import Event


class EventDetailView(DetailView):
    model = Event
    template_name = 'whosgoing/pages/event_detail.html'
    pk_url_kwarg = 'eventId'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        userIsMember = self.object.is_member(self.request.user)

        data['members'] = self.object.members.order_by('username')
        data['user_is_member'] = userIsMember

        if userIsMember:
            data['inviteForm'] = InviteForm(initial={
                'from_name': ' '.join([self.request.user.first_name, self.request.user.last_name]).strip()
            })
            data['notifyAddresses'] = self.object.get_notify_addresses_for_user(self.request.user)

        occurrence = self.object.next_occurrence
        if occurrence:
            data['occurrence'] = occurrence
            data['occurrenceMembers'] = occurrence.member_details_by_user
            if userIsMember:
                data['userAttendance'] = occurrence.get_member_attendance(self.request.user)

        return data


eventDetailView = EventDetailView.as_view()
