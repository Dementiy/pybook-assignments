package rsa

import (
	"reflect"
	"testing"
)

func TestIsPrime(t *testing.T) {
	result := isPrime(2)
	expectedResult := true
	if result != expectedResult {
		t.Fatalf("Expected '%t' but got '%t'", expectedResult, result)
	}

	result = isPrime(8)
	expectedResult = false
	if result != expectedResult {
		t.Fatalf("Expected '%t' but got '%t'", expectedResult, result)
	}

	result = isPrime(11)
	expectedResult = true
	if result != expectedResult {
		t.Fatalf("Expected '%t' but got '%t'", expectedResult, result)
	}
}

func TestGCD(t *testing.T) {
	result := gcd(12, 15)
	expectedResult := 3
	if result != expectedResult {
		t.Fatalf("Expected '%d' but got '%d'", expectedResult, result)
	}

	result = gcd(3, 7)
	expectedResult = 1
	if result != expectedResult {
		t.Fatalf("Expected '%d' but got '%d'", expectedResult, result)
	}
}

func TestMultiplicativeInverse(t *testing.T) {
	result := multiplicativeInverse(7, 40)
	expectedResult := 23
	if result != expectedResult {
		t.Fatalf("Expected '%d' but got '%d'", expectedResult, result)
	}
}

func TestEncrypt(t *testing.T) {
	result := Encrypt(Key{19, 187}, "secret")
	expectedResult := []int{174, 50, 143, 113, 50, 24}
	if !reflect.DeepEqual(result, expectedResult) {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}
}

func TestDecrypt(t *testing.T) {
	result := Decrypt(Key{59, 187}, []int{174, 50, 143, 113, 50, 24})
	expectedResult := "secret"
	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}
}
