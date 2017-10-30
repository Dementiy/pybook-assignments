package main

import (
	"reflect"
	"testing"
)

func TestGroup(t *testing.T) {
	result := group([]byte{1, 2, 3, 4}, 2)
	expected_result := [][]byte{{1, 2}, {3, 4}}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}

	result = group([]byte{1, 2, 3, 4, 5, 6, 7, 8, 9}, 3)
	expected_result = [][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}
}

func TestGetCol(t *testing.T) {
	result := getCol([][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, 0)
	expected_result := []byte{1, 4, 7}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}

	result = getCol([][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, 1)
	expected_result = []byte{2, 5, 8}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}

	result = getCol([][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, 2)
	expected_result = []byte{3, 6, 9}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}
}

func TestGetRow(t *testing.T) {
	result := getRow([][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, 0)
	expected_result := []byte{1, 2, 3}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}

	result = getRow([][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, 1)
	expected_result = []byte{4, 5, 6}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}

	result = getRow([][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, 2)
	expected_result = []byte{7, 8, 9}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}
}

func TestGetBlock(t *testing.T) {
	grid, _ := readSudoku("puzzle1.txt")
	result := getBlock(grid, 0, 1)
	expected_result := []byte{'5', '3', '.', '6', '.', '.', '.', '9', '8'}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}

	result = getBlock(grid, 4, 7)
	expected_result = []byte{'.', '.', '3', '.', '.', '1', '.', '.', '6'}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}

	result = getBlock(grid, 8, 8)
	expected_result = []byte{'2', '8', '.', '.', '.', '5', '.', '7', '9'}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}
}

func TestFindEmptyPosition(t *testing.T) {
	row, col := findEmptyPosition([][]byte{{1, 2, '.'}, {4, 5, 6}, {7, 8, 9}})
	expected_row, expected_col := 0, 2
	if row != expected_row || col != expected_col {
		t.Fatalf("Expected '(%d,%d)' but got '(%d,%d)'",
			expected_row, expected_col, row, col)
	}

	row, col = findEmptyPosition([][]byte{{1, 2, 3}, {4, '.', 6}, {7, 8, 9}})
	expected_row, expected_col = 1, 1
	if row != expected_row || col != expected_col {
		t.Fatalf("Expected '(%d,%d)' but got '(%d,%d)'",
			expected_row, expected_col, row, col)
	}

	row, col = findEmptyPosition([][]byte{{1, 2, 3}, {4, 5, 6}, {'.', 8, 9}})
	expected_row, expected_col = 2, 0
	if row != expected_row || col != expected_col {
		t.Fatalf("Expected '(%d,%d)' but got '(%d,%d)'",
			expected_row, expected_col, row, col)
	}
}

func TestFindPossibleValues(t *testing.T) {
	grid, _ := readSudoku("puzzle1.txt")
	result := findPossibleValues(grid, 0, 2)
	expected_result := []byte{'1', '2', '4'}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}

	result = findPossibleValues(grid, 4, 7)
	expected_result = []byte{'2', '5', '9'}
	if !reflect.DeepEqual(result, expected_result) {
		t.Fatalf("Expected '%v' but got '%v'", expected_result, result)
	}
}

func TestSolve(t *testing.T) {
	grid, _ := readSudoku("puzzle1.txt")
	solution, _ := solve(grid)
	expected_solution, _ := readSudoku("puzzle1_solution.txt")
	if !reflect.DeepEqual(solution, expected_solution) {
		t.Fatalf("Expected '%v' but got '%v'", expected_solution, solution)
	}
}

func TestCheckSolution(t *testing.T) {
	// TODO: Add test for checkSolution
}

func TestGenerateSudoku(t *testing.T) {
	// TODO: Add test for generateSudoku
}
