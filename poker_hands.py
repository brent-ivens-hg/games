from collections import Counter
from collections.abc import Sequence
from enum import Enum
from functools import cache
from random import sample

NAMES = 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace'
RANKS = '23456789TJQKA'
SUITS = 'SDCH'

RANK_VALUE = {rank: value for value, rank in enumerate(RANKS)}
SUIT_VALUE = {suit: value for value, suit in enumerate(SUITS)}

DECK = tuple(rank + suit for suit in SUITS for rank in RANKS[-1:] + RANKS[:-1])
NAME = dict(zip(RANKS, NAMES))


def get_card_value(card: str) -> tuple:
    return RANK_VALUE[card[0]], SUIT_VALUE[card[1]]


def get_card_name(card: str, plural: bool = False) -> str:
    return NAME[card[0]] + 's' * plural


class HandValue(Enum):
    HIGH_CARD = 'High Card'
    PAIR = 'Pair'
    TWO_PAIR = 'Two Pair'
    THREE_OF_A_KIND = 'Three of a Kind'
    STRAIGHT = 'Straight'
    FLUSH = 'Flush'
    FULL_HOUSE = 'Full House'
    FOUR_OF_A_KIND = 'Four of a Kind'
    STRAIGHT_FLUSH = 'Straight Flush'
    ROYAL_FLUSH = 'Royal Flush'

    def __str__(self) -> str:
        return self.value


