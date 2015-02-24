from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from whosgoing.models import EventOccurrence


class SetAttendanceView(View):
    def post(self, request, occurrenceId, **kwargs):
        occurrence = get_object_or_404(EventOccurrence, id=occurrenceId)
        return HttpResponse('balh')


setAttendanceView = login_required(SetAttendanceView.as_view())
