import json
from django.core.urlresolvers import reverse
from whosgoing.models import Event
from whosgoing.tests.unit.views.api.apiUnitTestCase import ApiUnitTestCase


class TestEventListApiView(ApiUnitTestCase):
    def get_url(self):
        return reverse('whosgoing:api:event-list')

    def test_getReturnsListOfUsersEvents(self):
        event1 = self.create_event(name='a', members=[self.loggedInUser])
        event2 = self.create_event(name='b', members=[self.loggedInUser])
        otherEvent = self.create_event()

        response = self.get()
        data = json.loads(response.content.decode())
        self.assertEqual(2, data['count'])
        self.assertEqual(event1.id, data['results'][0]['id'])
        self.assertEqual(event1.name, data['results'][0]['name'])

        self.assertEqual(event2.id, data['results'][1]['id'])
        self.assertEqual(event2.name, data['results'][1]['name'])

    def test_postCreatesEventWithUserAsMember(self):
        name = self.randStr()
        self.postJson({'name': name})
        event = Event.objects.get(name=name)
        self.assertTrue(event.is_member(self.loggedInUser))
