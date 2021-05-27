from enum import Enum, IntEnum


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.name = CardValue(self.rank).name + " of " + Suit(self.suit).name
        self.played_value = 0
        self.owner = None

    def evaluate(self, trump, trick_suit):
        if self.suit == trump:
            self.played_value = self.rank.value + 13
        elif self.suit == trick_suit:
            self.played_value = self.rank.value
        else:
            self.played_value = 0

    def __str__(self) -> str:
        return self.name


class Suit(IntEnum):
    CLUB = 0
    DIAMOND = 1
    HEART = 2
    SPADE = 3


class CardValue(IntEnum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12
