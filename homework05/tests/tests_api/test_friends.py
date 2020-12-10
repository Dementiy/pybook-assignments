import re
import time
import unittest

import responses

from vkapi.friends import FriendsResponse, get_friends, get_mutual


class FriendsTestCase(unittest.TestCase):
    @responses.activate
    def test_get_friends(self):
        expected_fids = [1, 2, 3, 4, 5]
        responses.add(
            responses.GET,
            "https://api.vk.com/method/friends.get",
            json={"response": {"count": len(expected_fids), "items": expected_fids}},
            status=200,
        )
        fids = get_friends(user_id=1)
        expected_response = FriendsResponse(count=len(expected_fids), items=expected_fids)
        self.assertEqual(expected_response, fids)

    @responses.activate
    def test_get_mutual(self):
        common_friends = [1, 2, 3, 4, 5]
        target_uid = 456
        responses.add(
            responses.GET,
            re.compile(f"https://api.vk.com/method/friends.getMutual\?.*target_uid={target_uid}.*"),
            match_querystring=True,
            json={"response": common_friends},
            status=200,
        )
        responses.add(
            responses.GET,
            re.compile(
                f"https://api.vk.com/method/friends.getMutual\?.*target_uids={target_uid}.*"
            ),
            match_querystring=True,
            json={
                "response": [
                    {
                        "id": target_uid,
                        "common_friends": common_friends,
                        "common_count": len(common_friends),
                    }
                ]
            },
            status=200,
        )
        mutual_friends = get_mutual(source_uid=123, target_uid=456)
        self.assertEqual(common_friends, mutual_friends)

    @responses.activate
    def test_get_mutual_more_than100(self):
        responses.add(
            responses.GET,
            re.compile("https://api.vk.com/method/friends.getMutual\?.*offset=0.*"),
            match_querystring=True,
            json={"response": [{"id": 1, "common_friends": [2, 3], "common_count": 2}]},
            status=200,
        )
        responses.add(
            responses.GET,
            re.compile("https://api.vk.com/method/friends.getMutual\?.*offset=100.*"),
            match_querystring=True,
            json={"response": [{"id": 2, "common_friends": [1, 3], "common_count": 2}]},
            status=200,
        )
        responses.add(
            responses.GET,
            re.compile("https://api.vk.com/method/friends.getMutual\?.*offset=200.*"),
            match_querystring=True,
            json={"response": [{"id": 3, "common_friends": [1, 2], "common_count": 2}]},
            status=200,
        )

        mutual_friends = get_mutual(target_uids=list(range(300)))
        self.assertEqual(
            [
                {"common_count": 2, "common_friends": [2, 3], "id": 1},
                {"common_count": 2, "common_friends": [1, 3], "id": 2},
                {"common_count": 2, "common_friends": [1, 2], "id": 3},
            ],
            mutual_friends,
        )

    @responses.activate
    def test_get_mutual_too_many_requests_handled_properly(self):
        common_friends = [{"id": 1, "common_friends": [2], "common_count": 1}]
        responses.add(
            responses.GET,
            "https://api.vk.com/method/friends.getMutual",
            json={"response": common_friends},
            status=200,
        )
        n_reqs = 4
        start = time.time()
        mutual_friends = get_mutual(target_uids=list(range(n_reqs * 100)))
        end = time.time()
        self.assertGreaterEqual(end - start, 1.0, msg="Слишком много запросов в секунду")
        self.assertEqual(common_friends * n_reqs, mutual_friends)
