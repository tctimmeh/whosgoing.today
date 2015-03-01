from django.core.urlresolvers import reverse
from testbase.unit.views import RequiresLogin
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestDeleteInvitationView(WhosGoingUnitTestCase, RequiresLogin):
    def setUp(self):
        super().setUp()
        self.logInAs()
        self.invitation = self.create_invitation()
        self.event = self.invitation.event
        self.event.add_member(self.loggedInUser)

    def get_url(self, inviteId=None):
        if inviteId is None:
            inviteId = self.invitation.inviteId
        return reverse('whosgoing:deleteInvitation', kwargs={'inviteId': inviteId})

    def test_postReturnsForbiddenIfUserIsNotMemberOfEvent(self):
        self.event.remove_member(self.loggedInUser)
        response = self.client.post(self.get_url())
        self._assertResponseStatusIs(response, 403)

    def test_returnsNotFoundForBadInviteId(self):
        response = self.client.get(self.get_url(inviteId=self.randStr(36)))
        self.assertResponseStatusIsNotFound(response)

    def test_deletesInvitation(self):
        self.client.post(self.get_url())
        self.assertEqual(0, self.event.invitations.count())

    def test_redirectsToEventPage(self):
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.event.get_absolute_url())
