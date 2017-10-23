package rsa

import (
    "math"
    "math/rand"
    "math/big"
    "errors"
)

type Key struct {
    key int
    n int
}

type KeyPair struct {
    Private Key
    Public Key
}

func isPrime(n int) bool {
    // PUT YOUR CODE HERE
}


func gcd(a int, b int) int {
    // PUT YOUR CODE HERE
}


func multiplicativeInverse(e int, phi int) int {
    // PUT YOUR CODE HERE
}


func GenerateKeypair(p int, q int) (KeyPair, error) {
    if !isPrime(p) || !isPrime(q) {
        return KeyPair{}, errors.New("Both numbers must be prime.")
    } else if  p == q {
        return KeyPair{}, errors.New("p and q can't be equal.")
    }

    // n = pq
    // PUT YOUR CODE HERE

    // phi = (p-1)(q-1)
    // PUT YOUR CODE HERE

    e := rand.Intn(phi - 1) + 1
    g := gcd(e, phi)
    for g != 1 {
        e = rand.Intn(phi - 1) + 1
        g = gcd(e, phi)
    }

    d := multiplicativeInverse(e, phi)
    return KeyPair{Key{e, n}, Key{d, n}}, nil
}


func Encrypt(pk Key, plaintext string) []int {
    cipher := []int{}
    n := new(big.Int)
    for _, ch := range plaintext {
        n = new(big.Int).Exp(
            big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
        n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
        cipher = append(cipher, int(n.Int64()))
    }
    return cipher
}


func Decrypt(pk Key, cipher []int) string {
    plaintext := ""
    n := new(big.Int)
    for _, ch := range cipher {
        n = new(big.Int).Exp(
            big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
        n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
        plaintext += string(rune(int(n.Int64())))
    }
    return plaintext
}
