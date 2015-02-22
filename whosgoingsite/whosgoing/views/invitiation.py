from allauth.account.models import EmailAddress
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils.translation import ugettext as _
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
            return HttpResponseRedirect(reverse('whosgoing:home'))
        elif action == 'accept':
            self.object.delete()
            self.object.event.add_member(self.request.user)
            messages.success(request, _('Successfully joined event "%(event_name)s".') % {'event_name': self.object.event.name})
            return HttpResponseRedirect(reverse('whosgoing:eventDetail', kwargs={'id': self.object.event.id}))
        else:
            return HttpResponseForbidden()

    def _is_invite_for_user(self):
        if self.request.user is None:
            return False

        userEmails = EmailAddress.objects.filter(user__id=self.request.user.id, email=self.object.address)
        return len(userEmails) > 0


invitationView = InvitationView.as_view()