class PokerHand:
    __slots__ = ('hand', 'ranks', 'suits', 'frequency', 'signature')

    def __init__(self, hand: Sequence[str]) -> None:
        assert len(hand) == 5, 'hand should consist of 5 cards'
        self.hand = tuple(sorted(hand, key=get_card_value))
        self.ranks, self.suits = zip(*self.hand)
        self.frequency = Counter(self.ranks)
        self.signature = Counter(self.frequency.values())

    @classmethod
    def random(cls, deck: Sequence[str] = DECK) -> 'PokerHand':
        assert len(deck) >= 5, 'deck should have at least 5 cards'
        return cls(sample(deck, k=5))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({list(self.hand)})'

    def __str__(self) -> str:
        return ' '.join(self.hand)

    @cache
    def is_royal_flush(self) -> bool:  # an Ace-High Straight Flush
        """
        Sequential Ranks Ten through Ace, Same Suit
        Probability: 4/2.598.960 ~ 0.00015%
        """
        return self.is_straight_flush() and set(self.ranks) == set('TJQKA')

    @cache
    def is_straight_flush(self) -> bool:
        """
        Sequential Ranks, Same Suit
        Probability: 40/2.598.960 ~ 0.0015%
        """
        return self.is_straight() and self.is_flush()

    @cache
    def is_four_of_a_kind(self) -> bool:
        """
        One Quadruplet, One kicker
        Probability: 624/2.598.960 ~ 0.024%
        """
        return self.signature == {1: 1, 4: 1}

    @cache
    def is_full_house(self) -> bool:
        """
        One Triplet, One Pair
        Probability: 3.744/2.598.960 ~ 0.14%
        """
        return self.signature == {2: 1, 3: 1}

    @cache
    def is_flush(self) -> bool:
        """
        Same Suit
        Probability: 5.108/2.598.960 ~ 0.20%
        """
        return len(set(self.suits)) == 1

    @cache
    def is_straight(self) -> bool:
        """
        Sequential Ranks
        Probability: __10__.200/2.598.960 ~ 0.39%
        """
        return ''.join(self.ranks) in RANKS or self.ranks == ('2', '3', '4', '5', 'A')

    @cache
    def is_three_of_a_kind(self) -> bool:
        """
        One Triplet, Two Kickers
        Probability: 54.912/2.598.960 ~ 2.11%
        """
        return self.signature == {1: 2, 3: 1}

    @cache
    def is_two_pair(self) -> bool:
        """
        Two Pairs, One Kicker
        Probability: 123.552/2.598.960 ~ 4.75%
        """
        return self.signature == {1: 1, 2: 2}

    @cache
    def is_pair(self) -> bool:
        """
        Pair, Three Kickers
        Probability: 1.098.240/2.598.960 ~ 42.26%
        """
        return self.signature == {1: 3, 2: 1}

    @cache
    def is_high_card(self) -> bool:
        """
        No Pair
        Probability: 1.302.540/2.598.960 ~ 50.12%
        """
        return self.signature == {1: 5} and not (self.is_flush() or self.is_straight())

    def hand_value(self) -> HandValue:
        if self.is_royal_flush():     return HandValue.ROYAL_FLUSH
        if self.is_straight_flush():  return HandValue.STRAIGHT_FLUSH
        if self.is_four_of_a_kind():  return HandValue.FOUR_OF_A_KIND
        if self.is_full_house():      return HandValue.FULL_HOUSE
        if self.is_flush():           return HandValue.FLUSH
        if self.is_straight():        return HandValue.STRAIGHT
        if self.is_three_of_a_kind(): return HandValue.THREE_OF_A_KIND
        if self.is_two_pair():        return HandValue.TWO_PAIR
        if self.is_pair():            return HandValue.PAIR
        return HandValue.HIGH_CARD

    def best_hand(self) -> str:
        match self.hand_value():
            case HandValue.ROYAL_FLUSH:
                return f'{HandValue.ROYAL_FLUSH!s}'

            case HandValue.STRAIGHT_FLUSH:
                if self.ranks == ('2', '3', '4', '5', 'A'):
                    return f'{get_card_name(self.hand[-2])}-High {HandValue.STRAIGHT_FLUSH!s}'
                return f'{get_card_name(self.hand[-1])}-High {HandValue.STRAIGHT_FLUSH!s}'

            case HandValue.FOUR_OF_A_KIND:
                card = next(str(rank) for rank in self.ranks if self.frequency[rank] == 4)
                return f'{HandValue.FOUR_OF_A_KIND!s}, {get_card_name(card, plural=True)}'

            case HandValue.FULL_HOUSE:
                first = next(str(rank) for rank in self.ranks if self.frequency[rank] == 3)
                second = next(str(rank) for rank in self.ranks if rank != first)
                return f'{HandValue.FULL_HOUSE!s}, {get_card_name(first, plural=True)} over {get_card_name(second, plural=True)}'

            case HandValue.FLUSH:
                return f'{get_card_name(self.hand[-1])}-High {HandValue.FLUSH!s}'

            case HandValue.STRAIGHT:
                if self.ranks == ('2', '3', '4', '5', 'A'):
                    return f'{get_card_name(self.hand[-2])}-High {HandValue.STRAIGHT!s}'
                return f'{get_card_name(self.hand[-1])}-High {HandValue.STRAIGHT!s}'

            case HandValue.THREE_OF_A_KIND:
                card = next(str(rank) for rank in self.ranks if self.frequency[rank] == 3)
                return f'{HandValue.THREE_OF_A_KIND!s}, {get_card_name(card, plural=True)}'

            case HandValue.TWO_PAIR:
                cards = iter(self.ranks)
                first = next(str(rank) for rank in cards if self.frequency[rank] == 2)
                second = next(str(rank) for rank in cards if rank != first and self.frequency[rank] == 2)
                return f'{HandValue.TWO_PAIR!s}, {get_card_name(first, plural=True)} and {get_card_name(second, plural=True)}'

            case HandValue.PAIR:
                card = next(str(rank) for rank in self.ranks if self.frequency[rank] == 2)
                return f'{HandValue.PAIR!s}, {get_card_name(card, plural=True)}'

            case HandValue.HIGH_CARD:
                return f'{HandValue.HIGH_CARD!s}, {get_card_name(self.hand[-1])}'

        raise AssertionError('unreachable code')

    def keyer(self) -> tuple:  # TODO: use enum : HandValue w/ match-case-statement
        ranks = self.ranks[::-1]  # high -> low
        # 1. Straight Flush
        if self.is_straight() and self.is_flush():
            # ranking, highest card-rank
            return 8, RANK_VALUE[ranks[0]]
        # 2. Four of a Kind
        if self.signature == {1: 1, 4: 1}:
            (quad, _), (kicker, _) = self.frequency.most_common() # TODO: reverse order of kickers
            # ranking, quadruplet rank, kicker rank
            return 7, RANK_VALUE[quad], RANK_VALUE[kicker]
        # 3. Full House
        if self.signature == {2: 1, 3: 1}:
            (trip, _), (pair, _) = self.frequency.most_common() # TODO: reverse order of kickers
            # ranking, triplet rank, pair rank
            return 6, RANK_VALUE[trip], RANK_VALUE[pair]
        # 4. Flush
        if self.is_flush():
            # ranking, highest card-rank
            return 5, RANK_VALUE[ranks[0]]
        # 5. Straight
        if self.is_straight():
            # ranking, highest card-rank
            return 4, RANK_VALUE[ranks[0]]
        # 6. Three Of A Kind
        if self.signature == {1: 2, 3: 1}:
            (trip, _), (kicker1, _), (kicker2, _) = self.frequency.most_common() # TODO: reverse order of kickers
            # ranking, triplet rank, kicker ranks (high -> low)
            return 3, RANK_VALUE[trip], RANK_VALUE[kicker1], RANK_VALUE[kicker2]
        # 7. Two Pair
        if self.signature == {1: 1, 2: 2}:
            (pair1, _), (pair2, _), (kicker, _) = self.frequency.most_common() # TODO: reverse order of kickers
            # ranking, pair ranks (high -> low), kicker rank
            return 2, RANK_VALUE[pair1], RANK_VALUE[pair2], RANK_VALUE[kicker]
        # 8. Pair
        if self.signature == {1: 3, 2: 1}:
            (pair, _), (kicker1, _), (kicker2, _), (kicker3, _) = self.frequency.most_common() # TODO: reverse order of kickers
            # ranking, pair rank, kicker ranks (high -> low)
            return 1, RANK_VALUE[pair], RANK_VALUE[kicker1], RANK_VALUE[kicker3]
        # 9. High Card
        # ranking, ranks (high -> low)
        return 0, *map(RANK_VALUE.get, ranks)


