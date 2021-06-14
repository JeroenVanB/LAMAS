from card import Card, Suit
import random
from public_announcement import AnnouncementType
from seat import Seat
from abc import ABC
from knowledge_base import KnowledgeBase
from public_announcement import PublicAnnouncement


class Player(ABC):
    """An (abstract) object representing a player"""

    def __init__(self, seat_number, seat: Seat):
        """Basic inialization of a player

        Args:
            seat_number (int): Number of the seat
            seat (Seat): Seat (of enumaration Seat)
        """
        self.seat = seat
        self.cards = []
        self.all_cards = []
        self.name = Seat(seat_number).name
        self.score = 0
        self.game_model = None

        self.wins = 0
        self.guessed_wins = 0
        self.opener = self.seat == Seat.NORTH
        self.kb = None

    def set_game_model(self, game_model):
        """Setting the game model

        Args:
            game_model (GameModel): The game model object
        """
        self.game_model = game_model

    def set_cards(self, cards):
        """Set the owner of the cards in the cards owned by the player.

        Args:
            cards (List[Card]): list of cards owned by the player
        """
        self.cards = cards
        for c in self.cards:
            c.set_owner(self)

    def set_all_cards(self, cards):
        self.all_cards = cards

    def guess_wins(self, trump, total_tricks):
        """Guess the amount of tricks the player is going to win in this round

        Args:
            trump (Suit): The trump of the roun
            n_cards (int): The amount of cards each player holds
        """
        raise NotImplementedError(
            "Abstract class function call: Should be overridden by subclass"
        )

    def change_guess(self, n_cards):
        """Changing the amount of tricks the player guesses to win in this round

        Args:
            n_cards (int): The amount of cards each player holds
        """
        x = random.randint(0, n_cards)
        if x == self.guessed_wins:
            self.change_guess(n_cards)
        else:
            self.guessed_wins = x

    def reset(self):
        """Reset the amounf of wins and guessed wins"""
        self.wins = 0
        self.guessed_wins = 0

    def calculate_score(self):
        """Calculate the score of the round, by comparing the wins with the guessed wins"""
        if self.wins == self.guessed_wins:
            self.score += self.wins * 2 + 10
        else:
            self.score += abs(self.wins - self.guessed_wins) * -2

    def add_win(self):
        """Add a win to the total wins of the player"""
        self.wins += 1

    def play_card(self) -> Card:
        """Let the player pick a card to play

        Returns:
            Card: the card that the player chooses to play
        """
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
        raise NotImplementedError(
            "Abstract class function call: Should be overridden by subclass"
        )

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
            value = card.played_value
            if value > highest_value:
                highest_value = value
                highest_cards = [card]
            elif value == highest_value:
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
        """Look which card of the trump suit is the highest card on the table

        Returns:
            Card: The highest trump suit card on the table
        """

        return self.get_highest_card(
            [
                c
                for _, c in self.game_model.table.items()
                if c is not None and c.suit == self.game_model.trump
            ]
        )

    def reset_knowledgebase(self):
        """Reset the knowledge base of the player"""
        self.kb = KnowledgeBase(
            player=self, all_cards=self.all_cards, own_cards=self.cards
        )

    def receive_announcement(self, announcement: PublicAnnouncement):
        """Receive an announcement and apply the new knowledge by updating the kripke models

        Args:
            announcement (PublicAnnouncement): The annoucement object, containing the information of the anncouncement
        """
        t = announcement.type
        sender = announcement.sender
        card = announcement.card
        if t == AnnouncementType.card_played:
            # A card is played, so we now know the owner of that card
            # (and can exclude the possiblity of others having that card)
            self.kb.set_card_knowledge(card, sender)
        elif t == AnnouncementType.does_not_have_suit:
            # A player does not have cards of a specific suit
            self.kb.set_all_cards_of_suit_of_player(
                suit=self.game_model.trick_suit, player=sender, value=False
            )
