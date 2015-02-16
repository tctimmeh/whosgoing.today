from whosgoing.models import EventMember
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestEventModel(WhosGoingUnitTestCase):
    def test_addingMemberCreatesEventMembership(self):
        user = self.createUser()
        event = self.create_event()
        event.add_member(user)
        self.assertModelInstanceExists(EventMember, user=user, event=event)
