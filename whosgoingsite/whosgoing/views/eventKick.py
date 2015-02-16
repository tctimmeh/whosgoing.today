from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import View
from whosgoing.forms.kick import KickForm
from whosgoing.models import Event


class KickError(Exception):
    def __init__(self, errors):
        self.errors = errors


class EventKickView(View):
    def post(self, request, eventId, **kwargs):
        event = get_object_or_404(Event, id=eventId)
        if not event.is_member(self.request.user):
            return HttpResponseForbidden()

        try:
            form = KickForm(event=event, data=self.request.POST)
            if not form.is_valid():
                raise KickError(form.errors['user'])
            user = form.cleaned_data['user']
            event.remove_member(user)
        except KickError as e:
            return JsonResponse({'success': False, 'errors': e.errors})

        return JsonResponse({'success': True})


eventKickView = EventKickView.as_view()
