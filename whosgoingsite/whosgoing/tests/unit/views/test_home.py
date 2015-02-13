from testbase.unit import UnitTestCase


class TestHomeView(UnitTestCase):
    def test_rootUrlRendersHomePage(self):
        response = self.get('home')
        self.assertResponseStatusIsOk()
