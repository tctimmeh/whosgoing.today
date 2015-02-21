from django.core.urlresolvers import reverse


class RequiresPermission(object):
    def test_getRedirectsToLoginIfUserNotLoggedIn(self):
        self.logOut()
        url = self.get_url()
        response = self.client.get(url)
        self.assertRedirects(response, reverse('account_login') + '?next={}'.format(url))

    def test_returnsForbiddenIfUserDoesNotHavePermission(self):
        self.logInAs()
        response = self.get()
        self._assertResponseStatusIs(response, 403)

    def test_returnsOkIfUserHasPermission(self):
        if not self.loggedInUser:
            self.logInAs()
        self.add_permission()
        self.get()
        self.assertResponseStatusIsOk()

    def test_returnsForbiddenIfPermissionRemoved(self):
        if not self.loggedInUser:
            self.logInAs()
        self.add_permission()
        self.remove_permission()
        response = self.get()
        self._assertResponseStatusIs(response, 403)

