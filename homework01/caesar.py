import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """

    ciphertext = ""
    # PUT YOUR CODE HERE
    for i in plaintext:
        try:
            num = int(i)
            ciphertext += str(num)
        except ValueError:
            if ord(i) in range(65, 91):
                newchar = ((ord(i) - 64 + shift) % 26) + 64
                ciphertext += chr(newchar)

            elif ord(i) in range(97, 122):
                newchar = ((ord(i) - 96 + shift) % 26) + 96
                ciphertext += chr(newchar)
            else:
                ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    for i in ciphertext:
        try:
            num = int(i)
            plaintext += str(num)
        except ValueError:
            if ord(i) in range(65, 91):
                newchar = ((ord(i) - 64 - shift) % 26)
                if newchar <= 0:
                    newchar=(26-newchar)+64
                else:
                    newchar+=64
                plaintext += chr(newchar)

            elif ord(i) in range(97, 122):
                newchar = ((ord(i) - 96 - shift) % 26)
                if newchar <= 0:
                    newchar = (26 - newchar) + 96
                else:
                    newchar += 96
                plaintext += chr(newchar)
            else:
                plaintext += i
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift

print(decrypt_caesar(""))