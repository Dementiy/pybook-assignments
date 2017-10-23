package rsa

import (
    "testing"
    "reflect"
)

func TestIsPrime(t *testing.T) {
    result := isPrime(2)
    expected_result := true
    if result != expected_result {
        t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
    }

    result = isPrime(8)
    expected_result = false
    if result != expected_result {
        t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
    }

    result = isPrime(11)
    expected_result = true
    if result != expected_result {
        t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
    }
}


func TestGCD(t *testing.T) {
    result := gcd(12, 15)
    expected_result := 3
    if result != expected_result {
        t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
    }

    result = gcd(3, 7)
    expected_result = 1
    if result != expected_result {
        t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
    }
}


func TestMultiplicativeInverse(t *testing.T) {
    result := multiplicativeInverse(7, 40)
    expected_result := 23
    if result != expected_result {
        t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
    }
}


func TestEncrypt(t *testing.T) {
    result := Encrypt(Key{19, 187}, "secret")
    expected_result := []int{174, 50, 143, 113, 50, 24}
    if !reflect.DeepEqual(result, expected_result) {
        t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
    }
}


func TestDecrypt(t *testing.T) {
    result := Decrypt(Key{59, 187}, []int{174, 50, 143, 113, 50, 24})
    expected_result := "secret"
    if result != expected_result {
        t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
    }
}

