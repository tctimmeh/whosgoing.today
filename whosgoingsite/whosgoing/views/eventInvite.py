from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.generic import View
from whosgoing.forms.invite import InviteForm
from whosgoing.models import Event, EmailInvitation


class EventInviteView(View):
    def post(self, request, eventId):
        event = get_object_or_404(Event, id=eventId)

        form = InviteForm(data=request.POST)
        if not form.is_valid():
            return JsonResponse({'success': False, 'errors': form.errors['user']})

        user = form.cleaned_data['user']

        invitation = EmailInvitation(event=event, address=user)
        try:
            invitation.full_clean()
        except ValidationError as e:
            return JsonResponse({'success': False, 'errors': e.messages})
        invitation.save()

        send_mail(_("Are you going to %(event_name)s today?" % {'event_name': event.name}),
                  render_to_string('whosgoing/inviteEmail.html', {'event': event}),
                  "<Who's Going Today?> admin@whosgoing.today",
                  [user]
        )

        return JsonResponse({'success': True})


eventInviteView = EventInviteView.as_view()
