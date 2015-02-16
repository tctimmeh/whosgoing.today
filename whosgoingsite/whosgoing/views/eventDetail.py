from django.views.generic import DetailView
from whosgoing.forms.invite import InviteForm
from whosgoing.models import Event


class EventDetailView(DetailView):
    model = Event
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.object.is_member(self.request.user):
            data['inviteForm'] = InviteForm()
        data['members'] = self.object.members.order_by('username')
        return data


eventDetailView = EventDetailView.as_view()
