"""
Tectonic
"""
from collections import defaultdict
from heapq import heappop, heappush, heapify


def grouper(grid: list) -> list[list]:
    res = defaultdict(list)
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            res[col].append((r, c))
    return list(res.values())


class TecTonic:
    def __init__(self, grid: list[list], groups: list[list]) -> None:
        self.grid = grid
        self.n = len(grid)
        self.groups = groups

    def __str__(self) -> str:
        return '\n'.join('  '.join(str(col) if col else ' ' for col in row) for row in self.grid)

    def __contains__(self, position: tuple) -> bool:
        row, col = position
        return 0 <= row < self.n and 0 <= col < self.n

    def adjacent(self, row: int, col: int) -> set[int]:
        return {self.grid[row + r][col + c]
                for r, c in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
                if (row + r, col + c) in self}

    def is_valid(self, value: int, row: int, col: int, group: list) -> bool:
        return ((row, col) in self  # if within bounds
                and self.grid[row][col] == 0  # if empty
                and value not in self.adjacent(row, col)  # check adjacent
                and all(value != self.grid[r][c] for r, c in group))  # check group

    def solve(self) -> None:
        queue = self.groups
        heapify(queue)
        while queue:
            break


print(TecTonic(
    [
        [3, 0, 0, 0, 3, 0, 2, 0, 0],
        [0, 0, 1, 0, 0, 4, 0, 0, 4],
        [2, 0, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0],
        [0, 5, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2],
        [4, 0, 0, 0, 2, 5, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 4],
        [3, 0, 0, 0, 0, 0, 0, 2, 0]
    ],
    grouper('AABBCCCDD AABBBCCDD AEEFFGHHH EEEFFGGHH IIIIJGGKK LLIJJMMKK LLLJJMMMK NNOOOOPPP NNNOQQPPR'.split())
))

print(grouper('AABBCCCDD AABBBCCDD AEEFFGHHH EEEFFGGHH IIIIJGGKK LLIJJMMKK LLLJJMMMK NNOOOOPPP NNNOQQPPR'.split()))

if __name__ == '__main__':
    import doctest

    doctest.testmod()
