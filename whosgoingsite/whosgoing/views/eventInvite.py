from smtplib import SMTPException
import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import View
from whosgoing.forms.invite import InviteForm
from whosgoing.models import Event, Invitation


class InviteError(Exception):
    def __init__(self, errors):
        self.errors = errors


class EventInviteView(View):
    MAX_INVITE_FREQUENCY = datetime.timedelta(hours=1)

    def post(self, request, eventId):
        event = get_object_or_404(Event, id=eventId)
        if not event.is_member(self.request.user):
            return HttpResponseForbidden()

        try:
            address = self._get_address_from_form(request.POST)
            invitation = self._get_invitation(event, address)
            self._send_email(invitation)
        except InviteError as e:
            return JsonResponse({'success': False, 'errors': e.errors})

        return JsonResponse({'success': True})

    def _get_address_from_form(self, formData):
        form = InviteForm(data=formData)
        if not form.is_valid():
            raise InviteError(form.errors['user'])
        user = form.cleaned_data['user']
        return user

    def _get_invitation(self, event, address):
        existing_invitations = Invitation.objects.filter(event=event, address=address)
        if not existing_invitations:
            invitation = self._create_invitation(event, address)
        else:
            invitation = existing_invitations[0]
            if invitation.since_last_sent < EventInviteView.MAX_INVITE_FREQUENCY:
                raise InviteError(['Please wait before sending another invitation to this address'])
            else:
                invitation.sent = timezone.now()
                invitation.save()
        return invitation

    def _create_invitation(self, event, address):
        invitation = Invitation(event=event, address=address)
        try:
            invitation.full_clean()
        except ValidationError as e:
            raise InviteError(e.messages)
        invitation.save()
        return invitation

    def _send_email(self, invitation):
        template_context = {'invitation': invitation, 'site': get_current_site(self.request)}
        try:
            send_mail(subject=_("Are you going to %(event_name)s today?" % {'event_name': invitation.event.name}),
                      message=render_to_string('whosgoing/inviteEmailText.html', template_context),
                      from_email="<Who's Going Today?> noreply@whosgoing.today",
                      recipient_list=[invitation.address],
                      html_message=render_to_string('whosgoing/inviteEmail.html', template_context),
            )
        except SMTPException as e:
            invitation.delete()
            raise InviteError([str(e)])


eventInviteView = EventInviteView.as_view()
