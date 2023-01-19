from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse("create_user")
        self.login_url = reverse("login_user")
        self.holidays_url = reverse("holiday_create")
        self.logout_url = reverse("logout_user")

        self.user_data = {
            'emp_name': "test",
            'password': "test@123",
            'email': "test@gmail.com",
            'confirm_password': "test@123"
        }

        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")

        self.token = res.data['token']

        return super().setUp()

    def tearDown(self):

        return super().tearDown()
