from django.core.urlresolvers import reverse
from whosgoing.tests.unit.views.api.apiUnitTestMixin import ApiUnitTestMixin
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestEventDetailApiView(ApiUnitTestMixin, WhosGoingUnitTestCase):
    def setUp(self):
        super().setUp()
        self.logInAs()
        self.event = self.create_event(members=[self.loggedInUser])

    def get_url(self):
        return reverse('whosgoing:api:event-detail', kwargs={'pk': self.event.pk})
