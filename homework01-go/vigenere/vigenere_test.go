package vigenere

import "testing"

func TestEncryptVigenere(t *testing.T) {
	result := EncryptVigenere("PYTHON", "A")
	expectedResult := "PYTHON"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}

	result = EncryptVigenere("python", "a")
	expectedResult = "python"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}

	result = EncryptVigenere("Python3.6", "a")
	expectedResult = "Python3.6"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}

	result = EncryptVigenere("ATTACKATDAWN", "LEMON")
	expectedResult = "LXFOPVEFRNHR"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}
}

func TestDecryptVigenere(t *testing.T) {
	result := DecryptVigenere("PYTHON", "A")
	expectedResult := "PYTHON"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}

	result = DecryptVigenere("python", "a")
	expectedResult = "python"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}

	result = DecryptVigenere("Python3.6", "a")
	expectedResult = "Python3.6"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}

	result = DecryptVigenere("LXFOPVEFRNHR", "LEMON")
	expectedResult = "ATTACKATDAWN"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}
}
