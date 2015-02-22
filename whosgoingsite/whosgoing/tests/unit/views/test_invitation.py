from allauth.account.models import EmailAddress
from django.core.urlresolvers import reverse
from whosgoing.models import Invitation, EventMember
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestInvitationView(WhosGoingUnitTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.logInAs()
        self.invitation = self.create_invitation()

    def get_url(self):
        return reverse('whosgoing:invitation', kwargs={'inviteId': self.invitation.inviteId})

    def test_rendersInvitationTemplate(self):
        response = self.get()
        self.assertTemplateUsed(response, 'whosgoing/invitation.html')

    def test_pageRenderedWithInvitation(self):
        self.get()
        self.assertLastContextValueEqual('invitation', self.invitation)

    def test_indicatesInvitationForLoggedInUser(self):
        EmailAddress.objects.create(user=self.user, email=self.invitation.address)
        self.get()
        self.assertLastContextValueEqual('inviteForUser', True)

    def test_indicatesInvitationNotForLoggedInUserWithWrongEmail(self):
        EmailAddress.objects.create(user=self.user, email=self.randStr()+'@host.com')
        self.get()
        self.assertLastContextValueEqual('inviteForUser', False)

    def test_postingAsAnonymousUserReturnsForbiddenResponse(self):
        self.logOut()
        response = self.client.post(self.get_url(), {'action': 'reject'})
        self._assertResponseStatusIs(response, 403)

    def test_postingAsWrongUserReturnsForbiddenResponse(self):
        EmailAddress.objects.create(user=self.user, email=self.randStr()+'@host.com')
        response = self.client.post(self.get_url(), {'action': 'reject'})
        self._assertResponseStatusIs(response, 403)

    def test_postingRejectionDeletesInvitation(self):
        EmailAddress.objects.create(user=self.user, email=self.invitation.address)
        self.client.post(self.get_url(), {'action': 'reject'})
        self.assertRaises(Invitation.DoesNotExist, Invitation.objects.get, id=self.invitation.id)

    def test_postingRejectionRedirectsToHomePage(self):
        EmailAddress.objects.create(user=self.user, email=self.invitation.address)
        response = self.client.post(self.get_url(), {'action': 'reject'})
        self.assertRedirects(response, reverse('whosgoing:home'))

    def test_postingAcceptanceAddUserToEventMembers(self):
        EmailAddress.objects.create(user=self.user, email=self.invitation.address)
        self.client.post(self.get_url(), {'action': 'accept'})
        self.assertModelInstanceExists(EventMember, event=self.invitation.event, user=self.user)

    def test_postingAcceptanceRedirectsToEventPage(self):
        EmailAddress.objects.create(user=self.user, email=self.invitation.address)
        response = self.client.post(self.get_url(), {'action': 'accept'})
        self.assertRedirects(response, self.invitation.event.get_absolute_url())

    def test_postingWithUnknownActionArgumentReturnsForbidden(self):
        EmailAddress.objects.create(user=self.user, email=self.invitation.address)
        response = self.client.post(self.get_url(), {'action': self.randStr()})
        self._assertResponseStatusIs(response, 403)

    def test_postingAcceptanceDeletesInvitation(self):
        EmailAddress.objects.create(user=self.user, email=self.invitation.address)
        self.client.post(self.get_url(), {'action': 'accept'})
        self.assertRaises(Invitation.DoesNotExist, Invitation.objects.get, id=self.invitation.id)
