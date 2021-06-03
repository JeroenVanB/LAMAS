from player import Player
from seat import Seat
from card import Card
import random

class RandomPlayer(Player):
    """The Random Player always plays a random (legal) card
    """    
    def __init__(self, seat_number, seat: Seat):
        Player.__init__(self, seat_number, seat)
    
    def pick_card(self, possible_cards: list, has_trick_suit:bool) -> Card:
        """Pick a card of a list of possible cards

        Args:
            possible_cards (list): the possible cards that the player can play
            trick_suit (bool): weather or not the player is able to play the trick suit

        Returns:
            Card: card that will be played
        """
        card = possible_cards[random.randrange(len(possible_cards))]
        return card