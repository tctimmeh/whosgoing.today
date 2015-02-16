from whosgoing.models import EventMember
from whosgoing.tests.unit.whosGoingUnitTestCase import WhosGoingUnitTestCase


class TestEventModel(WhosGoingUnitTestCase):
    def test_addingMemberCreatesEventMembership(self):
        event = self.create_event()
        user = self.createUser()
        event.add_member(user)
        self.assertModelInstanceExists(EventMember, user=user, event=event)

    def test_isMemberReturnsTrueIfUserIsMember(self):
        event = self.create_event()
        user = self.createUser()
        event.add_member(user)
        otherUser = self.createUser()
        self.assertTrue(event.is_member(user))
        self.assertFalse(event.is_member(otherUser))
