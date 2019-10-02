def encrypt_caesar(plaintext):
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
    for i in range (0,len(plaintext)):
        t = int(ord(plaintext[i]))
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


def decrypt_caesar(ciphertext):
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
    plaintext=str()
    for i in range (0,len(ciphertext)):
        t = int(ord(ciphertext[i]))
        if t <ord('A'):
            plaintext+=chr(t)
            continue
        if t >ord('Z'):
            if t<ord('a'):
                plaintext+=chr(t)
                continue
        if t>ord('z'):
            plaintext+=chr(t)
            continue
        t-=dem
        if ( t < ord('A') ):
            t=t+ord('Z')-ord('A')+1
        if( t < ord('a') ):
            if ( t > ord('Z')):
                t=t+ord('z')-ord('a')+1
        plaintext+=chr(t)
    return plaintext
