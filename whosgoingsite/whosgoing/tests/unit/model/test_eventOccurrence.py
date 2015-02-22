from datetime import timedelta

from django.utils import timezone
from whosgoing.models import EventOccurrence
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestEventOccurrence(WhosGoingUnitTestCase):
    def test_isPastReturnsTrueIfOccurrenceTimeIsBeforeNow(self):
        event = self.create_event()
        occurrence = EventOccurrence.objects.create(event=event, time=timezone.now()-timedelta(days=1))
        self.assertTrue(occurrence.is_past)

    def test_isPastReturnsFalseIfOccurrenceTimeIsAfterNow(self):
        event = self.create_event()
        occurrence = EventOccurrence.objects.create(event=event, time=timezone.now()+timedelta(days=1))
        self.assertFalse(occurrence.is_past)

