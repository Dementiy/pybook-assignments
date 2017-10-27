import unittest
import random
import json

from life_with_classes import Cell, CellList


class TestCell(unittest.TestCase):

    def test_can_create_a_cell(self):
        cell = Cell(0, 0)
        self.assertFalse(cell.is_alive())

    def test_can_create_a_cell(self):
        cell = Cell(0, 0, state=True)
        self.assertTrue(cell.is_alive())


class TestCellList(unittest.TestCase):

    def setUp(self):
        pass

    def test_clist_is_iterable(self):
        clist = CellList(nrows=3, ncols=3, randomize=False)
        raised = False
        try:
            it = iter(clist)
        except TypeError:
            raised = True
        self.assertFalse(raised, 'Iterator protocol is not implemented')

    def test_can_iterate_over_clist(self):
        clist = CellList(nrows=3, ncols=3, randomize=True)
        raised = False
        try:
            n = 9
            it = iter(clist)
            while n:
                self.assertIsInstance(next(it), Cell)
                n -= 1
        except StopIteration:
            raised = True
        self.assertFalse(raised, 'Cannot iterate over the cell list')

    def test_can_create_an_empty_grid(self):
        clist = CellList(nrows=3, ncols=3, randomize=False)
        states = [cell.is_alive() for cell in clist]
        self.assertEqual([0,0,0,0,0,0,0,0,0], states)

    def test_can_create_a_random_grid(self):
        random.seed(12345)
        clist = CellList(nrows=3, ncols=3, randomize=True)
        states = [cell.is_alive() for cell in clist]
        self.assertEqual([1,0,1,1,0,1,1,0,1], states)

    def test_can_create_a_grid_from_file(self):
        clist = CellList.from_file('grid.txt')
        states = [cell.is_alive() for cell in clist]
        self.assertEqual(6, clist.nrows)
        self.assertEqual(8, clist.ncols)
        self.assertEqual(29, sum(states))

    def test_get_neighbours(self):
        clist = CellList.from_file('grid.txt')
        neighbours = clist.get_neighbours(Cell(2,3))
        self.assertEquals(8, len(neighbours))
        self.assertEquals(4, sum(c.is_alive() for c in neighbours))

    def test_get_neighbours_for_upper_left_corner(self):
        clist = CellList.from_file('grid.txt')
        neighbours = clist.get_neighbours(Cell(0,0))
        self.assertEquals(3, len(neighbours))
        self.assertEquals(2, sum(c.is_alive() for c in neighbours))

    def test_get_neighbours_for_upper_right_corner(self):
        clist = CellList.from_file('grid.txt')
        neighbours = clist.get_neighbours(Cell(0,7))
        self.assertEquals(3, len(neighbours))
        self.assertEquals(2, sum(c.is_alive() for c in neighbours))

    def test_get_neighbours_for_lower_left_corner(self):
        clist = CellList.from_file('grid.txt')
        neighbours = clist.get_neighbours(Cell(5,0))
        self.assertEquals(3, len(neighbours))
        self.assertEquals(2, sum(c.is_alive() for c in neighbours))

    def test_get_neighbours_for_lower_right_corner(self):
        clist = CellList.from_file('grid.txt')
        neighbours = clist.get_neighbours(Cell(5,7))
        self.assertEquals(3, len(neighbours))
        self.assertEquals(1, sum(c.is_alive() for c in neighbours))

    def test_get_neighbours_for_upper_side(self):
        clist = CellList.from_file('grid.txt')
        neighbours = clist.get_neighbours(Cell(0,3))
        self.assertEquals(5, len(neighbours))
        self.assertEquals(4, sum(c.is_alive() for c in neighbours))

    def test_get_neighbours_for_bottom_side(self):
        clist = CellList.from_file('grid.txt')
        neighbours = clist.get_neighbours(Cell(5,3))
        self.assertEquals(5, len(neighbours))
        self.assertEquals(4, sum(c.is_alive() for c in neighbours))

    def test_get_neighbours_for_left_side(self):
        clist = CellList.from_file('grid.txt')
        neighbours = clist.get_neighbours(Cell(2,0))
        self.assertEquals(5, len(neighbours))
        self.assertEquals(2, sum(c.is_alive() for c in neighbours))

    def test_get_neighbours_for_right_side(self):
        clist = CellList.from_file('grid.txt')
        neighbours = clist.get_neighbours(Cell(2,7))
        self.assertEquals(5, len(neighbours))
        self.assertEquals(2, sum(c.is_alive() for c in neighbours))

    def test_can_update(self):
        clist = CellList.from_file('grid.txt')

        with open('steps.txt') as f:
            steps = json.load(f)

        num_updates = 0
        for step in sorted(steps.keys(), key=int):
            with self.subTest(step=step):
                for _ in range(int(step)-num_updates):
                    clist = clist.update()
                    num_updates += 1
                # TODO: Rewrite me
                c = 0
                row = []
                states = []
                for cell in clist:
                    row.append(int(cell.is_alive()))
                    c += 1
                    if c % clist.ncols == 0:
                        states.append(row)
                        row = []
                self.assertEqual(steps[step], states)


loader = unittest.TestLoader()
suite = loader.loadTestsFromTestCase(TestCell)
suite.addTests(loader.loadTestsFromTestCase(TestCellList))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
