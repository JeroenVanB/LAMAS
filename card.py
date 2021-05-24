from enum import Enum
class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.name = CardValue(self.rank).name + " of " + Suit(self.suit).name

    def evaluate(self, trump, trick_suit):
        if self.suit == trump:
            pass
        elif self.suit == trick_suit:
            pass
        else:
            return 0

class Suit(Enum):
    CLUB = 0
    DIAMOND = 1
    HEART = 2
    SPADE = 3

class CardValue(Enum):
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
