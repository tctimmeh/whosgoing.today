from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView
from whosgoing.models import Invitation


class DeleteInvitationView(DeleteView):
    model = Invitation
    slug_url_kwarg = 'inviteId'
    slug_field = 'inviteId'
    template_name = "whosgoing/pages/delete_form.html"

    def get_object(self, queryset=None):
        invitation = super().get_object(queryset)
        if not invitation.event.is_member(self.request.user):
            raise PermissionDenied()
        return invitation

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Invitation to {} for {}'.format(self.object.event.name, self.object.masked_address)
        data['extra_text'] = _('The user will not be able to join this event without a new invitation from an existing event member.')
        return data

    def get_success_url(self):
        return self.object.event.get_absolute_url()

deleteInvitationView = login_required(DeleteInvitationView.as_view())
