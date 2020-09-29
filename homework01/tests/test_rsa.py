import random
import unittest

import rsa


class RSATestCase(unittest.TestCase):
    def test_is_prime(self):
        self.assertFalse(rsa.is_prime(1))
        self.assertTrue(rsa.is_prime(2))
        self.assertTrue(rsa.is_prime(3))
        self.assertFalse(rsa.is_prime(4))
        self.assertTrue(rsa.is_prime(5))
        self.assertFalse(rsa.is_prime(6))
        self.assertTrue(rsa.is_prime(7))
        self.assertFalse(rsa.is_prime(8))
        self.assertTrue(rsa.is_prime(3571))

    def test_gcd(self):
        self.assertEqual(0, rsa.gcd(0, 0))
        self.assertEqual(1, rsa.gcd(3, 7))
        self.assertEqual(3, rsa.gcd(12, 15))
        self.assertEqual(9, rsa.gcd(0, 9))
        self.assertEqual(12, rsa.gcd(12, 0))
        self.assertEqual(14, rsa.gcd(42, 56))
        self.assertEqual(18, rsa.gcd(461952, 116298))
        self.assertEqual(32, rsa.gcd(7966496, 314080416))
        self.assertEqual(526, rsa.gcd(24826148, 45296490))

    def test_multiplicative_inverse(self):
        self.assertEqual(23, rsa.multiplicative_inverse(7, 40))
        self.assertEqual(1969, rsa.multiplicative_inverse(42, 2017))
        self.assertEqual(0, rsa.multiplicative_inverse(40, 1))
        self.assertEqual(169, rsa.multiplicative_inverse(121, 288))
        self.assertEqual(734969, rsa.multiplicative_inverse(142169, 1694640))
        self.assertEqual(1804547, rsa.multiplicative_inverse(9678731, 11181456))

    def test_generate_keypair(self):
        random.seed(1234567)
        self.assertEqual(((121, 323), (169, 323)), rsa.generate_keypair(17, 19))
        self.assertEqual(((142169, 1697249), (734969, 1697249)), rsa.generate_keypair(1229, 1381))
        self.assertEqual(
            ((9678731, 11188147), (1804547, 11188147)), rsa.generate_keypair(3259, 3433)
        )
