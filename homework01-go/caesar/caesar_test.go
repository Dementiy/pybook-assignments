package caesar

import "testing"

func TestEncryptCaesar(t *testing.T) {
	result := EncryptCaesar("PYTHON", 3)
	expectedResult := "SBWKRQ"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}

	result = EncryptCaesar("python", 3)
	expectedResult = "sbwkrq"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}

	result = EncryptCaesar("Python3.6", 3)
	expectedResult = "Sbwkrq3.6"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}

	result = EncryptCaesar("", 3)
	expectedResult = ""

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}
}

func TestDecryptCaesar(t *testing.T) {
	result := DecryptCaesar("SBWKRQ", 3)
	expectedResult := "PYTHON"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}

	result = DecryptCaesar("sbwkrq", 3)
	expectedResult = "python"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}

	result = DecryptCaesar("Sbwkrq3.6", 3)
	expectedResult = "Python3.6"

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}

	result = DecryptCaesar("", 3)
	expectedResult = ""

	if result != expectedResult {
		t.Fatalf("Expected '%s' but got '%s'", expectedResult, result)
	}
}
