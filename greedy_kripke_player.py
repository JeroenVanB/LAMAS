from public_announcement import AnnouncementType, PublicAnnouncement
from player import Player
from seat import Seat
from card import Card
from knowledge_base import KnowledgeBase
import sys


class GreedyKripkePlayer(Player):
    """The Kripke Player plays cards based on the kripke model"""

    def __init__(self, seat_number, seat: Seat):
        Player.__init__(self, seat_number, seat)
    
    def pick_card(self) -> Card:
        """Pick a card based on a tactic.

        Returns:
            Card: card that will be played
        """

        if self.opener:
            # check if other players still have trump cards
            if self.kb.other_players_have_suit(self.game_model.trump):
                # check if I have the highest trump
                trump_cards = self.get_trump_cards()
                card = self.kb.get_highest_card_of_suit(self.game_model.trump)
                if trump_cards and card.owner == self:  # I have highest trump card
                    print("1 card is:", card.name)
                    return card
                else:
                    # Do I have highest non-trump?
                    cards = self.kb.get_highest_non_trump_cards()
                    # If there are multiple highest card in the hand return just 1
                    for c in cards:
                        card = c if c.owner == self else None 
                    
                    if card is not None and card.owner == self:
                        # Do the others still have cards of that suit?
                        if self.kb.other_players_have_suit(card.suit):
                            print("2 card is:", card.name)
                            return card
                        else:
                            print("3 card is:", self.get_lowest_card().name)
                            return self.get_lowest_card()  # play worst
                    else:  # Do I have two cards of the same suit, that are not trump?
                        card = self.has_two_cards_of_non_trump()
                        if card is not None:
                            print("4 card is:", card.name)
                            return card  # lowest of the two cards
                        else:
                            print("5 card is:", self.get_lowest_card().name)
                            return self.get_lowest_card()

            else:  # other players do not have trump cards
                # Check if I have highest non-trump
                cards = self.kb.get_highest_non_trump_cards()
                for c in cards:
                    card = c if c.owner == self else None
                if card is not None:
                    print("highest card:", card.name)
   
                if card is not None and card.owner == self:
                    print("6 card is:", card.name)
                    return card
                else:  # Do I have two cards of the same suit, that are not trump?
                    card = self.has_two_cards_of_non_trump()
                    if card is not None:
                        print("6 card is:", card.name)
                        return card  # Return lowest of two cards
                    else:
                        print("7 card is:", self.get_lowest_card().name)
                        return self.get_lowest_card()  # Random lowest card

        # Player is not the opener
        else:
            # Do I have a trick suit?
            if self.get_cards_of_suit(self.game_model.trick_suit):
                # Did someone play a trump card?
                if self.game_model.trump_on_table():
                    return self.get_lowest_card_of_trick_suit()
                else:
                    card = self.kb.get_highest_card_of_suit(self.game_model.trick_suit)
                    if card.owner == self:  # i have higest trick suit card
                        print("8 card is:", card.name)
                        return card
                    else:  # play lowest trick card (obligated)
                        print("9 card is:", self.get_lowest_card_of_trick_suit().name)
                        return self.get_lowest_card_of_trick_suit()

            else:  # I do not have the trick suit
                self.game_model.make_announcement(
                    sender=self,
                    card=None,
                    announcement_type=AnnouncementType.does_not_have_suit,
                )
                if self.get_trump_cards():  # Do I have a trump card?
                    # Am I the last player?
                    if self.game_model.cur_player == 3:
                        # There is a trump card on the table
                        if self.game_model.trump_on_table():
                            # Is the trump card on the table higher than the one in the hand
                            if self.highest_trump_of_table().evaluate(
                                self.game_model.trump, self.game_model.trick_suit
                            ) > self.get_highest_card(
                                self.get_cards_of_suit(self.game_model.trump)
                            ).evaluate(
                                self.game_model.trump, self.game_model.trick_suit
                            ):
                                print("10 card is:", self.get_lowest_card().name)
                                return self.get_lowest_card()
                            else:
                                print(
                                    "11 card is:",
                                    self.get_highest_card(
                                        self.get_cards_of_suit(self.game_model.trump)
                                    ).name,
                                )
                                return self.get_highest_card(
                                    self.get_cards_of_suit(self.game_model.trump)
                                )
                        else:
                            return self.get_lowest_card()
                    # Am I not the last player
                    else:
                        # Others have trick suit
                        if self.kb.other_players_have_suit(self.game_model.trick_suit):
                            # Others have trump cards
                            if self.kb.other_players_have_suit(self.game_model.trump):
                                # If you have the highest trump card, return that card
                                if self.has_highest_trump_card():
                                    print(
                                        "12 card is:",
                                        self.has_highest_trump_card().name,
                                    )
                                    return self.has_highest_trump_card()
                                else:
                                    print("13 card is:", self.get_lowest_card().name)
                                    return self.get_lowest_card()
                            else:  # others don't have trumps
                                print("14 card is:", self.get_lowest_card().name)
                                return self.get_lowest_cards_of_suit(
                                    self.game_model.trump
                                )
                        else:  # no one else has a trump
                            # play lowest trump
                            print("15 card is:", self.get_lowest_card().name)
                            return self.get_lowest_cards_of_suit(self.game_model.trump)
                return self.get_lowest_card()

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

    def guess_wins(self, trump, total_tricks):
            """Guess the amount of tricks the player is going to win in this round

            Args:
                trump (Suit): The trump of the roun
                n_cards (int): The amount of cards each player holds
            """
            # How the guessing is done:
            # Calculate the average value of a card of the player
            total_value_hand = 0
            mean_value_hand = 0
            for c in self.kb.own_cards:
                total_value_hand += c.evaluate(trump=trump, trick_suit=None)
            mean_value_hand = total_value_hand/len(self.kb.own_cards)
            # print('mean_value_hand:', mean_value_hand)

            # Calculate the average value of a card in the game
            total_value_game = 0
            mean_value_game = 0
            for c in self.kb.all_cards:
                total_value_game += c.evaluate(trump=trump, trick_suit=None)
            mean_value_game = total_value_game/len(self.kb.all_cards)
            # print('mean_value_game:', mean_value_game)

            # Normalize the value
            normalized_value_hand = mean_value_hand/mean_value_game

            # If the cards are evaluated far below the mean
            if normalized_value_hand < 0.8:
                guess = 0
            # If the cards are evaluated around the mean
            elif normalized_value_hand < 1.2:
                guess = int(total_tricks/4)
            # If the cards are evaluated higher than the mean
            elif normalized_value_hand < 1.4:
                guess = int(total_tricks/4 * 2)
            # If the cards are evaluated much higher than the mean
            else:
                guess = total_tricks
            print('mean_value_normalized:', mean_value_hand/mean_value_game,'\tguesses', guess)
            self.guessed_wins = guess