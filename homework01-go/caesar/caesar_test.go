package caesar

import "testing"

func TestEncryptCaesar(t *testing.T) {
	result := encrypt_caesar("PYTHON", 3)
	expected_result := "SBWKRQ"

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}

	result = encrypt_caesar("python", 3)
	expected_result = "sbwkrq"

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}

	result = encrypt_caesar("Python3.6", 3)
	expected_result = "Sbwkrq3.6"

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}

	result = encrypt_caesar("", 3)
	expected_result = ""

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}
}

func TestDecryptCaesar(t *testing.T) {
	result := decrypt_caesar("SBWKRQ", 3)
	expected_result := "PYTHON"

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}

	result = decrypt_caesar("sbwkrq", 3)
	expected_result = "python"

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}

	result = decrypt_caesar("Sbwkrq3.6", 3)
	expected_result = "Python3.6"

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}

	result = decrypt_caesar("", 3)
	expected_result = ""

	if result != expected_result {
		t.Fatalf("Expected '%s' but got '%s'", expected_result, result)
	}
}
