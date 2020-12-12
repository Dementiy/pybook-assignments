import time
import unittest
from unittest.mock import patch
from urllib.parse import unquote

import pandas as pd
import responses

from vkapi.wall import get_wall_execute


class GetWallTestCase(unittest.TestCase):
    @responses.activate
    def test_total_count(self):
        expected_items = [
            {
                "id": 1,
                "from_id": 1234,
                "owner_id": 1234,
                "date": 1234567890,
                "text": "some message",
            }
        ]
        responses.add(
            responses.POST,
            "https://api.vk.com/method/execute",
            json={
                "response": {
                    "count": 1,
                    "items": expected_items,
                }
            },
            status=200,
        )
        wall = get_wall_execute(domain="cs102py", count=1)
        self.assertIsInstance(
            wall,
            pd.DataFrame,
            msg="Функция должна возвращать DataFrame, используйте json_normalize",
        )
        self.assertEqual(
            expected_items,
            wall.to_dict("records"),
            msg="Вы должны сделать один запрос, чтобы узнать общее число записей",
        )
        resp_body = unquote(responses.calls[0].request.body)
        self.assertTrue(
            '"count":"1"' in resp_body or '"count":+"1"' in resp_body,
            msg="Вы должны сделать один запрос, чтобы узнать общее число записей",
        )

    @responses.activate
    def test_too_many_requests(self):
        responses.add(
            responses.POST,
            "https://api.vk.com/method/execute",
            json={
                "response": {
                    "count": 6000,
                    "items": [],
                }
            },
            status=200,
        )
        start = time.time()
        with patch("vkapi.wall.get_posts_2500") as get_posts_2500:
            get_posts_2500.return_value = []
            _ = get_wall_execute(domain="cs102py", count=6000)
        end = time.time()
        self.assertGreaterEqual(end - start, 2.0, msg="Слишком много запросов в секунду")
