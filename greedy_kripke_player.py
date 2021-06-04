from public_announcement import AnnouncementType
from typing import overload
from player import Player
from seat import Seat
from card import Card, Suit
import random
from knowledge_base import KnowledgeBase


class GreedyKripkePlayer(Player):
    """The Kripke Player plays cards based on the kripke model"""

    def __init__(self, seat_number, seat: Seat):
        Player.__init__(self, seat_number, seat)
        self.kb = None

    def reset_knowledgebase(self):
        self.kb = KnowledgeBase(
            player=self, all_cards=self.all_cards, own_cards=self.cards
        )

    def pick_card(self) -> Card:
        """Pick a card based on a tactic.

        Returns:
            Card: card that will be played
        """

        if self.opener:
            # check if other players still have trump cards
            if self.kb.other_players_have_suit(self.game_model.trump):
                # check if I have the highest trump
                trump_cards = self.pick_trump_card()
                card, owner = self.kb.get_highest_card_of_suit(self.game_model.trump)
                if trump_cards and owner == self:  # I have highest trump card
                    return card
                else:
                    # Do I have highest non-trump?
                    card, owner = self.kb.get_highest_non_trump_card()
                    if owner == self:
                        # Do the others still have cards of that suit?
                        if self.kb.other_players_have_suit(card.suit):
                            return self.get_lowest_card()  # play worst
                        else:
                            return card
                    else:  # Do I have two cards of the same suit, that are not trump?
                        card = self.has_two_cards_of_non_trump()
                        if card is not None:
                            return card  # lowest of the two cards
                        else:
                            return self.get_lowest_card()

            else:  # other players do not have trump cards
                # Check if I have highest non-trump
                card, owner = self.kb.get_highest_non_trump_card()
                if owner == self:
                    return card
                else:  # Do I have two cards of the same suit, that are not trump?
                    card = self.has_two_cards_of_non_trump()
                    if card is not None:
                        return card  # Return lowest of two cards
                    else:
                        return self.get_lowest_card()  # Random lowest card

        # Player is not the opener
        else:
            # Do I have a trick suit?
            if self.get_cards_of_suit(self.game_model.trick_suit):
                # do i have highest trick suit?
                card, owner = self.kb.get_highest_card_of_suit(
                    self.game_model.trick_suit
                )
                if owner == self:  # i have higest trick suit card
                    return card
                else:  # play lowest trick card (obligated)
                    return self.get_lowest_card_of_trick_suit()

            else:  # I do not have the trick suit
                self.game_model.make_announcement(
                    sender=self,
                    card=None,
                    announcement_type=AnnouncementType.does_not_have_suit,
                )
                if self.get_trump_cards():  # Do I have a trump card?
                    if self.game_model.cur_player > 
                    # Others have trick suit
                    if self.kb.other_players_have_suit(self.game_model.trick_suit):
                        # Others have trump cards
                        if self.kb.other_players_have_suit(self.game_model.trump):
                            # If you have the highest trump card, return that card
                            if self.has_highest_trump_card():
                                return self.has_highest_trump_card()
                            else:
                                return self.get_lowest_card()
                            # Other players have trump cards higher than your trump cards
                            # if OTHERS HAVE HIGHER TRUMPS:
                            # return self.get_lowest_card()

                            # else:
                            # return lowest trump that still wins (higher than others)
                        else:  # others don't have trumps
                            return self.get_lowest_cards_of_suit(
                                self.game_model.trump_suit
                            )
                    else:  # no one else has a trump
                        # play lowest trump
                        return self.get_lowest_cards_of_suit(
                            self.game_model.trump_suit
                            )
                return self.get_lowest_card()
