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
                newchar = ((ord(i) - 65 + shift) % 26) + 65
                ciphertext += chr(newchar)

            elif ord(i) in range(97, 123):
                newchar = ((ord(i) - 97 + shift) % 26) + 97
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
                newchar = ((ord(i) - 65 - shift) % 26)
                if newchar < 0:
                    newchar=(25-newchar)+65
                else:
                    newchar+=65
                plaintext += chr(newchar)

            elif ord(i) in range(97, 123):
                newchar = ((ord(i) - 97 - shift) % 26)
                if newchar < 0:
                    newchar = (25 - newchar) + 97
                else:
                    newchar += 97
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