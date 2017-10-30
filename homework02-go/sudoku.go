package main

import (
	"fmt"
	"io/ioutil"
	"path/filepath"
)

func readSudoku(filename string) ([][]byte, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	grid := group(filter(data), 9)
	return grid, nil
}

func filter(values []byte) []byte {
	filtered_values := make([]byte, 0)
	for _, v := range values {
		if (v >= '1' && v <= '9') || v == '.' {
			filtered_values = append(filtered_values, v)
		}
	}
	return filtered_values
}

func display(grid [][]byte) {
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid); j++ {
			fmt.Print(string(grid[i][j]))
		}
		fmt.Println()
	}
}

func group(values []byte, n int) [][]byte {
	// PUT YOUR CODE HERE
}

func getRow(grid [][]byte, row int) []byte {
	// PUT YOUR CODE HERE
}

func getCol(grid [][]byte, col int) []byte {
	// PUT YOUR CODE HERE
}

func getBlock(grid [][]byte, row int, col int) []byte {
	// PUT YOUR CODE HERE
}

func findEmptyPosition(grid [][]byte) (int, int) {
	// PUT YOUR CODE HERE
}

func contains(values []byte, search byte) bool {
	for _, v := range values {
		if v == search {
			return true
		}
	}
	return false
}

func findPossibleValues(grid [][]byte, row int, col int) []byte {
	// PUT YOUR CODE HERE
}

func solve(grid [][]byte) ([][]byte, bool) {
	// PUT YOUR CODE HERE
}

func checkSolution(grid [][]byte) bool {
	// PUT YOUR CODE HERE
}

func generateSudoku(N int) [][]byte {
	// PUT YOUR CODE HERE
}

func main() {
	puzzles, err := filepath.Glob("puzzle*.txt")
	if err != nil {
		fmt.Printf("Could not find any puzzles")
		return
	}
	for _, fname := range puzzles {
		go func(fname string) {
			grid, _ := readSudoku(fname)
			solution, _ := solve(grid)
			fmt.Println("Solution for", fname)
			display(solution)
		}(fname)
	}
	var input string
	fmt.Scanln(&input)
}
