from datetime import timedelta

from django.utils import timezone
from whosgoing.models import EventOccurrence
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestEventOccurrence(WhosGoingUnitTestCase):
    def setUp(self):
        super().setUp()
        self.logInAs()
        self.event = self.create_event()
        self.event.add_member(self.loggedInUser)

    def test_isPastReturnsTrueIfOccurrenceTimeIsBeforeNow(self):
        occurrence = EventOccurrence.objects.create(event=self.event, time=timezone.now()-timedelta(days=1))
        self.assertTrue(occurrence.is_past)

    def test_isPastReturnsFalseIfOccurrenceTimeIsAfterNow(self):
        occurrence = EventOccurrence.objects.create(event=self.event, time=timezone.now()+timedelta(days=1))
        self.assertFalse(occurrence.is_past)

    def test_creationAddsEventMembers(self):
        occurrence = EventOccurrence.objects.create(event=self.event)
        self.assertIn(self.loggedInUser, occurrence.members.all())
