from django.core.urlresolvers import reverse
from testbase.unit import UnitTestCase
from testbase.unit.views import RequiresLogin
from whosgoing.models import Event


class TestCreateEventView(UnitTestCase, RequiresLogin):
    def setUp(self):
        super().setUp()
        self.user = self.logInAs()
        self.url = self.get_url()
        self.eventName = self.randStr()
        self.postData = {'name': self.eventName, 'time': '12:34 pm'}

    def get_url(self):
        return reverse('whosgoing:createEvent')

    def test_postRedirectsToLoginIfUserNotLoggedIn(self):
        self.logOut()
        response = self.client.post(self.url, self.postData)
        self.assertRedirects(response, reverse('account_login') + '?next={}'.format(self.url))

    def test_postWithValidFormDataCreatesNewEvent(self):
        self.client.post(self.url, self.postData)
        event = Event.objects.get(name=self.eventName)
        self.assertIsNotNone(event)

    def test_postWithValidFormDataRedirectsToEventDetailPage(self):
        response = self.client.post(self.url, self.postData)
        event = Event.objects.get(name=self.eventName)
        self.assertRedirects(response, event.get_absolute_url())

    def test_eventCreatorIsMemberOfEvent(self):
        self.client.post(self.url, self.postData)
        event = Event.objects.get(name=self.eventName)
        members = event.members.all()
        self.assertIn(self.user, members)
