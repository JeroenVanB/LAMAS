from enum import IntEnum


class Card:
    """An object that represents a card in the game"""

    def __init__(self, rank, suit):
        """Initialize a Card object

        Args:
            rank (Rank): The rank of a card
            suit (Suit): The suit of the card
        """
        self.rank = rank
        self.suit = suit
        self.name = Rank(self.rank).name + " of " + Suit(self.suit).name
        self.played_value = 0
        self.owner = None

    def evaluate(self, trump, trick_suit):
        """Evaluate the value of a card, determined by rank and suit of the card (influenced by the trump and the trick_suit)

        Args:
            trump (Suit): The trump suit of the round
            trick_suit (Suit): The trick suit

        Returns:
            int: The value of the card
        """
        if self.suit == trump:
            self.played_value = self.rank.value + 26
        elif trick_suit is not None and self.suit == trick_suit:
            self.played_value = self.rank.value + 13
        else:
            self.played_value = self.rank.value
        return self.played_value

    def pre_evaluate(self, trump):
        """Evaluatate the value of a card at the start of the game (there is not trick suit yet)

        Args:
            trump (Suit): The trick suit
        """        
        if self.suit == trump:
            self.played_value = self.rank.value + 13
        else:
            self.played_value = self.rank.value
        return self.played_value
        
    def set_owner(self, player):
        """Set the owner of the card

        Args:
            player (Player): The player that owns the card
        """
        self.owner = player

    def __str__(self) -> str:
        return self.name


class Suit(IntEnum):
    """Enumeration of the four possible suits of a deck of cards."""

    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3


class Rank(IntEnum):
    """Enumeration of the different ranks of cards in a deck of cards. The integer represents the base value of the card."""

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
