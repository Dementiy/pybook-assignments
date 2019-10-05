package vigenere

func EncryptVigenere(plaintext string, keyword string) string {
	var ciphertext string

	// PUT YOUR CODE HERE
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
}

func DecryptVigenere(ciphertext string, keyword string) string {
	var plaintext string

	// PUT YOUR CODE HERE
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
}
