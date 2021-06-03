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
        self.kb = None

    def set_game_model(self, game_model):
        self.game_model = game_model
    
    def set_cards(self, cards):
        self.cards = cards
        for c in self.cards:
            c.owner = self
    
    def set_all_cards(self, cards):
        self.all_cards = cards

    def reset_knowledgebase(self):
        self.kb = KnowledgeBase(player=self, all_cards=self.all_cards, own_cards=self.cards)

    def guess_wins(self, trump, winner, n_cards):
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
            self.score -= self.wins * 2

    def add_win(self):
        self.wins += 1

    def receive_announcement(self, announcement: PublicAnnouncement):
        t = announcement.type
        sender = announcement.sender
        card = announcement.card
        
        if t == AnnouncementType.card_played:
            # Since the card is played, it's no longer part of the game
            self.kb.remove_card(card)
        
        elif t == AnnouncementType.does_not_have_suit:
            self.kb.set_all_cards_of_suit_of_player(suit=self.game_model.trick_suit, player=sender, value=False)


    def play_card(self) -> Card:
        # Check if the player has cards of the same suit as the trick suit
        cards_of_suit = []
        if self.game_model.trick_suit is not None:
            cards_of_suit = self.get_cards_of_suit(self.game_model.trick_suit)
        
        # If the player has the trick suit, he must follow suit
        if len(cards_of_suit) > 0:
            played_card = self.pick_card(cards_of_suit)
            # Make announcement does_have_suit
            self.game_model.make_announcement(self, played_card, AnnouncementType.card_played)
        else:
            # The player does not have the trick suit, so may play what he wants
            #TODO this should not be random (bijv introeven, laag opleggen)
            played_card = self.cards.pop(random.randrange(len(self.cards)))
            self.game_model.make_announcement(self, played_card, AnnouncementType.card_played)
            # Make announcement does_not_have_suit
            if self.game_model.trick_suit:
                self.game_model.make_announcement(self, None, AnnouncementType.does_not_have_suit)
        return played_card

    def pick_card(self, possible_cards: list) -> Card:
        """Pick a card of a list of possible cards

        Args:
            possible_cards (list): the possible cards that the player can play

        Returns:
            Card: card that will be played
        """        
        # TODO this should not be random. Needs stragegy.
        card = possible_cards[random.randrange(len(possible_cards))]
        # Remove the card from the hand (self.cards)
        self.cards.remove(card)
        return card
        
    def get_cards_of_suit(self, suit: Suit) -> list:
        """Get the player's cards of a given suit

        Args:
            suit (Suit): The suit of the card

        Returns:
            List: List of the cards of the given suit
        """
        cards_of_suit = []
        for card in self.cards:
            if card.suit == suit:
                cards_of_suit.append(card)
        return cards_of_suit

    def pick_trump_card(self, possible_cards: list) -> list:
        """Pick the player's trump cards

        Args:
            possible_cards (list): Possible cards

        Returns:
            List: List of possible trump cards
        """
        trump_cards = []
        for card in self.cards:
            if card.suit == self.game_model.trump:
                trump_cards.append(card)
        return trump_cards