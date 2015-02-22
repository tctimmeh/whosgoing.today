import json
from django.core.urlresolvers import reverse
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestKickView(WhosGoingUnitTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.logInAs()
        self.kicked = self.createUser()
        self.event = self.create_event()
        self.event.add_member(self.user)
        self.event.add_member(self.kicked)
        self.post_data = {'user': self.kicked.id}

    def get_url(self, eventId=None):
        if eventId is None:
            eventId = self.event.id
        return reverse('whosgoing:event:kick', kwargs={'eventId': eventId})

    def test_returnsSuccessWithValidFormData(self):
        response = self.client.post(self.get_url(), self.post_data)
        self.assertResponseStatusIsOk(response)

    def test_returnsJsonSuccessWithValidFormData(self):
        response = self.client.post(self.get_url(), self.post_data)
        responseData = json.loads(response.content.decode())
        self.assertTrue(responseData['success'])

    def test_returnsNotFoundForBadEventId(self):
        response = self.client.post(self.get_url(99999), self.post_data)
        self.assertResponseStatusIsNotFound(response)

    def test_returnsForbiddenIfUserIsNotMemberOfEvent(self):
        self.logInAs()
        response = self.client.post(self.get_url(), self.post_data)
        self._assertResponseStatusIs(response, 403)

    def Test_returnsFailureIfUserToKickIsNotMember(self):
        self.event.remove_member(self.kicked)
        response = self.client.post(self.get_url(), self.post_data)
        responseData = json.loads(response.content.decode())
        self.assertFalse(responseData['success'])

    def test_postingWithValidDataKicksUserFromEvent(self):
        self.client.post(self.get_url(), self.post_data)
        self.assertFalse(self.event.is_member(self.kicked))
