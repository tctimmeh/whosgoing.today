from datetime import timedelta

from allauth.account.models import EmailAddress
from django.core import mail
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
        EventOccurrence.objects.create(event=self.event, time=timezone.now() + timedelta(hours=2))
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.event.get_absolute_url())
        self.assertEqual(1, len(EventOccurrence.objects.all()))

    def test_createsOccurrenceWithEventTimeIfNextOccurrenceIsInPast(self):
        EventOccurrence.objects.create(event=self.event, time=timezone.now() - timedelta(hours=2))
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.event.get_absolute_url())
        self.assertEqual(2, len(EventOccurrence.objects.all()))

    def getEmailsToRecipient(self, address):
        return [email for email in mail.outbox if address in email.to or address in email.cc or address in email.bcc]

    def test_sendsEmailToAllNotifyAddressesExceptOccurrenceCreator(self):
        email1 = EmailAddress.objects.create(user=self.loggedInUser, email=self.loggedInUser.email)
        otherEmail1 = EmailAddress.objects.create(user=self.loggedInUser, email=self.randStr() + '@host.com')

        otherUser = self.createUser()
        email2 = EmailAddress.objects.create(user=otherUser, email=otherUser.email)

        thirdUser = self.createUser()
        email3 = EmailAddress.objects.create(user=thirdUser, email=thirdUser.email)

        self.event.notify_addresses.add(email1)
        self.event.notify_addresses.add(otherEmail1)
        self.event.notify_addresses.add(email2)
        self.event.notify_addresses.add(email3)

        response = self.client.post(self.get_url())
        self.assertEqual(0, len(self.getEmailsToRecipient(email1.email)))
        self.assertEqual(0, len(self.getEmailsToRecipient(otherEmail1.email)))
        self.assertEqual(1, len(self.getEmailsToRecipient(email2.email)))
        self.assertEqual(1, len(self.getEmailsToRecipient(email3.email)))
        self.assertTemplateUsed(response, 'whosgoing/mail/new_occurrence.txt')
        self.assertTemplateUsed(response, 'whosgoing/mail/new_occurrence.html')
