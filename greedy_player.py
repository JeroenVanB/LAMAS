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
        # if self.wins < self.guessed_wins:
        if self.opener:
            return self.get_highest_card(self.cards)
        else:
            # Do I have a trick suit?
            suit_cards = self.get_cards_of_suit(self.game_model.trick_suit)
            if suit_cards:
                return self.get_highest_card(suit_cards)
            else:
                return self.get_highest_card(self.cards)
        # else:
        #     # This is the tactic of the random player
        #     if self.opener:
        #         return self.get_random_card(self.cards)
        #     else:
        #         # Do I have a trick suit?
        #         suit_cards = self.get_cards_of_suit(self.game_model.trick_suit)
        #         if suit_cards:
        #             return self.get_random_card(suit_cards)
        #         else:
        #             return self.get_random_card(self.cards)
    
    def guess_wins(self, trump, total_tricks):
            """Guess the amount of tricks the player is going to win in this round

            Args:
                trump (Suit): The trump of the round
                n_cards (int): The amount of cards each player holds
            """
            # How the guessing is done:
            # Calculate the average value of a card of the player
            total_value_hand = 0
            mean_value_hand = 0
            for c in self.kb.own_cards:
                total_value_hand += c.pre_evaluate(trump=trump)
            mean_value_hand = total_value_hand/len(self.kb.own_cards)

            # Calculate the average value of a card in the game
            total_value_game = 0
            mean_value_game = 0
            for c in self.kb.all_cards:
                total_value_game += c.pre_evaluate(trump=trump)
            mean_value_game = total_value_game/len(self.kb.all_cards)

            # Normalize the value
            normalized_value_hand = mean_value_hand/mean_value_game

            # If the cards are evaluated far below the mean
            if normalized_value_hand < 0.8:
                guess = 0
            # If the cards are evaluated around the mean
            elif normalized_value_hand < 1.1:
                guess = int(total_tricks/4)
            # If the cards are evaluated higher than the mean
            elif normalized_value_hand < 1.3:
                guess = int(total_tricks/4 * 2)
            # If the cards are evaluated much higher than the mean
            else:
                guess = total_tricks
            self.guessed_wins = guess


