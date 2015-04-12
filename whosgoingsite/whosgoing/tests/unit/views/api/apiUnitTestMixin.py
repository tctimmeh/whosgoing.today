import json


class ApiUnitTestMixin(object):
    def setUp(self):
        super().setUp()
        self.logInAs()

    def postJson(self, data):
        url = self.get_url()
        return self.client.post(url, data = {
            '_content_type': 'application/json',
            '_content': json.dumps(data),
        })

    def test_getReturnsSuccess(self):
        self.get()
        self.assertResponseStatusIsOk()

    def test_returnsForbiddenForAnonymousUser(self):
        self.logOut()
        self.get()
        self._assertResponseStatusIs(self._response, 403)
