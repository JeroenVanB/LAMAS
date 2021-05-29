from player import Player, Seat
from deck import Deck
from card import Suit
import sys
import random
from operator import attrgetter


class GameModel:
    def __init__(self):
        # TODO determine rounds/cards per round
        self.cards_per_round = [8, 3]
        self.players = [Player(i, Seat(i)) for i in range(4)]
        self.deck = Deck()
        self.table = {
            Seat.NORTH: None,
            Seat.EAST: None,
            Seat.SOUTH: None,
            Seat.WEST: None,
        }
        self.trump = None
        self.trick_suit = None
        self.played_cards = []
        self.cur_round = 0
        self.cur_trick = 0
        self.cur_player = 0

    def next_move(self):
        print("====  looking at next move.  ====")
        if self.cur_player > 3:
            # Trick has ended
            self.cur_player = 0
            self.cur_trick += 1
            self.reset_table()
            # Determine the winner of the trick
            # This is determined using the played_cards and the trick_suit
            winner = self.determine_winner(
                self.played_cards, self.trump, self.trick_suit
            )
            winner.add_win()
            print(winner.seat.name, "wins the trick!")

        if self.cur_round == len(self.cards_per_round):
            # Game has ended
            print(
                "The game has ended.\nThe winner is",
                max(self.players, key=attrgetter("score")).name,
            )
            exit(0)

        if self.cur_trick == self.cards_per_round[self.cur_round]:
            # round has ended
            for p in self.players:
                p.calculate_score()
            print(
                "Scores after round",
                self.cur_round + 1,
                ":",
                [p.score for p in self.players],
            )
            self.cur_trick = 0
            self.cur_round += 1
            return

        print(
            f"round {self.cur_round + 1}/{len(self.cards_per_round)} trick {self.cur_trick + 1 }/{self.cards_per_round[self.cur_round]}"
        )

        if self.cur_trick == 0 and self.cur_player == 0:
            # start of a round
            for p in self.players:
                p.reset()
            self.deal_cards(self.cards_per_round[self.cur_round])
            self.trump = self.pick_trump()
            print("Trump is", self.trump)
            opener = self.get_opener()
            self.order_players(opener)
            print("Player Order : ", [p.seat.name for p in self.players])
            self.make_guesses(self.trump, opener, self.cards_per_round[self.cur_round])

        if self.cur_trick < self.cards_per_round[self.cur_round]:
            # Let a player make a move in the current trick
            player = self.players[self.cur_player]
            card = player.play_card()
            self.table[player.seat] = card
            print(f"{player.seat.name} plays {card}")
            if self.cur_player == 0:
                self.trick_suit = card.suit
                print("Trick suit is :", self.trick_suit.name)
            self.played_cards.append(card)

            self.cur_player += 1

    def start_game(self):
        for round in range(len(self.cards_per_round)):
            for p in self.players:
                p.reset()
            self.play_round(round, self.cards_per_round[round])
            for p in self.players:
                p.calculate_score()
            print("Scores after round", round, ":", [p.score for p in self.players])

        print("The winner is", max(self.players, key=attrgetter("score")).name)

    def play_round(self, round, n_cards):
        print("=== Round", round, "with", n_cards, "cards", "===")
        self.deal_cards(n_cards)
        trump = self.pick_trump()
        print("Trump is ", trump)
        # Determine which player starts, this is usually the winner
        winner = self.get_opener()
        for trick in range(n_cards):
            self.reset_table()
            print("--- Trick", trick + 1, "/", n_cards, "---")

            self.order_players(winner)
            # print('The opener is', opener.name)
            print("Player Order : ", [p.seat.name for p in self.players])

            # Let all players make guess
            self.make_guesses(trump, winner, n_cards)
            # Every player plays a card in order
            self.played_cards = []
            for idx, p in enumerate(self.players):
                card = p.play_card()
                self.table[p] = card
                print(f"{p.seat.name} plays {card}")
                if idx == 0:
                    trick_suit = card.suit
                    print("Trick suit is :", trick_suit.name)
                self.played_cards.append(card)

            # Determine the winner of the trick
            # This is determined using the played_cards and the trick_suit
            winner = self.determine_winner(self.played_cards, trump, trick_suit)
            winner.add_win()
            print(winner.seat.name, "wins the trick!")

    def make_guesses(self, trump, winner, n_cards):
        total_guessed = 0
        for p in self.players:
            p.guess_wins(trump, winner, n_cards)
            print("Player", p.seat.name, "guesses", p.guessed_wins, "wins")
            total_guessed += p.guessed_wins
        if total_guessed == n_cards:
            print(
                "The guesses add up to",
                total_guessed,
                "so the dealer guesses again",
            )
            self.players[3].change_guess(
                n_cards
            )  # the last player in the list is always the dealer.
            print(
                "Player",
                self.players[3].seat.name,
                "changes to guessing",
                self.players[3].guessed_wins,
                "wins",
            )

    def deal_cards(self, n_cards):
        # Get a deck of cards
        self.deck.reset_deck(n_cards)
        self.deck.shuffle()
        print(len(self.deck.cards))
        print(len(self.players) * n_cards)
        assert len(self.deck.cards) == len(self.players) * n_cards
        for idx, p in enumerate(self.players):
            p.set_cards(self.deck.cards[idx * n_cards : (1 + idx) * n_cards])

    def reset_table(self):
        self.table = {
            Seat.NORTH: None,
            Seat.EAST: None,
            Seat.SOUTH: None,
            Seat.WEST: None,
        }

    def get_opener(self):
        for player in self.players:
            if player.opener:
                return player
        print("Error: Opener could not be found")
        sys.exit(1)

    def order_players(self, opener):
        idx = self.players.index(opener)
        self.players = self.players[idx:] + self.players[:idx]

    def pick_trump(self):
        return Suit(random.randint(0, 3))

    def determine_winner(self, played_cards, trump, trick_suit):
        highest_value = 0
        for c in played_cards:
            c.evaluate(trump, trick_suit)
            # print("value of ", c, " is ", c.played_value)
            if c.played_value > highest_value:
                highest_value = c.played_value
        return c.owner


if __name__ == "__main__":
    game_model = GameModel()
    game_model.start_game()
