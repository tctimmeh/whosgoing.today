from allauth.account.models import EmailAddress
from django.core.urlresolvers import reverse
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestToggleNotifyAddressView(WhosGoingUnitTestCase):
    def setUp(self):
        super().setUp()
        self.logInAs()
        self.emailAddress = EmailAddress.objects.create(user=self.loggedInUser, email=self.loggedInUser.email)
        self.event = self.create_event()
        self.event.add_member(self.loggedInUser)
        self.post_data = {'address': self.emailAddress.email}

    def get_url(self, eventId=None):
        if eventId is None:
            eventId = self.event.id
        return reverse('whosgoing:event:toggleNotifyAddress', kwargs={'eventId': eventId})

    def test_returnsNotFoundForInvalidEventId(self):
        response = self.client.post(self.get_url(99999), self.post_data)
        self.assertResponseStatusIsNotFound(response)

    def test_returnsForbiddenIfUserIsNotMemberOfEvent(self):
        self.event.remove_member(self.loggedInUser)
        response = self.client.post(self.get_url(), self.post_data)
        self._assertResponseStatusIs(response, 403)

    def test_returnsForbiddenIfNoAddressGiven(self):
        del self.post_data['address']
        response = self.client.post(self.get_url(), self.post_data)
        self._assertResponseStatusIs(response, 403)

    def test_returnsForbiddenIfAddressIsInvalid(self):
        self.post_data['address'] = self.randStr() + '@host.com'
        response = self.client.post(self.get_url(), self.post_data)
        self._assertResponseStatusIs(response, 403)

    def test_returnsForbiddenIfAddressDoesNotBelongToUser(self):
        otherUser = self.createUser()
        EmailAddress.objects.create(user=otherUser, email=otherUser.email)
        self.post_data['address'] = otherUser.email
        response = self.client.post(self.get_url(), self.post_data)
        self._assertResponseStatusIs(response, 403)

    def test_returnsOkIfAddressDiffersOnlyByCase(self):
        self.post_data['address'] = self.post_data['address'].upper()
        response = self.client.post(self.get_url(), self.post_data)
        self.assertResponseStatusIsOk(response)

    def test_returnsOkIfAllInputsValid(self):
        response = self.client.post(self.get_url(), self.post_data)
        self.assertResponseStatusIsOk(response)

    def test_addAddressToNotifyListIfNotPresent(self):
        self.client.post(self.get_url(), self.post_data)
        self.assertIn(self.emailAddress, self.event.notify_addresses.all())

    def test_removesAddressFromNotifyListIfAlreadyPresent(self):
        self.event.notify_addresses.add(self.emailAddress)
        self.client.post(self.get_url(), self.post_data)
        self.assertNotIn(self.emailAddress, self.event.notify_addresses.all())

