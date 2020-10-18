def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    i=0
    ciphertext = ""
    while i<len(plaintext):
        a = o
        if ord(ciphertext[i]) > ord('a') and ord(ciphertext[i]) < ord('z'):
            a = ord(ciphertext[i])+shift
            if a>ord('z'):
                a=a-ord('z')+ord('a')-1
            if a>ord('Z') and a<ord('a'):
                a = a - ord('z') + ord('a') - 1
        if a<1:
            a=ord(ciphertext[i])
        plaintext = plaintext + (chr(a))
        i = i + 1
    return ciphertext
print(encrypt_caesar('Python'))


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    i=0
    plaintext = ""
    while i<len(ciphertext):
        a=o
        if ord(ciphertext[i])>ord('a') and ord(ciphertext[i])<ord('z'):
            a=ord(ciphertext[i])-shift
            if a<ord('a') and a>ord('Z'):
                a=a+ord('z')-ord('a')+1
            if a ord('A'):
                a=a+ord('z')-ord('a')+1
        if a<1:
            a=ord(ciphertext[i])
        plaintext=plaintext+(chr(a))
        i=i+1

    return plaintext
print(decrypt_caesar('Sqwkrn'))