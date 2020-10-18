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
    for i in range(len(plaintext)):
        a = 0
        if 'a' <= plaintext[i] <= 'z':
            a = ord(plaintext[i]) + shift
            if a > ord('z'):
                a = a - 26
        if 'A' <= plaintext[i] <= 'Z':
            a = ord(plaintext[i]) + shift
            if a > ord('Z'):
                a = a - 26
        if a < 1:
            a = ord(plaintext[i])
        ciphertext = ciphertext + (chr(a))
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
    for i in range(len(ciphertext)):
        a = 0
        if 'a' <= ciphertext[i] <= 'z':
            a = ord(ciphertext[i]) - shift
            if a < ord('a'):
                a = a + 26
        if 'A' <= ciphertext[i] <= 'Z':
            a = ord(ciphertext[i]) - shift
            if a < ord('A'):
                a = a + 26
        if a < 1:
            a = ord(ciphertext[i])
        plaintext = plaintext + (chr(a))
    return plaintext
print(decrypt_caesar("Sbwkrq3.6"))