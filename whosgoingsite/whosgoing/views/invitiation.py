from allauth.account.models import EmailAddress
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from whosgoing.models import Invitation


class InvitationView(DetailView):
    model = Invitation
    slug_url_kwarg = 'inviteId'
    slug_field = 'inviteId'
    template_name = 'whosgoing/invitation.html'
    context_object_name = 'invitation'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['inviteForUser'] = self._is_invite_for_user()
        return data

    def post(self, request, inviteId, **kwargs):
        self.object = self.get_object()
        if not self._is_invite_for_user():
            return HttpResponseForbidden()

        action = request.POST['action']
        if action == 'reject':
            self.object.delete()

        return HttpResponseRedirect(reverse('home'))

    def _is_invite_for_user(self):
        if self.request.user is None:
            return False

        userEmails = EmailAddress.objects.filter(user__id=self.request.user.id, email=self.object.address)
        return len(userEmails) > 0


invitationView = InvitationView.as_view()
