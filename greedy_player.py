from public_announcement import AnnouncementType
from player import Player
from seat import Seat
from card import Card
import random

class GreedyPlayer(Player):
    """The Greedy layer always plays the highest cards that he has
    """    
    def __init__(self, seat_number, seat: Seat):
        Player.__init__(self, seat_number, seat)
    
    def pick_card(self) -> Card:
        """Picks a card based on a greedy tactic

        Returns:
            Card: the card that is picked
        """
        cards_of_suit = []
        if self.game_model.trick_suit is not None:
            cards_of_suit = self.get_cards_of_suit(self.game_model.trick_suit)
        # If the player has the trick suit, he must follow suit
        if len(cards_of_suit) > 0:
            played_card = self.get_highest_card(cards_of_suit)
        else:
            # The player does not have the trick suit, so may play what he wants
            played_card = random.choice(self.cards)
            if self.game_model.trick_suit:
                self.game_model.make_announcement(self, None, AnnouncementType.does_not_have_suit)
        return played_card


