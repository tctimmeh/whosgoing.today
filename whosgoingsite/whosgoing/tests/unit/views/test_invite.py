from django.core.urlresolvers import reverse
from testbase.unit import UnitTestCase
from whosgoing.models import Event


class TestInviteView(UnitTestCase):
    def setUp(self):
        self.event = Event.objects.create(name=self.randStr())
        self.inviteAddress = self.randStr() + '@host.com'

    def get_url(self, eventId=None):
        if eventId is None:
            eventId = self.event.id
        return reverse('eventInvite', kwargs={'eventId': eventId})

    def test_sendsEmailToUser(self):
        self.client.post(self.get_url(), {'user': self.inviteAddress})
        emails = self.getEmailsToRecipient(self.inviteAddress)
        self.assertEqual(len(emails), 1)

    def test_returnsNotFoundIfEventIdIsInvalid(self):
        response = self.client.post(self.get_url(9999), {'user': self.inviteAddress})
        self.assertResponseStatusIsNotFound(response)

    def test_returnsJsonSuccessResponseWithValidData(self):
        response = self.client.post(self.get_url(), {'user': self.inviteAddress})
        self.assertJSONEqual(response.content.decode(), '{"success": true}')

    def test_returnsForbiddenIfNoUserGiven(self):
        response = self.client.post(self.get_url(), {'user': ''})
        self._assertResponseStatusIs(response, 403)

    def test_rendersInviteEmailTemplate(self):
        response = self.client.post(self.get_url(), {'user': self.inviteAddress})
        self.assertTemplateUsed(response, 'whosgoing/inviteEmail.html')

