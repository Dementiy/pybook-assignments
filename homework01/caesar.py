def encrypt_caesar(s):
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
    # PUT YOUR CODE HERE
    ciphertext=str()
    for i in range (0,len(s)):
        t = int(ord(s[i]))
        if t <ord('A'):
            ciphertext+=chr(t)
            continue
        if t >ord('Z'):
            if t<ord('a'):
                ciphertext+=chr(t)
                continue
        if t>ord('z'):
            ciphertext+=chr(t)
            continue
        t+=3
        if ( t > ord('Z') ):
            if( t < ord('a') ):
                t=t-ord('Z')+ord('A')-1
            if( t >= ord('z') ):
                t=t-ord('z')+ord('a')-1
        ciphertext+=chr(t)
    return ciphertext


def decrypt_caesar(s):
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
    # PUT YOUR CODE HERE
    s1=str()
    for i in range (0,len(s)):
        t = int(ord(s[i]))
        if t <ord('A'):
            s1+=chr(t)
            continue
        if t >ord('Z'):
            if t<ord('a'):
                s1+=chr(t)
                continue
        if t>ord('z'):
            s1+=chr(t)
            continue
        t-=3
        if ( t < ord('A') ):
            t=t+ord('Z')-ord('A')+1
        if( t < ord('a') ):
            if ( t > ord('Z')):
                t=t+ord('z')-ord('a')+1
        s1+=chr(t)
    return s1

plaintext=str(input())
ciphertext=str(input())
kq1=encrypt_caesar(plaintext)
print(kq1)
kq2=decrypt_caesar(ciphertext)
print(kq2)
