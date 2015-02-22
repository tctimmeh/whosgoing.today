from datetime import timedelta
from django.core.urlresolvers import reverse
from django.utils import timezone
from whosgoing.models import EventOccurrence
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestCreateOccurrenceView(WhosGoingUnitTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.logInAs()
        self.event = self.create_event()
        self.event.add_member(self.user)
        self.eventDetailUrl = reverse('whosgoing:eventDetail', kwargs={'id': self.event.id})

    def get_url(self, eventId=None):
        if eventId is None:
            eventId = self.event.id
        return reverse('whosgoing:createOccurrence', kwargs={'eventId': eventId})

    def test_returnsNotFoundForInvalidEventId(self):
        response = self.client.post(self.get_url(9999))
        self.assertResponseStatusIsNotFound(response)

    def test_returnsForbiddenIfUserIsNotEventMember(self):
        self.event.remove_member(self.user)
        response = self.client.post(self.get_url())
        self._assertResponseStatusIs(response, 403)

    def test_createsNoOccurrenceIfNextOccurrenceIsInFuture(self):
        EventOccurrence.objects.create(event=self.event, time=timezone.now()+timedelta(hours=2))
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.eventDetailUrl)
        self.assertEqual(1, len(EventOccurrence.objects.all()))

    def test_createsOccurrenceWithEventTimeIfNextOccurrenceIsInPast(self):
        EventOccurrence.objects.create(event=self.event, time=timezone.now()-timedelta(hours=2))
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.eventDetailUrl)
        self.assertEqual(2, len(EventOccurrence.objects.all()))

