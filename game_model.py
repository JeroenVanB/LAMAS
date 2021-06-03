from typing import List
from player import Player
from seat import Seat
from deck import Deck
from card import Card, Suit
import sys
import random
from operator import attrgetter
from public_announcement import PublicAnnouncement, AnnouncementType


class GameModel:
    def __init__(self):
        # TODO determine rounds/cards per round
        self.cards_per_round = [3, 4]
        self.players = [Player(i, Seat(i)) for i in range(4)]
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
        self.played_cards = []
        self.cur_round = 0
        self.cur_trick = 0
        self.cur_player = 0
        self.finished = False
        self.status = ["Starting a round of Boeren Bridge!"] + [
            f"Round {idx+1} is played with {c} cards"
            for idx, c in enumerate(self.cards_per_round)
        ]
        print(self.status)

    def next_move(self):
        print("====  looking at next move.  ====")
        self.status = []
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
            self.status += [f'{winner.seat.name} wins the trick!']
            self.trick_suit = None
            # print(winner.seat.name, "wins the trick!")

        if self.cur_round == len(self.cards_per_round):
            # Game has ended
            self.status += [f'The game has ended!']
            self.finished = True
            return

        if self.cur_trick == self.cards_per_round[self.cur_round]:
            # round has ended
            for p in self.players:
                p.calculate_score()
            self.cur_trick = 0
            self.cur_round += 1
            self.status += ['The round has ended']
            return

        if self.cur_trick == 0 and self.cur_player == 0:
            # start of a round
            for p in self.players:
                p.reset()
            self.deal_cards(self.cards_per_round[self.cur_round])
            self.trump = self.pick_trump()
            opener = self.get_opener()
            self.order_players(opener)
            self.make_guesses(self.trump, opener, self.cards_per_round[self.cur_round])
            self.status += [f'Trump is {self.trump.name}, {opener.name} has to open the game']

        if self.cur_trick < self.cards_per_round[self.cur_round]:
            # Let a player make a move in the current trick
            player = self.players[self.cur_player]
            card = player.play_card()
            self.table[player.seat] = card

            if self.cur_player == 0:
                self.trick_suit = card.suit
                self.status += [f'Trick suit is {card.suit.name}']
            self.played_cards.append(card)
            self.cur_player += 1


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
            self.status += [f'Player {self.players[3].seat.name} changes to guessing {self.players[3].guessed_wins} wins']
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
            p.set_all_cards(self.deck.cards)

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

    def determine_winner(self, played_cards: List[Card], trump, trick_suit):
        highest_value = 0
        for c in played_cards:
            c.evaluate(trump, trick_suit)
            # print("value of ", c, " is ", c.played_value)
            if c.played_value > highest_value:
                highest_value = c.played_value
        return c.owner

    def make_announcement(self, sender: Player, card:Card, announcement_type:AnnouncementType):
        public_announcement = PublicAnnouncement(sender, card, announcement_type)
        for player in self.players:
            player.receive_announcement(public_announcement)
        
        # Show messages in the UI 
        msg = []
        if announcement_type == AnnouncementType.card_played:
            msg += [f'Public Announcement: Player {sender.name} plays {card.name}']
        elif announcement_type == AnnouncementType.does_not_have_suit:
            msg += [f'Public Announcement: Player {sender.name} does not have suit {self.trick_suit.name}']
        
        self.status += msg

if __name__ == "__main__":
    game_model = GameModel()
    game_model.start_game()
