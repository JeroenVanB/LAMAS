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
        # FIXME implement game rules (he can now  play any card he wants)
        card = self.cards[random.randrange(len(self.cards))]
        return card
    
    def guess_wins(self, trump, total_tricks):
        return random.randint(0, total_tricks)