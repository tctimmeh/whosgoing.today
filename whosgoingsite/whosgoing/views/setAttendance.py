from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from whosgoing.models import EventOccurrence, OccurrenceMember, Attendance


class SetAttendanceView(View):
    def get(self, request, occurrenceId, **kwargs):
        self.occurrenceId = occurrenceId
        return self._set_attendance(request.GET.get('attend'))

    def post(self, request, occurrenceId, **kwargs):
        self.occurrenceId = occurrenceId
        return self._set_attendance(request.POST.get('attendance'), request.POST.get('next'))

    def _set_attendance(self, attendance=None, next=None):
        if attendance is None:
            raise PermissionDenied()

        occurrence = get_object_or_404(EventOccurrence, id=self.occurrenceId)
        if not occurrence.event.is_member(self.request.user):
            raise PermissionDenied()
        if occurrence.is_past:
            raise PermissionDenied()

        try:
            attendance = Attendance.from_string(attendance)
        except ValueError:
            raise PermissionDenied()

        try:
            member = OccurrenceMember.objects.get(occurrence=occurrence, user=self.request.user)
        except OccurrenceMember.DoesNotExist:
            raise PermissionDenied()
        member.attendance = attendance
        member.save()

        if next is None:
            next = reverse('whosgoing:event:detail', kwargs={'eventId': occurrence.event.id})
        return HttpResponseRedirect(next)


setAttendanceView = login_required(SetAttendanceView.as_view())
