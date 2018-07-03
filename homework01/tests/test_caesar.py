import unittest
from solutions import caesar


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

    def test_decrypt_empty_string(self):
        self.assertEqual(caesar.decrypt_caesar(""), "")

    def test_decrypt_uppercase(self):
        self.assertEqual(caesar.decrypt_caesar("SBWKRQ"), "PYTHON")

    def test_decrypt_lowercase(self):
        self.assertEqual(caesar.decrypt_caesar("sbwkrq"), "python")

    def test_decrypt_uppercase_and_lowercase(self):
        self.assertEqual(caesar.decrypt_caesar("Sbwkrq"), "Python")

    def test_decrypt_uppercase_lowercase_and_digits(self):
        self.assertEqual(caesar.decrypt_caesar("Sbwkrq3.6"), "Python3.6")

