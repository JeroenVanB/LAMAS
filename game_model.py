from typing import List
from player import Player
from random_player import RandomPlayer
from greedy_player import GreedyPlayer
from greedy_kripke_player import GreedyKripkePlayer
from seat import Seat
from deck import Deck
from card import Card, Suit
import random
from public_announcement import PublicAnnouncement, AnnouncementType


class GameModel:
    def __init__(self, players=["greedy", "greedy", "kripke", "kripke"]):
        self.cards_per_round = [3, 4, 5, 4, 3]
        self.set_players(players)
        for p in self.players:
            p.set_game_model(self)

        self.deck = Deck()
        self.table = {
            Seat.NORTH: None,
            Seat.EAST: None,
            Seat.SOUTH: None,
            Seat.WEST: None,
        }
        self.trump = None
        self.trick_suit = None
        self.cur_round = 0
        self.cur_trick = 0
        self.cur_player = 0
        self.finished = False

        self.deal_cards(self.cards_per_round[self.cur_round])
        for p in self.players:
            p.reset()
            p.reset_knowledgebase()
            p.kb.set_game_model(self)

        self.status = ["Starting a round of Boeren Bridge!"] + [
            f"Round {idx+1} is played with {c} cards"
            for idx, c in enumerate(self.cards_per_round)
        ]

    def set_players(self, players: List[str]):
        """Constructs player instances based on string names

        Args:
            players (List[str]): The names of the players. Can be: greedy, kripke, random
        """
        self.players = []
        for idx, p in enumerate(players):
            if p == "greedy":
                player = GreedyPlayer(idx, Seat(idx))
            elif p == "kripke":
                player = GreedyKripkePlayer(idx, Seat(idx))
            else:
                player = RandomPlayer(idx, Seat(idx))
            self.players.append(player)

    def next_move(self):
        """Execute the next move of the game. The move is determined by whose turn it is, or if the game or the round has already ended"""
        self.status = []
        if self.cur_player > 3:
            # Trick has ended
            self.cur_player = 0
            self.cur_trick += 1

            # Determine the winner of the trick
            winner = self.determine_winner(self.trump, self.trick_suit)
            winner.add_win()
            self.status += [f"{winner.seat.name} wins the trick!"]

            # Make the winner of the previous trick the opener
            for player in self.players:
                player.opener = False
                if player.seat.name == winner.seat.name:
                    opener = winner
                    player.opener = True
            self.order_players(opener)
            self.trick_suit = None

            # Remove all cards from the table from all knowledge bases.
            for p in self.players:
                for _, card in self.table.items():
                    p.kb.remove_card(card)
            self.reset_table()

        if self.cur_round == len(self.cards_per_round):
            # Game has ended
            self.status += [f"The game has ended!"]
            self.finished = True
            return

        if self.cur_trick == self.cards_per_round[self.cur_round]:
            # round has ended
            for p in self.players:
                p.calculate_score()
            self.cur_trick = 0
            self.cur_round += 1
            self.status += ["The round has ended"]
            return

        if self.cur_trick == 0 and self.cur_player == 0:
            # start of a round
            self.deal_cards(self.cards_per_round[self.cur_round])
            for p in self.players:
                p.reset()
                p.reset_knowledgebase()
                p.kb.set_game_model(self)
            self.trump = self.pick_trump()
            opener = self.get_opener()
            self.order_players(opener)
            self.make_guesses(self.trump, self.cards_per_round[self.cur_round])
            self.status += [
                f"Trump is {self.trump.name}, {opener.name} has to open the game"
            ]

        if self.cur_trick < self.cards_per_round[self.cur_round]:
            # Let a player make a move in the current trick
            player = self.players[self.cur_player]
            card = player.play_card()
            self.table[player.seat] = card
            if self.cur_player == 0:
                self.trick_suit = card.suit
                self.status += [f"Trick suit is {card.suit.name}"]
            self.table[player.seat] = card
            self.cur_player += 1

    def get_remaining_players(self):
        """Obtaining the players that still need to play a card in the tricking

        Returns:
            list: The Players that still need to play a card
        """
        return self.players[self.cur_player + 1 : len(self.players)]

    def make_guesses(self, trump, n_cards):
        """Let all the players guess how many tricks they will win in the next round

        Args:
            trump (Suit): Trump of the game
            n_cards (int): Number of cards that each player holds
        """
        total_guessed = 0
        for p in self.players:
            p.guess_wins(trump, total_tricks=n_cards)
            total_guessed += p.guessed_wins
        # If the guesses add up to the amount of cards, the dealer must change his guess
        if total_guessed == n_cards:
            self.players[3].change_guess(
                n_cards
            )  # the last player in the list is always the dealer.
            self.status += [
                f"Player {self.players[3].seat.name} changes to guessing {self.players[3].guessed_wins} wins"
            ]

    def deal_cards(self, n_cards):
        """Dealing the cards between the players and

        Args:
            n_cards (int): The amount of cards that each player gets
        """
        # Get a deck of cards
        self.deck.reset_deck(n_cards)
        self.deck.shuffle()
        self.remaining_cards = self.deck.cards
        assert len(self.deck.cards) == len(self.players) * n_cards
        for idx, p in enumerate(self.players):
            p.set_cards(self.deck.cards[idx * n_cards : (1 + idx) * n_cards])
            p.set_all_cards(self.deck.cards)

    def reset_table(self):
        """Reset the table by removing the cards played by each player"""
        self.table = {
            Seat.NORTH: None,
            Seat.EAST: None,
            Seat.SOUTH: None,
            Seat.WEST: None,
        }

    def get_opener(self):
        """Determine who should be the opener of the next trick

        Raises:
            Exception: The opener cannot be determined

        Returns:
            Player: The opener of the next trick
        """
        for player in self.players:
            if player.opener:
                return player
        raise Exception("Error: Opener could not be found")

    def order_players(self, opener):
        """Order the players in self.players in the order in which the cards will be playerd

        Args:
            opener (Player): The opener of the next trick
        """
        idx = self.players.index(opener)
        self.players = self.players[idx:] + self.players[:idx]

    def pick_trump(self):
        """Choose the trump (randomly)

        Returns:
            Suit: The trump suit for the next round
        """
        return Suit(random.randint(0, 3))

    def determine_winner(self, trump, trick_suit):
        """Determine the winner of the last played trick

        Args:
            trump (Suit): Tuimp suit of the round
            trick_suit (Suit): The trick suit
        Returns:
            Player: The winner of the trick
        """
        highest_value = 0
        winner = None
        for _, c in self.table.items():
            c.evaluate(trump, trick_suit)
            if c.played_value > highest_value:
                highest_value = c.played_value
                winner = c.owner
        return winner

    def make_announcement(
        self, sender: Player, card: Card, announcement_type: AnnouncementType
    ):
        """Make an announcement, to inform al the players. The announcements can be used update the kb

        Args:
            sender (Player): The sender of the annoucement
            card (Card): The card that the sender played
            announcement_type (AnnouncementType): The type of announcement which is send to all the players
        """
        public_announcement = PublicAnnouncement(sender, announcement_type, card)
        for player in self.players:
            player.receive_announcement(public_announcement)

        # Show messages in the UI
        msg = []
        if announcement_type == AnnouncementType.card_played:
            msg += [f"Public Announcement: Player {sender.name} plays {card.name}"]
        elif announcement_type == AnnouncementType.does_not_have_suit:
            msg += [
                f"Public Announcement: Player {sender.name} does not have suit {Suit(self.trick_suit).name}"
            ]

        self.status += msg

    def trump_on_table(self):
        """Is there a trump card played on the table?

        Returns:
            bool: Wether there is a trump card on the table or not
        """
        for _, c in self.table.items():
            if c is not None and c.suit == self.trump:
                return True
        return False


if __name__ == "__main__":
    game_model = GameModel()
    game_model.start_game()
