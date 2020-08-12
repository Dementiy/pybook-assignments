import unittest

import caesar


class EncryptTestCase(unittest.TestCase):
    def test_shift0(self):
        cases = [
            ("", ""),
            ("python", "python"),
            ("PYTHON", "PYTHON"),
            ("Python", "Python"),
            ("Python3.6", "Python3.6"),
        ]

        for i, (plaintext, chiphertext) in enumerate(cases):
            with self.subTest(case=i, plaintext=plaintext, chiphertext=chiphertext):
                self.assertEqual(chiphertext, caesar.encrypt_caesar(plaintext, shift=0))

    def test_shift3(self):
        cases = [
            ("", ""),
            ("PYTHON", "SBWKRQ"),
            ("python", "sbwkrq"),
            ("Python", "Sbwkrq"),
            ("Python3.6", "Sbwkrq3.6"),
        ]

        for i, (plaintext, chiphertext) in enumerate(cases):
            with self.subTest(case=i, plaintext=plaintext, chiphertext=chiphertext):
                self.assertEqual(chiphertext, caesar.encrypt_caesar(plaintext, shift=3))


class DecryptTestCase(unittest.TestCase):
    def test_shift0(self):
        cases = [
            ("", ""),
            ("python", "python"),
            ("PYTHON", "PYTHON"),
            ("Python", "Python"),
            ("Python3.6", "Python3.6"),
        ]

        for i, (chiphertext, plaintext) in enumerate(cases):
            with self.subTest(case=i, chiphertext=chiphertext, plaintext=plaintext):
                self.assertEqual(plaintext, caesar.decrypt_caesar(chiphertext, shift=0))

    def test_shift3(self):
        cases = [
            ("", ""),
            ("SBWKRQ", "PYTHON"),
            ("sbwkrq", "python"),
            ("Sbwkrq", "Python"),
            ("Sbwkrq3.6", "Python3.6"),
        ]

        for i, (chiphertext, plaintext) in enumerate(cases):
            with self.subTest(case=i, chiphertext=chiphertext, plaintext=plaintext):
                self.assertEqual(plaintext, caesar.decrypt_caesar(chiphertext, shift=3))
