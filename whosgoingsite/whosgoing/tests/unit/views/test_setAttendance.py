from datetime import timedelta
from django.core.urlresolvers import reverse
from django.utils import timezone
from whosgoing.models import EventOccurrence, Attendance
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestSetAttendanceView(WhosGoingUnitTestCase):
    def setUp(self):
        super().setUp()
        self.logInAs()
        self.event = self.create_event()
        self.event.add_member(self.loggedInUser)
        self.occurrence = EventOccurrence.objects.create(event=self.event, time=timezone.now() + timedelta(hours=1))
        self.post_data = {'attendance': 'Accept', 'next': reverse('whosgoing:home')}

    def get_url(self, occurrenceId=None, queryArg=None):
        if occurrenceId is None:
            occurrenceId = self.occurrence.id

        url = reverse('whosgoing:occurrence:setAttendance', kwargs={'occurrenceId': occurrenceId})

        if queryArg is not None:
            url = '{}?attend={}'.format(url, queryArg)

        return url

    def test_returnsNotFoundForInvalidOccurrenceId(self):
        response = self.client.post(self.get_url(occurrenceId=9999), self.post_data)
        self.assertResponseStatusIsNotFound(response)

    def test_successfulPostRedirectsToNextUrl(self):
        response = self.client.post(self.get_url(), self.post_data)
        self.assertRedirects(response, self.post_data['next'])

    def test_returnsForbiddenIfUserIsNotMember(self):
        self.event.remove_member(self.loggedInUser)
        response = self.client.post(self.get_url(), self.post_data)
        self._assertResponseStatusIs(response, 403)

    def test_returnsForbiddenIfOccurenceIsPast(self):
        self.occurrence.time = timezone.now() - timedelta(hours=1)
        self.occurrence.save()
        response = self.client.post(self.get_url(), self.post_data)
        self._assertResponseStatusIs(response, 403)

    def test_successfulPostSetsMemberAttendance(self):
        self.client.post(self.get_url(), self.post_data)
        attendance = self.occurrence.get_member_attendance(self.loggedInUser)
        self.assertEqual(self.post_data['attendance'], attendance.name)

    def test_getWithNoQueryArgReturnsForbidden(self):
        response = self.get()
        self._assertResponseStatusIs(response, 403)

    def test_getReturnsForbiddenIfQueryArgIsInvalid(self):
        response = self.client.get(self.get_url(queryArg=self.randStr()))
        self._assertResponseStatusIs(response, 403)

    def test_getSetsAttendanceAsIndicatedByQueryArg(self):
        response = self.client.get(self.get_url(queryArg='accept'))
        self.assertEqual(Attendance.ACCEPT, self.occurrence.get_member_attendance(self.loggedInUser).id)

    def test_getRedirectsToEventDetailPage(self):
        response = self.client.get(self.get_url(queryArg='regret'))
        self.assertRedirects(response, reverse('whosgoing:event:detail', kwargs={'eventId': self.event.id}))
