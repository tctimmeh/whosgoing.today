from django.views.generic import TemplateView


class InvitationView(TemplateView):
    template_name = 'whosgoing/invitation.html'

invitationView = InvitationView.as_view()
