from django.core.urlresolvers import reverse
from whosgoing.models import EventOccurrence
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestSetAttendanceView(WhosGoingUnitTestCase):
    def setUp(self):
        super().setUp()
        self.logInAs()
        self.event = self.create_event()
        self.event.add_member(self.loggedInUser)
        self.occurrence = EventOccurrence.objects.create(event=self.event)

    def get_url(self, occurrenceId=None):
        if occurrenceId is None:
            occurrenceId = self.occurrence.id
        return reverse('whosgoing:setAttendance', kwargs={'occurrenceId': occurrenceId})

    def test_returnsNotFoundForInvalidOccurrenceId(self):
        response = self.client.post(self.get_url(occurrenceId=9999))
        self.assertResponseStatusIsNotFound(response)
