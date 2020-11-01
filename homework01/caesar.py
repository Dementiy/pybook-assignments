import typing as tp
a = []
b = []
for m in range(65, 91):
    a.append(chr(m))
for n in range(97, 123):
    b.append(chr(n))


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    shift = shift % 26
    ciphertext = list(plaintext)
    for i in range(len(plaintext)):
        for j in range(len(a)):
            if plaintext[i] == a[j]:
                if j + shift < 26:
                    ciphertext[i] = a[j + shift]
                else:
                    ciphertext[i] = a[j + shift - 26]
            if plaintext[i] == b[j]:
                if j + shift < 26:
                    ciphertext[i] = b[j + shift]
                else:
                    ciphertext[i] = b[j + shift - 26]
    ciphertext = ''.join(ciphertext)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    shift = shift % 26
    plaintext = list(ciphertext)
    for i in range(len(ciphertext)):
        for j in range(len(a)):
            if ciphertext[i] == a[j]:
                if j < shift:
                    plaintext[i] = a[j + 26 - shift]
                else:
                    plaintext[i] = a[j - shift]
            if ciphertext[i] == b[j]:
                if j < shift:
                    plaintext[i] = b[j + 26 - shift]
                else:
                    plaintext[i] = b[j - shift]
    plaintext = ''.join(plaintext)
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    best_shift = 0
    for i in range(25):
        if decrypt_caesar(ciphertext, i) in dictionary:
            best_shift = i
    return best_shift
