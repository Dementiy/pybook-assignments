def encrypt_caesar(plaintext: str) -> str:
    ciphertext = ''
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            if chr((ord(plaintext[i]) + 3)).isalpha():
                ciphertext += chr(ord(plaintext[i]) + 3)
            else:
                ciphertext += chr(ord(plaintext[i]) - 23)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
    plaintext = ''
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            if chr((ord(ciphertext[i]) - 3)).isalpha():
                plaintext += chr(ord(ciphertext[i]) - 3)
            else:
                plaintext += chr(ord(ciphertext[i]) + 23)
        else:
            plaintext += ciphertext[i]
    return plaintext
