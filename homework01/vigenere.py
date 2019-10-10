def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # PUT YOUR CODE HERE
    ciphertext=str()
    tro=0
    for i in range(0,len(plaintext)):
        if plaintext[i] >= 'A':
            if plaintext[i]<='Z':
                t=ord(plaintext[i])+ord(keyword[tro])-ord('A')
                if t > ord('Z'):
                    t-=26
                ciphertext+=chr(t)
        if plaintext[i] >= 'a':
            if plaintext[i]<='z':
                t=ord(plaintext[i])+ord(keyword[tro])-ord('a')
                if t > ord('z'):
                    t-=26
                ciphertext+=chr(t)
        tro+=1
        if(tro== len(keyword)):
            tro=0
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    plaintext=str()
    tro=0
    for i in range(0,len(ciphertext)):
        if ciphertext[i] >= 'A':
            if ciphertext[i]<='Z':
                t=ord(ciphertext[i])-ord(keyword[tro])+ord('A')
                if t < ord('A'):
                    t+=26
                plaintext+=chr(t)
        if ciphertext[i] >= 'a':
            if ciphertext[i]<='z':
                t=ord(sciphertext[i])-ord(keyword[tro])+ord('a')
                if t < ord('a'):
                    t+=26
                plaintext+=chr(t)
        tro+=1
        if(tro== len(keyword)):
            tro=0
    return plaintext
plaintext=str(input())
keyword1=str(input())
ciphertext=str(input())
keyword2=str(input())
ciphertext=encrypt_vigenere(plaintext,keyword1)
print(ciphertext)
plaintext=decrypt_vigenere(ciphertext,keyword2)
print( plaintext)