def doctest_poker_hand() -> None:
    """
    >>> from random import seed

    >>> seed(0)

    >>> PokerHand.random()
    PokerHand(['3S', '4D', 'TH', 'QD', 'AC'])
    >>> PokerHand.random(['4S', 'TD', '4H', '2H', '7H'])
    PokerHand(['2H', '4S', '4H', '7H', 'TD'])

    >>> PokerHand(('3H', '4S', '7S', 'QD', 'KD')).best_hand()
    'High Card, King'
    >>> PokerHand(('4D', '6S', 'TC', 'JS', 'JC')).best_hand()
    'Pair, Jacks'
    >>> PokerHand(('6S', '6D', 'TD', 'TH', 'KH')).best_hand()
    'Two Pair, Sixs and Tens'
    >>> PokerHand(('5S', '5C', '5H', '6S', 'QC')).best_hand()
    'Three of a Kind, Fives'
    >>> PokerHand(('AS', '2H', '3S', '4H', '5C')).best_hand()
    'Five-High Straight'
    >>> PokerHand(('AS', 'TH', 'JS', 'QH', 'KC')).best_hand()
    'Ace-High Straight'
    >>> PokerHand(('6S', '7H', '8S', '9H', 'TC')).best_hand()
    'Ten-High Straight'
    >>> PokerHand(('3C', '5C', '6C', '9C', 'QC')).best_hand()
    'Queen-High Flush'
    >>> PokerHand(('7S', '7D', 'AS', 'AC', 'AH')).best_hand()
    'Full House, Aces over Sevens'
    >>> PokerHand(('8S', '8D', '8C', '8H', 'KH')).best_hand()
    'Four of a Kind, Eights'
    >>> PokerHand(('4D', '5D', '6D', '7D', '8D')).best_hand()
    'Eight-High Straight Flush'
    >>> PokerHand(('AS', '2S', '3S', '4S', '5S')).best_hand()
    'Five-High Straight Flush'
    >>> PokerHand(('AH', 'TH', 'JH', 'QH', 'KH')).best_hand()
    'Royal Flush'
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
