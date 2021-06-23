from public_announcement import AnnouncementType
from player import Player
from seat import Seat
from card import Card


class FullKripkePlayer(Player):
    """The Kripke Player plays cards based on the Kripke model"""

    def __init__(self, seat_number, seat: Seat):
        Player.__init__(self, seat_number, seat)

    def pick_card(self) -> Card:
        """Pick a card based on a tactic.
        Returns:
            Card: card that will be played
        """
        # The player wants to win a trick
        if self.wins < self.guessed_wins:
            if self.opener:
                # check if other players still have trump cards
                if self.kb.other_players_have_suit(self.game_model.trump):
                    # check if I have the highest trump
                    trump_cards = self.get_trump_cards()
                    card = self.kb.get_highest_card_of_suit(self.game_model.trump)
                    if trump_cards and card.owner == self:  # I have highest trump card
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
                                return card
                            else:
                                return self.get_lowest_card()  # play worst
                        else:  # Do I have two cards of the same suit, that are not trump?
                            card = self.has_two_cards_of_non_trump()
                            if card is not None:
                                return card  # lowest of the two cards
                            else:
                                return self.get_lowest_card()

                else:  # other players do not have trump cards
                    # Check if I have highest non-trump
                    cards = self.kb.get_highest_non_trump_cards()
                    for c in cards:
                        card = c if c.owner == self else None
                    if card is not None and card.owner == self:
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
                    # Did someone play a trump card?
                    if self.game_model.trump_on_table():
                        return self.get_lowest_card_of_trick_suit()
                    else:
                        card = self.kb.get_highest_card_of_suit(
                            self.game_model.trick_suit
                        )
                        if card.owner == self:  # i have higest trick suit card
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

                                    return self.get_lowest_card()
                                else:
                                    return self.get_highest_card(
                                        self.get_cards_of_suit(self.game_model.trump)
                                    )
                            else:

                                return self.get_lowest_card()
                        # Am I not the last player
                        else:
                            # Others have trick suit
                            if self.kb.other_players_have_suit(
                                self.game_model.trick_suit
                            ):
                                # Others have trump cards
                                if self.kb.other_players_have_suit(
                                    self.game_model.trump
                                ):
                                    # If you have the highest trump card, return that card
                                    if self.has_highest_trump_card():
                                        return self.has_highest_trump_card()
                                    else:
                                        return self.get_lowest_card()
                                else:  # others don't have trumps
                                    return self.get_lowest_cards_of_suit(
                                        self.game_model.trump
                                    )
                            else:  # no one else has a trump
                                # play lowest trump
                                return self.get_lowest_cards_of_suit(
                                    self.game_model.trump
                                )
                    return self.get_lowest_card()
        # If he does not need a win
        else:
            # He wants to lose this and the following tricks
            if self.opener:
                return self.get_lowest_card()
            else:
                # Do I have a trick suit?
                suit_cards = self.get_cards_of_suit(self.game_model.trick_suit)
                if suit_cards:
                    # Did someone play a trump card?
                    if self.game_model.trump_on_table():
                        # Play the highest trick suit card
                        return self.get_highest_card(
                            self.get_cards_of_suit(self.game_model.trick_suit)
                        )
                    else:
                        card = self.kb.get_highest_card_of_suit(
                            self.game_model.trick_suit
                        )
                        if card.owner == self:  # I have the highest trick suit card
                            return self.get_highest_card(
                                self.get_cards_of_suit(self.game_model.trick_suit)
                            )
                        else:  # Play the highest trick suit card that still loses
                            highest_losing = self.get_highest_card_below(
                                self.get_cards_of_suit(self.game_model.trick_suit),
                                self.game_model.highest_card_of_table(),
                            )
                            if highest_losing is not None:
                                return highest_losing
                            else:
                                return self.get_highest_card(
                                    self.get_cards_of_suit(self.game_model.trick_suit)
                                )
                else:  # He does not have trick suit
                    self.game_model.make_announcement(
                        sender=self,
                        card=None,
                        announcement_type=AnnouncementType.does_not_have_suit,
                    )
                    # Does he have trump cards?
                    own_trump_cards = self.get_trump_cards()
                    if own_trump_cards:
                        # Is there trump on the table?
                        if self.game_model.trump_on_table():
                            # Does he have a lower trump card?
                            highest_trump = self.highest_trump_of_table()
                            if self.contains_lower(own_trump_cards, highest_trump):
                                return self.get_highest_card_below(
                                    own_trump_cards, highest_trump
                                )
                    return self.get_highest_card(self.cards)

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
            total_value_hand += c.pre_evaluate(trump=trump)
        mean_value_hand = total_value_hand / len(self.kb.own_cards)

        # Normalize the value
        normalized_value_hand = mean_value_hand / self.game_model.mean_card_value

        # If the cards are evaluated far below the mean
        if normalized_value_hand < 0.8:
            guess = 0
        # If the cards are evaluated around the mean
        elif normalized_value_hand < 1.1:
            guess = int(total_tricks / 4)
        # If the cards are evaluated higher than the mean
        elif normalized_value_hand < 1.3:
            guess = int(total_tricks / 4 * 2)
        # If the cards are evaluated much higher than the mean
        else:
            guess = total_tricks
        self.guessed_wins = guess
