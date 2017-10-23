package caesar

import "testing"

func TestEncryptCaesar(t *testing.T) {
	result := encryptCaesar("PYTHON", 3)
	expected_result := "SBWKRQ"

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}

	result = encryptCaesar("python", 3)
	expected_result = "sbwkrq"

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}

	result = encryptCaesar("Python3.6", 3)
	expected_result = "Sbwkrq3.6"

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}

	result = encryptCaesar("", 3)
	expected_result = ""

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}
}

func TestDecryptCaesar(t *testing.T) {
	result := decryptCaesar("SBWKRQ", 3)
	expected_result := "PYTHON"

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}

	result = decryptCaesar("sbwkrq", 3)
	expected_result = "python"

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}

	result = decryptCaesar("Sbwkrq3.6", 3)
	expected_result = "Python3.6"

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}

	result = decryptCaesar("", 3)
	expected_result = ""

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}
}
