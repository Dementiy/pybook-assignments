import string

def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i in range(len(plaintext)):
        keyword = keyword.lower()
        a = ord(keyword[i%len(keyword)]) - ord('a')
        if 'a' <= plaintext[i] <= 'z':
            a = ord(plaintext[i]) + a
            if a > ord('z'):
                a = a - 26
        if 'A' <= plaintext[i] <= 'Z':
            a = ord(plaintext[i]) + a
            if a > ord('Z'):
                a = a - 26
        ciphertext = ciphertext + chr(a)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for i in range(len(ciphertext)):
        keyword = keyword.lower()
        a = ord(keyword[i%len(keyword)]) - ord('a')
        if 'a' <= ciphertext[i] <= 'z':
            a = ord(ciphertext[i]) - a
            if a < ord('a'):
                a = a + 26
        if 'A' <= ciphertext[i] <= 'Z':
            a = ord(ciphertext[i]) - a
            if a < ord('A'):
                a = a + 26
        plaintext = plaintext + chr(a)
    return plaintext
