from allauth.account.models import EmailAddress
from django.core.urlresolvers import reverse
from whosgoing.models import Invitation
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestInvitationView(WhosGoingUnitTestCase):
    def setUp(self):
        super().setUp()
        self.invitation = self.create_invitation()

    def get_url(self):
        return reverse('invitation', kwargs={'inviteId': self.invitation.inviteId})

    def test_rendersInvitationTemplate(self):
        response = self.get()
        self.assertTemplateUsed(response, 'whosgoing/invitation.html')

    def test_pageRenderedWithInvitation(self):
        self.get()
        self.assertLastContextValueEqual('invitation', self.invitation)

    def test_indicatesInvitationForLoggedInUser(self):
        user = self.logInAs()
        EmailAddress.objects.create(user=user, email=self.invitation.address)
        self.get()
        self.assertLastContextValueEqual('inviteForUser', True)

    def test_indicatesInvitationNotForLoggedInUserWithWrongEmail(self):
        user = self.logInAs()
        EmailAddress.objects.create(user=user, email=self.randStr()+'@host.com')
        self.get()
        self.assertLastContextValueEqual('inviteForUser', False)

    def test_postingAsAnonymousUserReturnsForbiddenResponse(self):
        response = self.client.post(self.get_url(), {'action': 'reject'})
        self._assertResponseStatusIs(response, 403)

    def test_postingAsWrongUserReturnsForbiddenResponse(self):
        user = self.logInAs()
        EmailAddress.objects.create(user=user, email=self.randStr()+'@host.com')
        response = self.client.post(self.get_url(), {'action': 'reject'})
        self._assertResponseStatusIs(response, 403)

    def test_postingRejectionDeletesInvitation(self):
        user = self.logInAs()
        EmailAddress.objects.create(user=user, email=self.invitation.address)
        self.client.post(self.get_url(), {'action': 'reject'})
        self.assertRaises(Invitation.DoesNotExist, Invitation.objects.get, id=self.invitation.id)

    def test_postingRejectionRedirectsToHomePage(self):
        user = self.logInAs()
        EmailAddress.objects.create(user=user, email=self.invitation.address)
        response = self.client.post(self.get_url(), {'action': 'reject'})
        self.assertRedirects(response, reverse('home'))
