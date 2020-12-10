import time
import unittest

import httpretty
import responses
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout, RetryError

from vkapi.session import Session


class TestSession(unittest.TestCase):
    @httpretty.activate
    def test_max_retries(self):
        session = Session("https://example.com", max_retries=5, backoff_factor=0)
        httpretty.register_uri(
            httpretty.GET,
            "https://example.com/",
            responses=[
                httpretty.Response(
                    body="",
                    status=500,
                ),
                httpretty.Response(
                    body="",
                    status=500,
                ),
                httpretty.Response(
                    body="",
                    status=500,
                ),
            ],
        )
        with self.assertRaises(RetryError):
            _ = session.get("")
        self.assertEqual(6, len(httpretty.latest_requests()))

    @httpretty.activate
    def test_backoff_factor(self):
        backoff_factor = 0.5
        max_retries = 4
        total_delay = sum(backoff_factor * (2 ** n) for n in range(1, max_retries))

        session = Session(
            "https://example.com",
            max_retries=max_retries,
            backoff_factor=backoff_factor,
        )
        httpretty.register_uri(
            httpretty.GET,
            "https://example.com/",
            responses=[
                httpretty.Response(
                    body="",
                    status=500,
                )
                for _ in range(max_retries)
            ],
        )
        start_time = time.time()
        with self.assertRaises(RetryError):
            _ = session.get("")
        end_time = time.time()
        time_diff = end_time - start_time

        self.assertAlmostEqual(time_diff, total_delay, places=0)
        self.assertEqual(max_retries + 1, len(httpretty.latest_requests()))

    @responses.activate
    def test_raises_on_timeout_error(self):
        responses.add(responses.GET, "https://example.com", body=ReadTimeout())
        session = Session("https://example.com", max_retries=1)
        with self.assertRaises(ReadTimeout):
            _ = session.get("")

    @responses.activate
    def test_raises_on_http_error(self):
        responses.add(responses.GET, "https://example.com", body=HTTPError())
        session = Session("https://example.com", max_retries=1)
        with self.assertRaises(HTTPError):
            _ = session.get("")

    @responses.activate
    def test_raises_on_server_internal_error(self):
        responses.add(responses.GET, "https://example.com", body=ConnectionError())
        session = Session("https://example.com", max_retries=1)
        with self.assertRaises(ConnectionError):
            _ = session.get("")
