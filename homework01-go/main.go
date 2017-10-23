package main

import (
    "fmt"
    "flag"
    "os"
    "./rsa"
)


func main() {
    p := flag.Int("p", 11, "")
    q := flag.Int("q", 17, "")
    plaintext := flag.String("text", "", "")
    flag.Parse()
    keys, err := rsa.GenerateKeypair(*p, *q)
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
    ciphertext := rsa.Encrypt(keys.Private, *plaintext)
    fmt.Println("Encrypted message:", ciphertext)
    fmt.Println("Decrypted message:", rsa.Decrypt(keys.Public, ciphertext))
}
