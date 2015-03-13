from dcbase.views.generic.popupFormView import PopupFormMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView
from whosgoing.models import Invitation


class DeleteInvitationView(PopupFormMixin, DeleteView):
    model = Invitation
    slug_url_kwarg = 'inviteId'
    slug_field = 'inviteId'
    template_name = "whosgoing/fragments/cancel_invitation.html"
    submit_text = _('Cancel Invite')
    submit_style = 'danger'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, _('Invitation cancelled successfully'))
        return self.popup_form_valid()

    def get_object(self, queryset=None):
        invitation = super().get_object(queryset)
        if not invitation.event.is_member(self.request.user):
            raise PermissionDenied()
        return invitation


deleteInvitationView = login_required(DeleteInvitationView.as_view())
