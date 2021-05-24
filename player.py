from enum import Enum
import random

class Player():
    
    def __init__(self, seat_number, seat):
        self.seat_number = seat_number
        self.seat = seat
        self.cards = []
        self.name = Seat(seat_number).name
        print(self.seat)
        if self.seat == Seat.NORTH:
            self.opener = True
        else:
            self.opener = False

    def set_cards(self, cards):
        self.cards = cards

    def play_card(self):
        return self.cards.pop(random.randrange(len(self.cards)))

class Seat(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    
