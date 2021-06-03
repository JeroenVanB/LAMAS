from player import Player
from seat import Seat
from card import Card
import random

class GreedyPlayer(Player):
    """The Greedy layer always plays the highest cards that he has
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
        card = self.get_highest_card(possible_cards)
        return card
    

