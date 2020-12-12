import re
import unittest

import responses

from research.network import ego_network


class EgoNetworkTestCase(unittest.TestCase):
    @responses.activate
    def test_network(self):
        target_uids = [1, 2, 3, 4, 5]
        responses.add(
            responses.GET,
            re.compile(
                f"https://api.vk.com/method/friends.getMutual\?.*target_uids={target_uids}.*"
            ),
            match_querystring=True,
            json={
                "response": [
                    {
                        "id": 1,
                        "common_friends": [2, 3],
                        "common_count": 2,
                    },
                    {
                        "id": 2,
                        "common_friends": [1, 3, 4],
                        "common_count": 3,
                    },
                    {
                        "id": 3,
                        "common_friends": [1, 2],
                        "common_count": 2,
                    },
                    {
                        "id": 4,
                        "common_friends": [2],
                        "common_count": 1,
                    },
                    {
                        "id": 5,
                        "common_friends": [],
                        "common_count": 0,
                    },
                ]
            },
            status=200,
        )
        expected_edges = [
            (1, 2),
            (1, 3),
            (2, 1),
            (2, 3),
            (2, 4),
            (3, 1),
            (3, 2),
            (4, 2),
        ]
        edges = ego_network(friends=target_uids)
        self.assertEqual(set(expected_edges), set(edges))
