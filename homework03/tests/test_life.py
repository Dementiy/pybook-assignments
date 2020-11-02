import json
import os
import random
import unittest

import life


class TestGameOfLife(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [1, 1, 0, 0, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [1, 0, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1],
        ]
        self.rows = 6
        self.cols = 8
        self.max_generations = 18

    def test_can_create_an_empty_grid(self):
        game = life.GameOfLife((3, 3))
        grid = game.create_grid(randomize=False)
        self.assertEqual([[0, 0, 0], [0, 0, 0], [0, 0, 0]], grid)

    def test_can_create_a_random_grid(self):
        game = life.GameOfLife((3, 3))
        random.seed(12345)
        grid = game.create_grid(randomize=True)
        self.assertEqual([[1, 0, 1], [1, 0, 1], [1, 0, 1]], grid)

    def test_get_neighbours(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid
        neighbours = game.get_neighbours((2, 3))
        self.assertEqual(8, len(neighbours))
        self.assertEqual(4, sum(neighbours))

    def test_get_neighbours_for_upper_left_corner(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid
        neighbours = game.get_neighbours((0, 0))
        self.assertEqual(3, len(neighbours))
        self.assertEqual(2, sum(neighbours))

    def test_get_neighbours_for_upper_right_corner(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid
        neighbours = game.get_neighbours((0, 7))
        self.assertEqual(3, len(neighbours))
        self.assertEqual(2, sum(neighbours))

    def test_get_neighbours_for_lower_left_corner(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid
        neighbours = game.get_neighbours((5, 0))
        self.assertEqual(3, len(neighbours))
        self.assertEqual(2, sum(neighbours))

    def test_get_neighbours_for_lower_right_corner(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid
        neighbours = game.get_neighbours((5, 7))
        self.assertEqual(3, len(neighbours))
        self.assertEqual(1, sum(neighbours))

    def test_get_neighbours_for_upper_side(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid
        neighbours = game.get_neighbours((0, 3))
        self.assertEqual(5, len(neighbours))
        self.assertEqual(4, sum(neighbours))

    def test_get_neighbours_for_bottom_side(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid
        neighbours = game.get_neighbours((5, 3))
        self.assertEqual(5, len(neighbours))
        self.assertEqual(4, sum(neighbours))

    def test_get_neighbours_for_left_side(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid
        neighbours = game.get_neighbours((2, 0))
        self.assertEqual(5, len(neighbours))
        self.assertEqual(2, sum(neighbours))

    def test_get_neighbours_for_right_side(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid
        neighbours = game.get_neighbours((2, 7))
        self.assertEqual(5, len(neighbours))
        self.assertEqual(2, sum(neighbours))

    def test_can_update(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid

        tests_dir = os.path.dirname(__file__)
        steps_path = os.path.join(tests_dir, "steps.txt")
        with open(steps_path) as f:
            steps = json.load(f)

        num_updates = 0
        for step in sorted(steps.keys(), key=int):
            with self.subTest(step=step):
                for _ in range(int(step) - num_updates):
                    game.curr_generation = game.get_next_generation()
                    num_updates += 1
                self.assertEqual(steps[step], game.curr_generation)

    def test_prev_generation_is_correct(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid
        game.step()
        self.assertEqual(game.prev_generation, self.grid)

    def test_is_max_generations_exceeded(self):
        max_generations = 4
        game = life.GameOfLife((self.rows, self.cols), max_generations=max_generations)
        game.curr_generation = self.grid
        for _ in range(max_generations - 1):
            game.step()
        self.assertEqual(game.generations, max_generations)
        self.assertTrue(game.is_max_generations_exceeded)

    def test_is_changing(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid
        game.step()
        self.assertTrue(game.is_changing)

    def test_is_not_changing(self):
        game = life.GameOfLife((self.rows, self.cols))
        game.curr_generation = self.grid
        for _ in range(self.max_generations + 1):
            game.step()
        self.assertFalse(game.is_changing)
