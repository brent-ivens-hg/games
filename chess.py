"""
Chess
"""
GRAPHICAL_PIECE = 'PpNnBbRrQqKk-'
NAME_PIECE = ['white pawn', 'black pawn', 'white knight', 'black knight', 'white bishop', 'black bishop',
              'white rook', 'black rook', 'white queen', 'black queen', 'white king', 'black king', 'none']


# double move
# en-peasant
# castling


class Board:
    OFFSETS = [8, -8,  # up-down
               1, -1,  # left-right
               7, -7,  # diagonal 1
               9, -9]  # diagonal 2

    def __init__(self) -> None:
        self.square: list[int] = []
        self.has_moved: list[int] = []

        self.is_white = True
        self.reset()

        self.white_occupied = set()
        self.black_occupied = set()

    def occupied(self):
        return self.white_occupied | self.black_occupied

    def is_occupied(self, i: int) -> bool:
        return i in self.occupied()

    def reset(self) -> None:
        self.has_moved = [0] * 64
        self.square = [
            6, 2, 4, 8, 10, 4, 2, 6,
            0, 0, 0, 0, 0, 0, 0, 0,
            -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1, -1,
            1, 1, 1, 1, 1, 1, 1, 1,
            7, 3, 5, 9, 11, 5, 3, 7,
        ]
        self.white_occupied = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
        self.black_occupied = {48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63}

    def __str__(self) -> str:
        view = reversed if self.is_white else iter  # mirror horizontally
        return '\n'.join(' '.join(GRAPHICAL_PIECE[self.square[8 * rank + file]]
                                  for file in range(8)) for rank in view(range(8)))


game = Board()
print(game)

if __name__ == '__main__':
    import doctest

    doctest.testmod()
