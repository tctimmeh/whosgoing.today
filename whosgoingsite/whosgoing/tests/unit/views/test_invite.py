import json
from django.core.urlresolvers import reverse
from testbase.unit import UnitTestCase
from whosgoing.models import Event, Invitation


class TestInviteView(UnitTestCase):
    def setUp(self):
        super().setUp()
        self.logInAs()
        self.event = Event.objects.create(name=self.randStr())
        self.event.add_member(self.loggedInUser)
        self.inviteAddress = self.randStr() + '@host.com'
        self.inviteAddress = self.inviteAddress.lower()
        self.post_data = {'address': self.inviteAddress, 'from_name': self.randStr(), 'message': self.randStr()}

    def get_url(self, eventId=None):
        if eventId is None:
            eventId = self.event.id
        return reverse('whosgoing:event:invite', kwargs={'eventId': eventId})

    def test_sendsEmailToUser(self):
        self.client.post(self.get_url(), self.post_data)
        emails = self.getEmailsToRecipient(self.inviteAddress)
        self.assertEqual(len(emails), 1)

    def test_returnsNotFoundIfEventIdIsInvalid(self):
        response = self.client.post(self.get_url(9999), self.post_data)
        self.assertResponseStatusIsNotFound(response)

    def test_rendersInviteEmailTemplate(self):
        response = self.client.post(self.get_url(), self.post_data)
        self.assertTemplateUsed(response, 'whosgoing/mail/invite.html')
        self.assertTemplateUsed(response, 'whosgoing/mail/invite.txt')

    def test_createsInvitationWithPostedData(self):
        self.client.post(self.get_url(), self.post_data)
        invitation = Invitation.objects.get(event=self.event, address=self.inviteAddress)
        self.assertEqual(self.post_data['address'], invitation.address)
        self.assertEqual(self.post_data['from_name'], invitation.from_name)
        self.assertEqual(self.post_data['message'], invitation.message)

    def test_createsInvitationWithAddressFromUserName(self):
        self.post_data['address'] = self.loggedInUser.username
        self.client.post(self.get_url(), self.post_data)
        Invitation.objects.get(event=self.event, address__iexact=self.loggedInUser.email)

    def test_postingAsUserWhoIsNotMembersReturnsForbidden(self):
        self.logInAs()
        response = self.client.post(self.get_url(), self.post_data)
        self._assertResponseStatusIs(response, 403)
