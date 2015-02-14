from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import View
from whosgoing.models import Event


class EventInviteView(View):
    def post(self, request, eventId):
        event = get_object_or_404(Event, id=eventId)

        user = request.POST['user']
        if not user:
            return HttpResponseForbidden()

        send_mail("Who's Going Today? Are you?",
                  render_to_string('whosgoing/inviteEmail.html', {'event': event}),
                  "<Who's Going Today?> admin@whosgoing.today",
                  [user]
        )
        return JsonResponse({'success': True})


eventInviteView = EventInviteView.as_view()
