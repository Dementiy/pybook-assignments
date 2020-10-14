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
    # PUT YOUR CODE HERE
    newkey=keyword
    for i in range(0, len(plaintext)//len(keyword)):
        newkey+=keyword
    for i in range(0,len(plaintext)):
        try:
            num = int(plaintext[i])
            ciphertext += str(num)
        except ValueError:
            if ord(plaintext[i]) in range(65, 91) and  ord(newkey[i]) in range(65, 91) :
                newchar = ((ord(plaintext[i]) - 65 + ord(newkey[i]) - 65 ) % 26) + 65
                ciphertext += chr(newchar)
            elif ord(plaintext[i]) in range(97, 123)  and  ord(newkey[i]) in range(97, 123):
                newchar = ((ord(plaintext[i]) - 97 + ord(newkey[i])- 97) % 26) + 97
                ciphertext += chr(newchar)
            else:
                ciphertext += plaintext[i]

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
    # PUT YOUR CODE HERE
    newkey=keyword
    for i in range(0, len(ciphertext)//len(keyword)):
        newkey+=keyword
    for i in range(0,len(ciphertext)):
        try:
            num = int(ciphertext[i])
            plaintext += str(num)
        except ValueError:
            if ord(ciphertext[i]) in range(65, 91) and  ord(newkey[i]) in range(65, 91):
                newchar = ((ord(ciphertext[i]) - 65 - (ord(newkey[i])-65)) % 26)
                if newchar < 0:
                    newchar = (25 - newchar) + 65
                else:
                    newchar += 65
                plaintext += chr(newchar)

            elif ord(ciphertext[i]) in range(97, 123) and  ord(newkey[i]) in range(97, 123):
                newchar = ((ord(ciphertext[i]) - 97 - (ord(newkey[i])-97)) % 26)

                if newchar < 0:
                    newchar = (25 - newchar) + 97
                else:
                    newchar += 97
                plaintext += chr(newchar)
            else:
                plaintext += ciphertext[i]
    return plaintext