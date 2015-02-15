from allauth.account.models import EmailAddress
from django.core.urlresolvers import reverse
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

