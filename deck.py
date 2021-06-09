from card import Card, Suit, CardValue
import random


class Deck:
    def __init__(self, n_cards):
        self.cards = []
        self.reset_deck(n_cards)
        self.shuffle()

    def __init__(self):
        self.cards = []

    def reset_deck(self, n_cards):
        self.cards = []
        for c in range(n_cards):
            self.cards.append(Card(CardValue(12 - c), Suit(0)))
            self.cards.append(Card(CardValue(12 - c), Suit(1)))
            self.cards.append(Card(CardValue(12 - c), Suit(2)))
            self.cards.append(Card(CardValue(12 - c), Suit(3)))

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
        random.shuffle(self.cards)
