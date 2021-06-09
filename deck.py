from card import Card, Suit, Rank
import random


class Deck:
    """An object that represents a deck of cards in the game
    """    
    def __init__(self, n_cards):
        """Initialize a new deck of cards

        Args:
            n_cards (int): The amount of cards each player receives
        """        
        self.cards = []
        self.reset_deck(n_cards)
        self.shuffle()

    def __init__(self):
        """Initialize an empty deck of cards
        """        
        self.cards = []

    def reset_deck(self, n_cards):
        """Reset the deck of cards

        Args:
            n_cards (int): The amount of cards each player receives
        """        
        self.cards = []
        self.n_cards = n_cards
        for c in range(self.n_cards):
            self.cards.append(Card(Rank(12 - c), Suit(0)))
            self.cards.append(Card(Rank(12 - c), Suit(1)))
            self.cards.append(Card(Rank(12 - c), Suit(2)))
            self.cards.append(Card(Rank(12 - c), Suit(3)))

    def shuffle(self):
        """Shuffle the cards in the deck
        """        
        random.shuffle(self.cards)
