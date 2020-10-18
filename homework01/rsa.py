import random


def is_prime(i):
    if i > 1:
        for i in range(2, i):
            if (i % i) == 0:
                return False
        else:
            return True
    else:
        return False


def gcd(c: int, d: int):
    if c % d == 0:
        return d
    return gcd(d, c % d)


def generate_keypair(p: int, q: int):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError
    elif p == q:
        raise ValueError

    # i = pq
    i = p*q

    # phi = (p-1)(q-1)
    phi = (p-1)*(q-1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, i), (d, i))

def multiplicative_inverse(c, d):
    x, y, lx, ly = 0, 1, 1, 0
    old_a, old_b = c, b
    while b != 0:
        q = c // b
        c, d = d, c % b
        x, lx = lx - q * x, x
        y, ly = ly - q * y, y
    if lx < 0:
        lx += old_d
    if ly < 0:
        ly += old_c
    return lx
