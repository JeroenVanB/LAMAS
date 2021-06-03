from player import Player
from seat import Seat
from card import Card
import random
from knowledge_base import KnowledgeBase

class GreedyKripkePlayer(Player):
    """The Kripke Player plays cards based on the kripke model
    """    
    def __init__(self, seat_number, seat: Seat):
        Player.__init__(self, seat_number, seat)
        self.kb = None

    def reset_knowledgebase(self):
        self.kb = KnowledgeBase(player=self, all_cards=self.all_cards, own_cards=self.cards)
        
    def pick_card(self, possible_cards: list, has_trick_suit:bool) -> Card:
        """Pick a card of a list of possible cards

        Args:
            possible_cards (list): the possible cards that the player can play
            trick_suit (bool): weather or not the player is able to play the trick suit

        Returns:
            Card: card that will be played
        """
        
        #TODO What if the the player is the opener?

        # If the player has a card of the trick suit
        if has_trick_suit:
            cards = self.get_cards_of_suit(self.game_model.trick_suit)
            if len(cards) < 2:
                # Play the highest card of the trick_suit, if you hold it
                highest_card = self.kb.get_highest_card_of_suit(self.game_model.trick_suit)
                if highest_card.owner == self.seat:
                    return highest_card
            # Otherwise, play the worst card
                return self.get_lowest_card_of_trick_suit()

        # The player does not have a card the trick suit
        elif not has_trick_suit:
            # Check if the player has trump cards
            if self.has_trump_cards():
                # The player must choose wether to play a trump card or not
                
                # 1. Playing a low trump card is good if the other (next) players still have cards of the trick suit (use kb)
                # If the other players still have cards of the trick suit: Play your lowest trump card
                if self.kb.do_next_players_have_suit(self.game_model.get_remaining_players(), self.game_model.trick_suit):
                    return self.get_lowest_cards_of_suit(self.game_model.trump)
                # If the other players to not have cards of the trick suit (They might play trump cards)
                else:
                    pass
                # 2a. If the player has the highest trump card in the game: play it (#TODO?)
                # 2b. If the player does not have the highest trump card in the game: play the worst card*.
                # 
            

                # Play the highest trump card (Greedy)
                # * How to calculate what is the worst card:
                #    (cannot be done by card.evaluate(), since that takes the trick suit into account)
                #    Look at the non trump, non trick suit cards
                #    Determine the card with the lowest rank (card.rank.value) 
                #           (#TODO Do we also need to take into account how many cards of that suit the player has?)
                #    Check which player has how many cards of which suit? (kb)


            highest_card = self.get_cards_of_suit(self.game_model.trump)
        

        # The player cannot play a card with the trick suit, so it plays its lowest card
        return possible_cards[random.randrange(len(possible_cards))] # TODO -> self.get_lowest_card(possible_cards)
