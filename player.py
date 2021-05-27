from card import Card
from enum import Enum
import random


class Player:
    def __init__(self, seat_number, seat):
        self.seat_number = seat_number
        self.seat = seat
        self.cards = []
        self.name = Seat(seat_number).name
        self.score = 0

        self.wins = 0
        self.guessed_wins = 0
        self.opener = self.seat == Seat.NORTH

    def set_cards(self, cards):
        self.cards = cards
        for c in self.cards:
            c.owner = self

    def guess_wins(self, trump, winner, n_cards):
        self.guessed_wins = random.randint(0, n_cards)

    def change_guess(self, n_cards):
        x = random.randint(0, n_cards)
        if x == self.guessed_wins:
            self.change_guess(n_cards)
        else:
            self.guessed_wins = x

    def reset(self):
        self.wins = 0
        self.guessed_wins = 0

    def calculate_score(self):
        if self.wins == self.guessed_wins:
            self.score += self.wins * 2 + 10
        else:
            self.score -= self.wins * 2

    def add_win(self):
        self.wins += 1

    def play_card(self) -> Card:
        return self.cards.pop(random.randrange(len(self.cards)))


class Seat(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
