class RequiresPermission(object):
    def test_returnsForbiddenIfUserDoesNotHavePermission(self):
        self.logOut()
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


