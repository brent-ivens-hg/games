# noinspection PyAttributeOutsideInit
class TicTacToe:
    has_3 = staticmethod(lambda S: bool({'XXX', 'OOO'} & S))

    def __init__(self):
        self.scores = [0, 0]
        self.round = 1
        self.reset()

    def __str__(self):
        return '\n'.join(map(' '.join, self.grid))

    @property
    def mark(self):
        return 'O' if self.player else 'X'

    def place(self, placement):
        assert not self.game_over(), 'game is over'
        placement -= 1
        r, c = divmod(placement, 3)
        assert 0 <= placement < 9 and self.grid[r][c] == '_', 'invalid placement'

        self.grid[r][c] = self.mark
        if self.is_won():
            self.scores[self.player] += 1
        else:
            self.turn += 1
            self.player ^= 1

    def reset(self):
        self.player = self.turn = 0
        self._is_won = False
        self.grid = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

    def is_won(self):
        if not self._is_won and self.turn < 9:
            self._is_won = (
                    self.has_3(set(map(''.join, self.grid))) or
                    self.has_3(set(map(''.join, zip(*self.grid)))) or
                    self.has_3(set(map(''.join, (
                        (self.grid[i][i] for i in range(3)), (self.grid[2 - i][i] for i in range(3))))))
            )
        return self._is_won

    def game_over(self):
        return self.is_won() or self.turn == 9

    def rematch(self):
        assert self.game_over()
        self.round += 1
        self.reset()

    def play(self):
        print('The board is numbered with the nine positions as follows\n1 2 3\n4 5 6\n7 8 9')
        while 1:
            print(f'\nROUND {self.round}:\n{self}')

            while not self.game_over():
                inp = input(f'\n{self.mark}\'s turn\n[1-9]? ')
                if inp.lower() == 'stop': return 1
                try:
                    self.place(int(inp))
                    print(self)
                except (AssertionError, ValueError):
                    print(f'Unable to place at "{inp}". Try again.')

            print('\n{} Won\nStandings: X: {} - O: {}\n'.format(self.mark, *self.scores))
            while (inp := input('Rematch [y/n]? ').lower()) not in {'y', 'yes', 'n', 'no', 'stop'}: pass
            if inp == 'stop': return 1
            if inp in 'no': return 0
            self.rematch()


TicTacToe().play()
