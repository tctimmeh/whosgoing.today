from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from whosgoing.models import Invitation


class InvitationView(TemplateView):
    template_name = 'whosgoing/invitation.html'

    def get_context_data(self, inviteId, **kwargs):
        invitation = get_object_or_404(Invitation, inviteId=inviteId)
        return {'invitation': invitation}

invitationView = InvitationView.as_view()
