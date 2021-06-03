from typing import List
from card import Card, Suit
from seat import Seat

class KnowledgeBase:
    def __init__(
        self, player, all_cards: List[Card], own_cards: List[Card]
    ) -> None:
        self.all_cards = all_cards
        self.player = player
        self.own_cards = own_cards
        self.knowledge = {}
        for c in own_cards:
            k = {
                Seat.NORTH: False,
                Seat.EAST: False,
                Seat.SOUTH: False,
                Seat.WEST: False,
            }
            self.knowledge[c] = k

    def set_card_knowledge(self, card: Card, player, value: bool):
        """Set the knowledge value for an individual card and player

        Args:
            card (Card): the card
            player (Player): the player
            value (bool): If the player could have the card or not

        Raises:
            Exception: raised if the card is not part of the KB.
        """
        if not card in self.knowledge:
            raise Exception(
                "Trying to change knowledge of a card that is not in the knowledge base"
            )
        self.knowledge[card][player.seat] = value

    def set_knowledge_of_remaining_cards_in_deck(self):
        """Cards not in the players hand can be in any other players hand."""
        for card in self.all_cards:
            if card not in self.own_cards:

                k = {
                    Seat.NORTH: True,
                    Seat.EAST: True,
                    Seat.SOUTH: True,
                    Seat.WEST: True,
                }
                k[self.player.seat] = False
                self.knowledge[card] = k

    def set_knowledge_of_own_hand(self):
        """A player has knowledges of the cards in its hand and thus knows that
        no other player can have these cards
        """
        k = {
            Seat.NORTH: False,
            Seat.EAST: False,
            Seat.SOUTH: False,
            Seat.WEST: False,
        }
        k[self.player.seat] = True
        for card in self.own_cards:
            self.knowledge[card] = k

    def remove_card(self, card: Card):
        """Removes a card from the kb since it has been played and is out of the game.
        Args:
            card (Card): The card that has been played
        """
        self.knowledge.pop(card)

    def set_all_cards_of_suit_of_player(self, suit: Suit, player, value: bool):
        """Sets the value for all cards from a suit of a player

        Args:
            suit (Suit): The suit of the cards
            player (Player): The player
            value (bool): Truth value 
        """
        for (card, seats) in self.knowledge:
            if card.suit == suit:
                seats[player.seat] = value
        