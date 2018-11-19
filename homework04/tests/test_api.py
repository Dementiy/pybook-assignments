import unittest
from unittest.mock import patch
import requests
import time

from api import get


class TestGetRequest(unittest.TestCase):

    def test_max_retries(self):
        with patch('requests.get', side_effect=requests.exceptions.RequestException) as requests_get:
            with self.assertRaises(requests.exceptions.RequestException):
                get('http://example.com', max_retries=3, backoff_factor=0)
        self.assertEqual(requests_get.call_count, 3)
    
    def test_backoff_factor(self):
        backoff_factor = 0.5
        max_retries = 4
        total_delay = sum([backoff_factor * (2 ** n) for n in range(max_retries-1)])

        start_time = time.time()
        with patch('requests.get', side_effect=requests.exceptions.RequestException) as requests_get:
            with self.assertRaises(requests.exceptions.RequestException):
                get('http://example.com', max_retries=max_retries, backoff_factor=backoff_factor)
        end_time = time.time()
        time_diff = end_time - start_time
        
        self.assertAlmostEqual(time_diff, total_delay, places=0)
        self.assertEqual(requests_get.call_count, max_retries)

    def test_raises_on_timeout_error(self):
        with patch('requests.get', side_effect=requests.exceptions.ReadTimeout):
            with self.assertRaises(requests.exceptions.ReadTimeout):
                get('http://example.com', max_retries=1)

    def test_raises_on_http_error(self):
        with patch('requests.get', side_effect=requests.exceptions.HTTPError):
            with self.assertRaises(requests.exceptions.HTTPError):
                get('http://example.com', max_retries=1)

    def test_raises_on_server_internal_error(self):
        with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
            with self.assertRaises(requests.exceptions.ConnectionError):
                get('http://example.com', max_retries=1)

