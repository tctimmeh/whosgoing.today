from datetime import timedelta
from allauth.account.models import EmailAddress
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

    def get_url(self, eventId=None):
        if eventId is None:
            eventId = self.event.id
        return reverse('whosgoing:event:createOccurrence', kwargs={'eventId': eventId})

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
        self.assertRedirects(response, self.event.get_absolute_url())
        self.assertEqual(1, len(EventOccurrence.objects.all()))

    def test_createsOccurrenceWithEventTimeIfNextOccurrenceIsInPast(self):
        EventOccurrence.objects.create(event=self.event, time=timezone.now()-timedelta(hours=2))
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.event.get_absolute_url())
        self.assertEqual(2, len(EventOccurrence.objects.all()))

    def test_sendsEmailToAllNotifyAddresses(self):
        email1 = EmailAddress.objects.create(user=self.loggedInUser, email=self.loggedInUser.email)

        otherUser = self.createUser()
        email2 = EmailAddress.objects.create(user=otherUser, email=otherUser.email)

        self.event.notify_addresses.add(email1)
        self.event.notify_addresses.add(email2)

        response = self.client.post(self.get_url())
        self.assertEqual(1, len(self.getEmailsToRecipient(email1.email)))
        self.assertEqual(1, len(self.getEmailsToRecipient(email2.email)))
        self.assertTemplateUsed(response, 'whosgoing/mail/new_occurrence.txt')
        self.assertTemplateUsed(response, 'whosgoing/mail/new_occurrence.html')
