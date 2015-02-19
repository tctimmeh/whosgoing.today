from smtplib import SMTPException
import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import View
from whosgoing.forms.invite import InviteForm
from whosgoing.models import Event, Invitation


class InviteError(RuntimeError):
    pass


class EventInviteView(View):
    MAX_INVITE_FREQUENCY = datetime.timedelta(hours=1)

    def post(self, request, eventId):
        self.event = get_object_or_404(Event, id=eventId)
        if not self.event.is_member(self.request.user):
            return HttpResponseForbidden()

        message = None
        form = InviteForm(request.POST)
        try:
            if form.is_valid():
                self.address = form.cleaned_data['address']
                self.from_name = form.cleaned_data['from_name']
                self.message = form.cleaned_data['message']

                invitation = self._get_invitation()
                self._send_email(invitation)

                message = _('Successfully sent invite to %(recipient)s!') % {'recipient': self.address}
                form = InviteForm(initial={'from_name': self.from_name, 'message': self.message})
        except InviteError as e:
            form.add_error(None, str(e))

        return render(self.request, 'whosgoing/invite_form.html', {'event': self.event, 'form': form, 'message': message})

    def _get_invitation(self):
        existing_invitations = Invitation.objects.filter(event=self.event, address=self.address)
        if not existing_invitations:
            invitation = Invitation.objects.create(event=self.event, address=self.address, from_name=self.from_name, message=self.message)
        else:
            invitation = existing_invitations[0]
            if invitation.since_last_sent < EventInviteView.MAX_INVITE_FREQUENCY:
                raise InviteError(_('Please wait before sending another invitation to this address'))
            else:
                invitation.sent = timezone.now()
                invitation.from_name = self.from_name
                invitation.message = self.message
                invitation.save()
        return invitation

    def _send_email(self, invitation):
        template_context = {'invitation': invitation, 'site': get_current_site(self.request)}
        try:
            send_mail(subject=_("[Who's Going Today?] You've been invited to %(event_name)s!") % {'event_name': invitation.event.name},
                      message=render_to_string('whosgoing/inviteEmailText.html', template_context),
                      from_email="Who's Going Today? <noreply@whosgoing.today>",
                      recipient_list=[invitation.address],
                      html_message=render_to_string('whosgoing/inviteEmail.html', template_context),
            )
        except SMTPException as e:
            invitation.delete()
            raise InviteError([str(e)])


eventInviteView = EventInviteView.as_view()
