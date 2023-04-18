import typing as tp

T = tp.TypeVar("T")

def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    temp_mini = []
    result = []
    while values:
        while len(temp_mini) < n:
            temp_mini.append(values.pop(0))

        result.append([i for i in temp_mini])
        temp_mini.clear()
    
    return result


def read_sudoku(path: str) -> tp.List[tp.List[str]]:
    file = open(path)
    values = [char for char in file.read() if char in '123456789.']
    file.close()
    grid = group(values, 9)
    return grid

grid = read_sudoku('puzzle1.txt')

def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()

display(grid)


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return [i[pos[1]] for i in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    temp = []
    row_block = pos[0] // 3
    col_block = pos[1] // 3
    for i in range(9):
        temp.extend(grid[row_block * 3 + i // 3][col_block * 3 + i % 3])

    return temp

    
def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    for i in range(len(grid)): 
        if '.' in grid[i]:
            return (i, grid[i].index('.'))
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    res = set()
    if grid[pos[0]][pos[1]] != '.':
        return res
    
    for i in range(1, 10):
        if str(i) in get_row(grid, (pos[0], pos[1])) or str(i) in get_col(grid, (pos[0], pos[1])) or str(i) in get_block(grid, (pos[0], pos[1])):
            continue
        res.add(str(i))

    return res


# def sudoku_helper(grid: tp.List[tp.List[str]], val: str) -> bool:


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    empty_pos = find_empty_positions(grid)
    if empty_pos is None:
        return grid
    row, col = empty_pos
    
    for val in find_possible_values(grid, empty_pos):
        grid[row][col] = val
        solved_sudoku = solve(grid)
        if solved_sudoku is not None: 
            return solved_sudoku
        grid[row][col] = '.'
    
    return None
    
solution = solve(grid)
print('Solution: ')
display(solution)