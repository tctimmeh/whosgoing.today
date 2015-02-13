from django.core.urlresolvers import reverse
from testbase.unit import UnitTestCase
from testbase.unit.views import RequiresLogin
from whosgoing.models import Event


class TestCreateEventView(UnitTestCase, RequiresLogin):
    def setUp(self):
        super().setUp()
        user = self.createUser()
        self.logInAs(user)
        self.url = self.get_url()

    def get_url(self):
        return reverse('createEvent')

    def test_postRedirectsToLoginIfUserNotLoggedIn(self):
        self.logOut()
        response = self.client.post(self.url, data={'name': self.randStr()})
        self.assertRedirects(response, reverse('account_login') + '?next={}'.format(self.url))

    def test_postWithValidFormDataCreatesNewEvent(self):
        eventName = self.randStr()
        self.client.post(self.url, data={'name': eventName})
        event = Event.objects.get(name=eventName)
        self.assertIsNotNone(event)

    def test_postWithValidFormDataRedirectsToEventDetailPage(self):
        eventName = self.randStr()
        response = self.client.post(self.url, data={'name': eventName})
        event = Event.objects.get(name=eventName)
        self.assertRedirects(response, reverse('eventDetail', kwargs={'id': event.id}))

