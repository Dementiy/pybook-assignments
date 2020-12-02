import unittest

from hello import get_greeting


class HelloTestCase(unittest.TestCase):
    def test_hello(self):
        cases = [
            ("World", "Hello, World!"),
            ("Anonymous", "Hello, Anonymous!"),
        ]
        for i, (name, message) in enumerate(cases, start=1):
            with self.subTest(case=i):
                self.assertEqual(message, get_greeting(name))
