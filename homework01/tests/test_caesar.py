import unittest
import caesar


class CaesarCipherTest(unittest.TestCase):

    def test_encrypt_empty_string(self):
        self.assertEqual(caesar.encrypt_caesar(""), "")

    def test_encrypt_uppercase(self):
        self.assertEqual(caesar.encrypt_caesar("PYTHON"), "SBWKRQ")

    def test_encrypt_lowercase(self):
        self.assertEqual(caesar.encrypt_caesar("python"), "sbwkrq")

    def test_encrypt_uppercase_and_lowercase(self):
        self.assertEqual(caesar.encrypt_caesar("Python"), "Sbwkrq")

    def test_encrypt_uppercase_lowercase_and_digits(self):
        self.assertEqual(caesar.encrypt_caesar("Python3.6"), "Sbwkrq3.6")
