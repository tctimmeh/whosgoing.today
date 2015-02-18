import json
from django.core.urlresolvers import reverse
from testbase.unit import UnitTestCase
from whosgoing.models import Event, Invitation


class TestInviteView(UnitTestCase):
    def setUp(self):
        super().setUp()
        user = self.logInAs()
        self.event = Event.objects.create(name=self.randStr())
        self.event.add_member(user)
        self.inviteAddress = self.randStr() + '@host.com'

    def get_url(self, eventId=None):
        if eventId is None:
            eventId = self.event.id
        return reverse('eventInvite', kwargs={'eventId': eventId})

    def test_sendsEmailToUser(self):
        self.client.post(self.get_url(), {'address': self.inviteAddress})
        emails = self.getEmailsToRecipient(self.inviteAddress)
        self.assertEqual(len(emails), 1)

    def test_returnsNotFoundIfEventIdIsInvalid(self):
        response = self.client.post(self.get_url(9999), {'address': self.inviteAddress})
        self.assertResponseStatusIsNotFound(response)

    def test_returnsJsonSuccessResponseWithValidData(self):
        response = self.client.post(self.get_url(), {'address': self.inviteAddress})
        self.assertJSONEqual(response.content.decode(), '{"success": true}')

    def test_rendersInviteEmailTemplate(self):
        response = self.client.post(self.get_url(), {'address': self.inviteAddress})
        self.assertTemplateUsed(response, 'whosgoing/inviteEmail.html')

    def test_createsInvitation(self):
        response = self.client.post(self.get_url(), {'address': self.inviteAddress})
        invitation = Invitation.objects.get(event=self.event, address=self.inviteAddress)
        self.assertIsNotNone(invitation)

    def test_responseIndicatesFailureIfEmailAddressIsInvalid(self):
        response = self.client.post(self.get_url(), {'address': self.randStr()})
        responseData = json.loads(response.content.decode())
        self.assertFalse(responseData['success'])

    def test_responseIndicatesFailureIfPostDataInvalid(self):
        response = self.client.post(self.get_url(), {'address': ''})
        responseData = json.loads(response.content.decode())
        self.assertFalse(responseData['success'])

    def test_returnsFailureMessageIfDuplicateInvitationSentTooSoon(self):
        self.client.post(self.get_url(), {'address': self.inviteAddress})
        response = self.client.post(self.get_url(), {'address': self.inviteAddress})
        responseData = json.loads(response.content.decode())
        self.assertFalse(responseData['success'])

    def test_postingAsUserWhoIsNotMembersReturnsForbidden(self):
        user = self.logInAs()
        response = self.client.post(self.get_url(), {'address': self.inviteAddress})
        self._assertResponseStatusIs(response, 403)
