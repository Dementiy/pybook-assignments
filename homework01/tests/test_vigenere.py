import random
import string
import unittest

import vigenere


class VigenereTestCase(unittest.TestCase):
    def test_encrypt(self):
        cases = [
            ("PYTHON", "A", "PYTHON"),
            ("python", "a", "python"),
            ("introduction to python", "lsci", "tfvzzvwkeaqv lq aqvpzf"),
            ("ATTACKATDAWN", "LEMON", "LXFOPVEFRNHR"),
        ]

        for i, (plaintext, keyword, chiphertext) in enumerate(cases):
            with self.subTest(
                case=i, plaintext=plaintext, keyword=keyword, chiphertext=chiphertext
            ):
                self.assertEqual(chiphertext, vigenere.encrypt_vigenere(plaintext, keyword))

    def test_decrypt(self):
        cases = [
            ("PYTHON", "A", "PYTHON"),
            ("python", "a", "python"),
            ("tfvzzvwkeaqv lq aqvpzf", "lsci", "introduction to python"),
            ("LXFOPVEFRNHR", "LEMON", "ATTACKATDAWN"),
        ]

        for i, (chiphertext, keyword, plaintext) in enumerate(cases):
            with self.subTest(
                case=i, chiphertext=chiphertext, keyword=keyword, plaintext=plaintext
            ):
                self.assertEqual(plaintext, vigenere.decrypt_vigenere(chiphertext, keyword))

    def test_randomized(self):
        kwlen = random.randint(4, 24)
        keyword = ''.join(random.choice(string.ascii_letters) for _ in range(kwlen))
        plaintext = ''.join(random.choice(string.ascii_letters + ' -,') for _ in range(64))
        ciphertext = vigenere.encrypt_vigenere(plaintext, keyword)
        self.assertEqual(plaintext, vigenere.decrypt_vigenere(ciphertext, keyword))
