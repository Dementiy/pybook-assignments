import random
import typing as tp
from math import *


def is_prime(n: int) -> bool:
    if n == 0 or n == 1:
        d = False
    elif n == 2 or n == 3:
        d = True
    elif n > 3:
        a = int(sqrt(n))
        d = True
        for i in range(2, a + 1):
            if n % i == 0:
                d = False
                break
    return d


def gcd(a: int, b: int) -> int:
    while a != b:
        if a < b:
            c = a
            a = b
            b = c
        else:
            a = a - b
    return a


def multiplicative_inverse(e: int, phi: int) -> int:
    t = 1
    while t * e % phi != 1:
        t = t + 1
    return t


def generate_keypair(p: int, q: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal")
    else:
        n = p * q
        phi = (p - 1) * (q - 1)
        e = random.randrange(1, phi)
        while gcd(e, phi) != 1:
            e = random.randrange(1, phi)
        d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)


def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher


def decrypt(pk: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    plain = ''.join(plain)
    return plain


if __name__ == "__main__":
    print("RSA Encrypter/ Decpypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print("".join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
input()
