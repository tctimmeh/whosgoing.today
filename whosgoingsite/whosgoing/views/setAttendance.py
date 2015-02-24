from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from whosgoing.models import EventOccurrence, OccurrenceMember, Attendance


class SetAttendanceView(View):
    def post(self, request, occurrenceId, **kwargs):
        occurrence = get_object_or_404(EventOccurrence, id=occurrenceId)
        if not occurrence.event.is_member(request.user):
            raise PermissionDenied()
        if occurrence.is_past:
            raise PermissionDenied()

        try:
            member = OccurrenceMember.objects.get(occurrence=occurrence, user=request.user)
        except OccurrenceMember.DoesNotExist:
            raise PermissionDenied()

        member.attendance = Attendance.from_string(request.POST['attendance'])
        member.save()

        return HttpResponseRedirect(request.POST['next'])


setAttendanceView = login_required(SetAttendanceView.as_view())
