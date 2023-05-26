from random import sample, seed

# seed('blackjack')

RANKS = 'A23456789TJQK'
SUITS = 'SDCH'
CARDS = [r + s for s in SUITS for r in RANKS]


def deck(shuffled=False):
    cards = CARDS.copy()
    return sample(cards, 52) if shuffled else cards


class Blackjack:
    def __init__(self):
        self.reset()

    def __str__(self):
        return r''' _______________________________________________________________________________________
/    __        __                      __                                    __         |
$$  /  |      /  |                    /  |                                  /  |        |
$$  $$ |____  $$ |  ______    _______ $$ |   __      __   ______    _______ $$ |   __   |
$$  $$      \ $$ | /      \  /       |$$ |  /  |    /  | /      \  /       |$$ |  /  |  |
$$  $$$$$$$  |$$ | $$$$$$  |/$$$$$$$/ $$ |_/$$/     $$/  $$$$$$  |/$$$$$$$/ $$ |_/$$/   |
$$  $$ |  $$ |$$ | /    $$ |$$ |      $$   $$<      /  | /    $$ |$$ |      $$   $$<    |
$$  $$ |__$$ |$$ |/$$$$$$$ |$$ \_____ $$$$$$  \     $$ |/$$$$$$$ |$$ \_____ $$$$$$  \   |
$$  $$    $$/ $$ |$$    $$ |$$       |$$ | $$  |    $$ |$$    $$ |$$       |$$ | $$  |  |
$$  $$$$$$$/  $$/  $$$$$$$/  $$$$$$$/ $$/   $$/__   $$ | $$$$$$$/  $$$$$$$/ $$/   $$/   |
$$                                            /  \__$$ |                                |
$$                                            $$    $$/                                 |
$$                                             $$$$$$/                                  |
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$/
'''

    @staticmethod
    def calc_value(cards):
        aces = value = 0
        for card in cards:
            c = card[0]
            if c in 'TJQK':
                value += 10
            elif c != 'A':
                value += int(c)
            else:
                aces += 1; value += 11
        while aces and value > 21: aces -= 1; value -= 10
        return value

    def deal(self):
        """ deal a card to the player """
        card = next(self.cards)
        return self.player.append(card)

    def pull(self):
        """ pull a card from the deck """
        card = next(self.cards)
        return self.dealer.append(card)

    def print(self, text='', assist=False):
        """ prints cards, shows dealer's hand """
        if assist:
            print('Dealer: %s (%d)\nPlayer: %s (%d)' % (
                ' '.join(self.dealer), self.dealer_val,
                ' '.join(self.player), self.player_val))
        else:
            print('Dealer: %s\nPlayer: %s' % (' '.join(self.dealer), ' '.join(self.player)))
        if text: print(text)

    def print_hidden(self, assist=False):
        """ prints cards, hides dealer's hand """
        upcards = self.dealer[1:]
        if assist:
            print('Dealer: XX %s (%d*)\nPlayer: %s (%d)' % (
                ' '.join(upcards), self.calc_value(upcards),
                ' '.join(self.player), self.player_val))
        else:
            print('Dealer: XX %s\nPlayer: %s' % (' '.join(upcards), ' '.join(self.player)))

    def reset(self):
        """ reset attributes """
        self.player_val = self.dealer_val = 0
        self.dealer, self.player = [], []
        self.cards = iter(deck(shuffled=True))

    def update_dealer(self):
        """ updates the dealer value """
        self.dealer_val = self.calc_value(self.dealer)

    def update_player(self):
        """ updates the player value """
        self.player_val = self.calc_value(self.player)

    def play(self, assist=False):
        """
         simulates blackjack game:
         :param assist: card value assist
        """
        # TODO: betting / doubling / splitting / insurance
        print(self)
        while 1:
            # setup
            self.deal(), self.pull(), self.deal(), self.pull()
            self.update_player(), self.update_dealer()
            # no turns
            if self.player_val == self.dealer_val == 21:
                self.print(text='Push!', assist=assist)
            elif self.dealer_val == 21:
                self.print(text='Dealer Blackjack!', assist=assist)
            elif self.player_val == 21:
                self.print(text='Blackjack!', assist=assist)
            # turns
            else:
                # player's turn
                while self.player_val < 21:
                    self.print_hidden(assist=assist)
                    inp = input('[HIT][STAND] ').lower()
                    if inp in {'s', 'stand', 'o'}: break
                    if inp in {'h', 'hit', 'x'}:
                        self.deal(), self.update_player()
                    else:
                        print('Invalid command, try [X][O]')

                if self.player_val > 21:
                    self.print(text='Busted!', assist=assist)
                else:
                    # dealer's turn
                    while 17 > self.dealer_val <= self.player_val: self.pull(), self.update_dealer()
                    self.print(text='Push!' if self.player_val == self.dealer_val else
                    'You Lost…' if self.player_val < self.dealer_val <= 21 else
                    'You Won!', assist=assist)
            self.reset()
            inp = input('[RETRY] ').lower()
            if inp not in {'y', 'yes', 'r', 'retry', 'x'}: break


Blackjack().play(assist=True)
