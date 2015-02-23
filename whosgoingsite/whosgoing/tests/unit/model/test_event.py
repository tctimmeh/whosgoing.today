import datetime
from django.utils import timezone
from whosgoing.models import EventMember, EventOccurrence
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestEventModel(WhosGoingUnitTestCase):
    def setUp(self):
        super().setUp()
        self.event = self.create_event()
        self.user = self.createUser()

    def test_addingMemberCreatesEventMembership(self):
        self.event.add_member(self.user)
        self.assertModelInstanceExists(EventMember, user=self.user, event=self.event)

    def test_addingMemberAddsToLatestOccurrence(self):
        occurrence = EventOccurrence.objects.create(event=self.event, time=timezone.now() + datetime.timedelta(hours=1))
        self.logInAs()
        self.event.add_member(self.loggedInUser)
        self.assertIn(self.loggedInUser, occurrence.members.all())

    def test_addingMemberDoesNotAddToLatestOccurrenceIfOccurrenceIsPast(self):
        occurrence = EventOccurrence.objects.create(event=self.event, time=timezone.now() - datetime.timedelta(hours=1))
        self.logInAs()
        self.event.add_member(self.loggedInUser)
        self.assertNotIn(self.loggedInUser, occurrence.members.all())

    def test_isMemberReturnsTrueIfUserIsMember(self):
        self.event.add_member(self.user)
        otherUser = self.createUser()
        self.assertTrue(self.event.is_member(self.user))
        self.assertFalse(self.event.is_member(otherUser))

    def test_removingMemberDeletesEventMembership(self):
        self.event.add_member(self.user)
        self.event.remove_member(self.user)
        self.assertModelInstanceNotExists(EventMember, user=self.user, event=self.event)

    def test_removingMemberRemovesUserFromOccurrence(self):
        self.logInAs()
        self.event.add_member(self.loggedInUser)
        occurrence = EventOccurrence.objects.create(event=self.event, time=timezone.now() + datetime.timedelta(hours=1))
        self.event.remove_member(self.loggedInUser)
        self.assertNotIn(self.loggedInUser, occurrence.members.all())

    def test_removingMemberDoesNotRemoveUserFromOccurrenceIfOccurrenceHasPast(self):
        self.logInAs()
        self.event.add_member(self.loggedInUser)
        occurrence = EventOccurrence.objects.create(event=self.event, time=timezone.now() - datetime.timedelta(hours=1))
        self.event.remove_member(self.loggedInUser)
        self.assertIn(self.loggedInUser, occurrence.members.all())

    def test_nextOccurrenceReturnsOccurrenceWithLatestTime(self):
        expected = EventOccurrence.objects.create(event=self.event, time=timezone.now()+datetime.timedelta(days=1))
        EventOccurrence.objects.create(event=self.event, time=timezone.now())
        self.assertEqual(expected, self.event.next_occurrence)

    def test_setTimeFromEventCopiesEventTimeForSameDayIfTimeIsNotYetPast(self):
        event = self.create_event()
        event.time = (timezone.now() + datetime.timedelta(hours=1)).replace(microsecond=0)
        self.assertEqual(event.time, event.next_occurrence_time.replace(microsecond=0))

    def test_setTimeFromEventCopiesEventTimeForNextDayIfTimeIsPast(self):
        event = self.create_event()
        event.time = (timezone.now() - datetime.timedelta(hours=1)).replace(microsecond=0)
        expected = event.time + datetime.timedelta(days=1)
        self.assertEqual(expected, event.next_occurrence_time.replace(microsecond=0))

