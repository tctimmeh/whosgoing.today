from allauth.account.models import EmailAddress
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestHomeView(WhosGoingUnitTestCase):
    def test_rootUrlRendersHomePage(self):
        response = self.get('whosgoing:home')
        self.assertResponseStatusIsOk()
        self.assertTemplateUsed(response, 'whosgoing/pages/home.html')

    def test_contextContainsInvitationsForAllUsersEmailAddresses(self):
        user = self.logInAs()
        email1 = self.randStr()+'@host.com'
        email2 = self.randStr()+'@host.com'
        EmailAddress.objects.create(user=user, email=email1)
        EmailAddress.objects.create(user=user, email=email2)
        event = self.create_event()
        invitation1 = self.create_invitation(event, email1)
        invitation2 = self.create_invitation(event, email2)

        self.create_invitation(event, self.randStr()+'@host.com')

        response = self.get('whosgoing:home')
        actualInvitations = response.context['invitations']
        self.assertEqual(set(actualInvitations), {invitation1, invitation2})
