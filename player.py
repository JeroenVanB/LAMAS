from knowledge_base import KnowledgeBase
from card import Card, Suit
from enum import Enum
import random
from public_announcement import AnnouncementType, PublicAnnouncement
from seat import Seat


class Player:
    def __init__(self, seat_number, seat: Seat):
        self.seat = seat
        self.cards = []
        self.all_cards = []
        self.name = Seat(seat_number).name
        self.score = 0
        self.game_model = None

        self.wins = 0
        self.guessed_wins = 0
        self.opener = self.seat == Seat.NORTH

    def set_game_model(self, game_model):
        self.game_model = game_model

    def set_cards(self, cards):
        self.cards = cards
        for c in self.cards:
            c.set_owner(self)

    def set_all_cards(self, cards):
        self.all_cards = cards

    def guess_wins(self, trump, n_cards):
        self.guessed_wins = random.randint(0, n_cards)

    def change_guess(self, n_cards):
        x = random.randint(0, n_cards)
        if x == self.guessed_wins:
            self.change_guess(n_cards)
        else:
            self.guessed_wins = x

    def reset(self):
        self.wins = 0
        self.guessed_wins = 0

    def calculate_score(self):
        if self.wins == self.guessed_wins:
            self.score += self.wins * 2 + 10
        else:
            self.score += abs(self.wins - self.guessed_wins) * -2

    def add_win(self):
        self.wins += 1

    def play_card(self) -> Card:
        card = self.pick_card()
        self.cards.remove(card)
        self.game_model.make_announcement(self, card, AnnouncementType.card_played)
        return card

    def pick_card(self) -> Card:
        """Pick a card based on a tactic

        Raises:
            NotImplementedError: Should be implemented by subclass

        Returns:
            Card: chosen card
        """
        # Subclasses should override this method
        raise NotImplementedError

    def get_cards_of_suit(self, suit: Suit) -> list:
        """Get the player's cards of a given suit

        Args:
            suit (Suit): The suit of the card

        Returns:
            List: List of the cards of the given suit
        """
        return [c for c in self.cards if c.suit == suit]

    def get_trump_cards(self) -> list:
        """Pick the player's trump cards

        Args:
            possible_cards (list): Possible cards

        Returns:
            List: List of possible trump cards
        """
        return [card for card in self.cards if card.suit == self.game_model.trump]

    def get_lowest_card_of_trick_suit(self):
        """Getting the lowest card that the player holds of the trick suit

        Returns:
            Card: the lowest card of the trick suit
        """
        return self.get_lowest_cards_of_suit(self.game_model.trick_suit)

    def get_highest_card(self, possible_cards):
        """Getting the highest evaluated card from a list of cards

        Args:
            possible_cards (list): list of cards

        Returns:
            Card: the highest cards
        """
        assert len(possible_cards) > 0
        highest_value = -1
        highest_cards = []
        for card in possible_cards:
            card.evaluate(self.game_model.trump, self.game_model.trick_suit)
            eval = card.played_value
            if eval > highest_value:
                highest_value = eval
                highest_cards = [card]
            elif eval == highest_value:
                highest_cards.append(card)
        return random.choice(highest_cards)

    def has_trump_cards(self):
        """Whether the player has a trump card

        Returns:
            bool: Has trump card
        """
        for card in self.cards:
            if card.suit == self.game_model.trump:
                return True
        return False

    def get_lowest_cards_of_suit(self, suit):
        """Gets the lowest ranked card of a given suit

        Args:
            suit (Suit): the suit

        Returns:
            Card: The lowest ranked card
        """
        suit_cards = self.get_cards_of_suit(suit)
        lowest_value = 999
        lowest_card = None
        for card in suit_cards:
            card.evaluate(self.game_model.trump, self.game_model.trick_suit)
            value = card.played_value
            if value < lowest_value:
                lowest_value = value
                lowest_card = card
        return lowest_card

    def get_lowest_card(self):
        """Get the card with the lowest value of all cards

        Returns:
            Card: Card with lowest value
        """
        lowest_value = 999
        lowest_card = None
        for suit in Suit:
            c = self.get_lowest_cards_of_suit(suit)
            if c is not None and c.played_value < lowest_value:
                lowest_value = c.played_value
                lowest_card = c
        return lowest_card

    def has_two_cards_of_non_trump(self):
        """Checks if there are two cards of the same suit and returns the lowest.

        Returns:
            Card: Lowest card of the two, None if there are no two of the same suit
        """
        cards_of_suit = [0, 0, 0, 0]
        for card in self.cards:
            if not card.suit == self.game_model.trump:
                cards_of_suit[card.suit] += 1

        suits_idx = [index for index, count in enumerate(cards_of_suit) if count >= 2]
        if not suits_idx:  # there are no two cards of the same non_trump suit
            return None
        non_trump_suit = Suit(random.choice(suits_idx))
        return self.get_lowest_cards_of_suit(non_trump_suit)

    def has_highest_trump_card(self):
        """Returns true if player has a higher trump card than all the other players

        Returns:
            Card: the highest trump card of player
        """
        highest_card = None
        for player in self.game_model.players:
            if player is not self:
                if player.get_highest_card(
                    self.get_cards_of_suit(self.game_model.trump)
                ).evaluate(
                    self.game_model.trump, self.game_model.trick_suit
                ) > self.get_highest_card(
                    self.get_cards_of_suit(self.game_model.trump)
                ).evaluate(
                    self.game_model.trump, self.game_model.trick_suit
                ):
                    return None
                else:
                    highest_card = self.get_highest_card(
                        self.get_cards_of_suit(self.game_model.trump)
                    )

        return highest_card

    def highest_trump_of_table(self):
        return self.get_highest_card(self.game_model.table.items())
