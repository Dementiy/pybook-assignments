import unittest
from unittest.mock import patch
import datetime as dt

from age import age_predict


class TestAgePredict(unittest.TestCase):

    def test_friends_with_bdate_field(self):
        today = dt.date.today()
        yesterday = dt.date(day=today.day-1, month=today.month, year=1996).strftime('%d.%m.%Y')
        tomorrow = dt.date(day=today.day+1, month=today.month, year=1992).strftime('%d.%m.%Y')
        response = [
            {'id': 1, 'first_name': '', 'last_name': '', 'bdate': yesterday, 'online': 0},
            {'id': 2, 'first_name': '', 'last_name': '', 'bdate': tomorrow, 'online': 0},
            {'id': 3, 'first_name': '', 'last_name': '', 'bdate': '11.11', 'online': 0},
            {'id': 4, 'first_name': '', 'last_name': '', 'online': 0},
        ]
        with patch('age.get_friends', return_value=response):
            predicted_age = age_predict(user_id=1)
            self.assertEqual(predicted_age, 23.5)

    def test_friends_without_bdate_field(self):
        response = [
            {'id': 1, 'first_name': '', 'last_name': '', 'online': 0},
            {'id': 2, 'first_name': '', 'last_name': '', 'online': 0},
        ]
        with patch('age.get_friends', return_value=response):
            predicted_age = age_predict(user_id=1)
            self.assertEqual(predicted_age, None)

    def test_friends_with_incomplete_bdate_field(self):
        response = [
            {'id': 1, 'first_name': '', 'last_name': '', 'bdate': '15.1', 'online': 0},
            {'id': 2, 'first_name': '', 'last_name': '', 'bdate': '3.9', 'online': 0},
        ]
        with patch('age.get_friends', return_value=response):
            predicted_age = age_predict(user_id=1)
            self.assertEqual(predicted_age, None)

    def test_empty_response(self):
        response = []
        with patch('age.get_friends', return_value=response):
            predicted_age = age_predict(user_id=1)
            self.assertEqual(predicted_age, None)

