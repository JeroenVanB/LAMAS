import time
from typing import List
from card import Card, Suit
from seat import Seat
import copy


class KnowledgeBase:
    def __init__(self, player, all_cards: List[Card], own_cards: List[Card]) -> None:
        self.all_cards = [c for c in all_cards]
        # self.all_cards = copy.deepcopy(all_cards)  # all cards in the game
        self.player = player
        # self.own_cards = copy.deepcopy(own_cards)  # cards of the player
        self.own_cards = [c for c in own_cards]
        self.knowledge = {}
        self.game_model = None
        for c in self.all_cards:
            k = {
                Seat.NORTH: False,
                Seat.EAST: False,
                Seat.SOUTH: False,
                Seat.WEST: False,
            }
            self.knowledge[c] = k
        self.set_knowledge_of_remaining_cards_in_deck()
        self.set_knowledge_of_own_hand()

    def set_game_model(self, game_model):
        self.game_model = game_model

    def set_card_knowledge(self, card: Card, player):
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
        k = {
            Seat.NORTH: False,
            Seat.EAST: False,
            Seat.SOUTH: False,
            Seat.WEST: False,
        }
        k[player.seat] = True
        self.knowledge[card] = k

    def get_card_knowledge(self, card):
        """Returns the knowledge of a card

        Args:
            card (Card): The card

        Returns:
            knowledge: if card is found else None
        """
        for c, knowledge in self.knowledge.items():
            if c.name == card.name:
                return knowledge
        return None

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
        idx = -1
        for idx, c in enumerate(self.all_cards):
            if c == card:
                break
        if idx != -1:
            del self.all_cards[idx]
        else:
            raise Exception("Card is no part of the KB so I cannot remove it.")
        self.knowledge.pop(card)

    def set_all_cards_of_suit_of_player(self, suit: Suit, player, value: bool):
        """Sets the value for all cards from a suit of a player

        Args:
            suit (Suit): The suit of the cards
            player (Player): The player
            value (bool): Truth value
        """
        for (card, seats) in self.knowledge.items():
            if card.suit == suit:
                seats[player.seat] = value

    def get_highest_card_of_suit(self, suit: Suit):
        """Getting the highest card of suit in the game.

        Args:
            suit (Suit): the suit
        """
        assert len(self.all_cards) > 0
        highest_value = -1
        highest_card = None
        for card in self.all_cards:
            if card.suit == suit:
                card.evaluate(self.game_model.trump, self.game_model.trick_suit)
                value = card.played_value
                if value > highest_value:
                    highest_value = value
                    highest_card = card
        return highest_card

    def get_highest_non_trump_card(self):
        """Get the highest card still in the game (non-trump)

        Returns:
            Card : highest non trump card in the game
        """
        highest_card = None
        highest_value = -1
        for suit in Suit:
            if suit == self.game_model.trump:
                continue
            card = self.get_highest_card_of_suit(suit)
            if card is not None:
                val = card.evaluate(self.game_model.trump, None)
                if val > highest_value:
                    highest_value = val
                    highest_card = card
        return highest_card

    def other_players_have_suit(self, suit: Suit):
        """Checks if there are other players with suit

        Args:
            suit (Suit): the suit to check

        Returns:
            bool: whether there is another player that has the suit
        """
        # get all players except the current player
        players = [
            player for player in self.game_model.players if player is not self.player
        ]
        for player in players:
            if self.player_might_have_suit(player, suit):
                return True
        return False

    def player_might_have_suit(self, player: list, suit: Suit):
        for card in self.all_cards:
            if card.suit == suit and card.owner == player:
                return True
        return False
