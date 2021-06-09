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

    def get_card_by_rank_and_suit(self, rank, suit):
        """Returns a card object by its rank and suit

        Args:
            rank (Rank): rank of the card
            suit (Suit): suit of the card

        Returns:
            Card: the card or None if not found
        """
        for card in self.cards:
            if card.suit == suit and card.rank == rank:
                return card
        return None

    def shuffle(self):
        """Shuffle the cards in the deck
        """        
        random.shuffle(self.cards)
