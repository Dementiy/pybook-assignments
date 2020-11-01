a = []
b = []
for m in range(65, 91):
    a.append(chr(m))
for n in range(97, 123):
    b.append(chr(n))


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    d = len(plaintext) // len(keyword)
    keyword = list(keyword)
    keyword1 = list(range(len(keyword)))
    for i in range(len(keyword)):
        for j in range(len(a)):
            if keyword[i] == a[j]:
                keyword1[i] = j
            if keyword[i] == b[j]:
                keyword1[i] = j
    tran = keyword1 * (d + 1)
    ciphertext = list(plaintext)
    for i in range(len(plaintext)):
        for j in range(len(a)):
            if plaintext[i] == a[j]:
                if j + tran[i] < 26:
                    ciphertext[i] = a[j + tran[i]]
                else:
                    ciphertext[i] = a[j + tran[i] - 26]
            if plaintext[i] == b[j]:
                if j + tran[i] < 26:
                    ciphertext[i] = b[j + tran[i]]
                else:
                    ciphertext[i] = b[j + tran[i] - 26]
    ciphertext = ''.join(ciphertext)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    d = len(ciphertext) // len(keyword)
    keyword = list(keyword)
    keyword1 = list(range(len(keyword)))
    for i in range(len(keyword)):
        for j in range(len(a)):
            if keyword[i] == a[j]:
                keyword1[i] = j
            if keyword[i] == b[j]:
                keyword1[i] = j
    tran = keyword1 * (d + 1)
    plaintext = list(ciphertext)
    for i in range(len(ciphertext)):
        for j in range(len(a)):
            if ciphertext[i] == a[j]:
                if j < tran[i]:
                    plaintext[i] = a[j + 26 - tran[i]]
                else:
                    plaintext[i] = a[j - tran[i]]
            if ciphertext[i] == b[j]:
                if j < tran[i]:
                    plaintext[i] = b[j + 26 - tran[i]]
                else:
                    plaintext[i] = b[j - tran[i]]
    plaintext = ''.join(plaintext)
    return plaintext
