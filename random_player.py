from player import Player
from seat import Seat
from card import Card
from public_announcement import PublicAnnouncement
import random


class RandomPlayer(Player):
    """The Random Player always plays a random (legal) card
    """    
    def __init__(self, seat_number, seat: Seat):
        Player.__init__(self, seat_number, seat)
    
    def pick_card(self) -> Card:
        """Pick a card of a list of possible cards

        Args:
            possible_cards (list): the possible cards that the player can play
            trick_suit (bool): weather or not the player is able to play the trick suit

        Returns:
            Card: card that will be played
        """
        if self.opener:
            return self.get_random_card(self.cards)
        else:
            # Do I have a trick suit?
            suit_cards = self.get_cards_of_suit(self.game_model.trick_suit)
            if suit_cards:
                return self.get_random_card(suit_cards)
            else:
                return self.get_random_card(self.cards)


    
    def guess_wins(self, trump, total_tricks):
        self.guessed_wins = random.randint(0, total_tricks)