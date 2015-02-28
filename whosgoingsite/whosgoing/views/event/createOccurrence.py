from smtplib import SMTPException
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.generic import View
from whosgoing.models import Event


class CreateOccurrenceView(View):
    def post(self, request, eventId, **kwargs):
        self.event = get_object_or_404(Event, id=eventId)
        if not self.event.is_member(request.user):
            raise PermissionDenied()

        nextOccurrence = self.event.next_occurrence
        if nextOccurrence and not nextOccurrence.is_past:
            return HttpResponseRedirect(self.event.get_absolute_url())

        self.occurrence = self.event.occurrences.create(time=self.event.next_occurrence_time)

        self.send_notifications()

        return HttpResponseRedirect(self.event.get_absolute_url())

    def send_notifications(self):
        notifyAddresses = self.event.notify_addresses.values('email')
        notifyAddresses = [entry['email'] for entry in notifyAddresses]
        template_context = {
            'occurrence': self.occurrence,
            'site': get_current_site(self.request),
        }

        try:
            send_mail(subject=_("[Who's Going Today?] New occurrence of %(event_name)s!") % {'event_name': self.event.name},
                      message=render_to_string('whosgoing/mail/new_occurrence.txt', template_context),
                      from_email="Who's Going Today? <noreply@whosgoing.today>",
                      recipient_list=notifyAddresses,
                      html_message=render_to_string('whosgoing/mail/new_occurrence.html', template_context),
            )
        except SMTPException as e:
            messages.error(self.request, _('The occurrence was created but an error was encountered sending notification emails.'))


createOccurrenceView = login_required(CreateOccurrenceView.as_view())
