from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from whosgoing.models import Event


class CreateOccurrenceView(View):
    def post(self, request, eventId, **kwargs):
        event = get_object_or_404(Event, id=eventId)
        if not event.is_member(request.user):
            raise PermissionDenied()

        nextOccurrence = event.next_occurrence
        if nextOccurrence and not nextOccurrence.is_past:
            return HttpResponseRedirect(reverse('whosgoing:eventDetail', kwargs={'id': eventId}))

        event.occurrences.create(time=event.next_occurrence_time)

        return HttpResponseRedirect(reverse('whosgoing:eventDetail', kwargs={'id': eventId}))


createOccurrenceView = login_required(CreateOccurrenceView.as_view())
