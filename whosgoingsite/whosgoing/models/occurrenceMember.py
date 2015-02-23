from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey
from whosgoing.models import Attendance


class OccurrenceMember(Model):
    user = ForeignKey(User)
    occurrence = ForeignKey('EventOccurrence')
    attendence = ForeignKey(Attendance, default=Attendance.UNDECIDED)

    class Meta:
        unique_together = ('user', 'occurrence')
