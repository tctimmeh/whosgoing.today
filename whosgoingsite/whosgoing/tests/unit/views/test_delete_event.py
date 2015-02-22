from django.core.urlresolvers import reverse
from whosgoing.tests.unit.requiresPermission import RequiresPermission
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestDeleteEventView(WhosGoingUnitTestCase, RequiresPermission):
    def setUp(self):
        super().setUp()
        self.event = self.create_event()

    def get_url(self):
        return reverse('whosgoing:eventDelete', kwargs={'id': self.event.id})

    def add_permission(self):
        self.event.add_member(self.loggedInUser)

    def remove_permission(self):
        self.event.remove_member(self.loggedInUser)

