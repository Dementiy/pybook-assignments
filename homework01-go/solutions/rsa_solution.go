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
    if n == 2 || n == 3 {
        return true
    }

    if n < 2 || n % 2 == 0 {
        return false
    }

    for i := 2; i <= int(math.Floor(math.Sqrt(float64(n)))); i++ {
        if n % i == 0 {
            return false
        }
    }
    return true
}


func gcd(a int, b int) int {
    for b != 0 {
        a, b = b, a % b
    }
    return a
}


func multiplicativeInverse(e int, phi int) int {
    var tbl [][]int

    A := phi
    B := e
    row := []int{A, B, A % B, A / B, -1, -1}
    tbl = append(tbl, row)
    for i := 0; tbl[i][2] != 0; i++ {
        A = tbl[i][1]
        B = tbl[i][2]
        row := []int{A, B, A % B, A / B, -1, -1}
        tbl = append(tbl, row)
    }

    tbl[len(tbl)-1][4] = 0
    tbl[len(tbl)-1][5] = 1
    for i := len(tbl)-2; i >= 0; i-- {
        tbl[i][4] = tbl[i+1][5]
        tbl[i][5] = tbl[i+1][4] - tbl[i+1][5]*tbl[i][3]
    }

    r := tbl[0][5] % phi
    if r < 0 {
        r = r + phi
    }
    return r
}


func GenerateKeypair(p int, q int) (KeyPair, error) {
    // https://golang.org/pkg/errors/
    if !isPrime(p) || !isPrime(q) {
        return KeyPair{}, errors.New("Both numbers must be prime.")
    } else if  p == q {
        return KeyPair{}, errors.New("p and q can't be equal.")
    }

    n := p * q
    phi := (p - 1)*(q - 1)
    // https://golang.org/pkg/math/rand/#Intn
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
