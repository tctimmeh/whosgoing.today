from testbase.unit import UnitTestCase
from whosgoing.models import Event, Invitation


class WhosGoingUnitTestCase(UnitTestCase):
    def assertModelInstanceExists(self, modelClass, **filterOptions):
        self.assertTrue(modelClass.objects.filter(**filterOptions).exists())

    def assertModelInstanceNotExists(self, modelClass, **filterOptions):
        self.assertFalse(modelClass.objects.filter(**filterOptions).exists())

    def create_event(self, name=None, members=()):
        if name is None:
            name = self.randStr()
        event = Event.objects.create(name=name)
        for user in members:
            event.add_member(user)
        return event

    def create_invitation(self, event=None, address=None):
        if event is None:
            event = self.create_event()
        if address is None:
            address = self.randStr() + '@host.com'
        return Invitation.objects.create(event=event, address=address)

