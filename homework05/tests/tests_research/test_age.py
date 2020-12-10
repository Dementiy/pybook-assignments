import datetime as dt
import unittest

import responses

from research.age import age_predict


class AgeTestCase(unittest.TestCase):
    def setUp(self):
        self.now = dt.datetime.now()
        self.year = self.now.year

    @responses.activate
    def test_age(self):
        friends = [
            {
                "id": 1,
                "first_name": "",
                "last_name": "",
                "bdate": f"01.1.{self.year-25}",
            },
            {
                "id": 2,
                "first_name": "",
                "last_name": "",
                "bdate": f"01.1.{self.year-20}",
            },
            {
                "id": 3,
                "first_name": "",
                "last_name": "",
                "bdate": f"01.1.{self.year-15}",
            },
            {"id": 4, "first_name": "", "last_name": "", "bdate": "9.8"},
            {"id": 5, "first_name": "", "last_name": ""},
        ]
        responses.add(
            responses.GET,
            "https://api.vk.com/method/friends.get",
            json={"response": {"count": len(friends), "items": friends}},
            status=200,
        )
        self.assertEqual(20.0, age_predict(user_id=123))

    @responses.activate
    def test_no_bdates(self):
        friends = [
            {"id": 1, "first_name": "", "last_name": ""},
            {"id": 2, "first_name": "", "last_name": ""},
            {"id": 3, "first_name": "", "last_name": ""},
        ]
        responses.add(
            responses.GET,
            "https://api.vk.com/method/friends.get",
            json={"response": {"count": len(friends), "items": friends}},
            status=200,
        )
        self.assertIsNone(age_predict(user_id=123))
