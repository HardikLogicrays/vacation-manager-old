from .test_setup import TestSetUp


class TestViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)

        self.assertEqual(res.status_code, 400)

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")

        self.token = res.data['token']

        self.assertEqual(res.status_code, 200)

    def test_holidays(self):

        holiday_data = {
            "title": "title 1",
            "start_date": "2023-02-18",
            "end_date": "2023-02-20"
        }

        create_holiday = self.client.post(path=self.holidays_url, data=holiday_data, HTTP_AUTHORIZATION=f"Token {self.token}",
                                          format="json")

        self.assertEqual(create_holiday.status_code, 200)

        get_all_holidays = self.client.get(path=self.holidays_url, HTTP_AUTHORIZATION=f"Token {self.token}",
                                           format="json")

        self.assertEqual(get_all_holidays.status_code, 200)

        self.params = {
            'start_date': '2023-02-18',
            'end_date': '2023-02-20'
        }

        get_filter_holidays = self.client.get(data=self.params, path=self.holidays_url, HTTP_AUTHORIZATION=f"Token {self.token}",
                                              format="json")

        self.assertEqual(get_filter_holidays.status_code, 200)

    def test_user_logout(self):
        res = self.client.post(
            self.logout_url, HTTP_AUTHORIZATION=f"Token {self.token}", format="json")

        self.assertEqual(res.status_code, 200)
