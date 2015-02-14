from smtplib import SMTPException
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.generic import View
from whosgoing.forms.invite import InviteForm
from whosgoing.models import Event, Invitation


class EventInviteView(View):
    def post(self, request, eventId):
        event = get_object_or_404(Event, id=eventId)

        form = InviteForm(data=request.POST)
        if not form.is_valid():
            return JsonResponse({'success': False, 'errors': form.errors['user']})

        user = form.cleaned_data['user']

        invitation = Invitation(event=event, address=user)
        try:
            invitation.full_clean()
        except ValidationError as e:
            return JsonResponse({'success': False, 'errors': e.messages})
        invitation.save()

        template_context = {'invitation': invitation, 'site': get_current_site(request)}
        try:
            send_mail(subject=_("Are you going to %(event_name)s today?" % {'event_name': event.name}),
                      message=render_to_string('whosgoing/inviteEmailText.html', template_context),
                      from_email="<Who's Going Today?> noreply@whosgoing.today",
                      recipient_list=[user],
                      html_message=render_to_string('whosgoing/inviteEmail.html', template_context),
            )
        except SMTPException as e:
            invitation.delete()
            return JsonResponse({'success': False, 'errors': [str(e)]})

        return JsonResponse({'success': True})


eventInviteView = EventInviteView.as_view()
