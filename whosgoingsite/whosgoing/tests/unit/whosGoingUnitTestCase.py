from testbase.unit import UnitTestCase
from whosgoing.models import Event, Invitation


class WhosGoingUnitTestCase(UnitTestCase):
    def assertModelInstanceExists(self, modelClass, **filterOptions):
        self.assertTrue(modelClass.objects.filter(**filterOptions).exists())

    def create_event(self, name=None):
        if name is None:
            name = self.randStr()
        return Event.objects.create(name=name)

    def create_invitation(self, event=None, address=None):
        if event is None:
            event = self.create_event()
        if address is None:
            address = self.randStr() + '@host.com'
        return Invitation.objects.create(event=event, address=address)
