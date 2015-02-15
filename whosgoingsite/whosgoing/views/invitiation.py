from allauth.account.models import EmailAddress
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from whosgoing.models import Invitation


class InvitationView(TemplateView):
    template_name = 'whosgoing/invitation.html'

    def get_context_data(self, inviteId, **kwargs):
        data = {}

        invitation = get_object_or_404(Invitation, inviteId=inviteId)
        data['invitation'] = invitation

        if self.request.user is not None:
            userEmails = EmailAddress.objects.filter(user__id=self.request.user.id, email=invitation.address)
            data['inviteForUser'] = len(userEmails) > 0

        return data

invitationView = InvitationView.as_view()
