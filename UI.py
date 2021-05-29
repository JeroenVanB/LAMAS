import pygame
import pygame_gui
from pathlib import Path
from card import Card, CardValue, Suit
from player import Seat, Player
from typing import List, Tuple
from game_model import GameModel

RESOLUTION = (800, 800)
CARD_SIZE = (75, 100)
PLAYER_LOC = {
    # (LEFT, TOP)
    Seat.NORTH: (40 + CARD_SIZE[0] + 10 + 20 + CARD_SIZE[0], 20 + 20 + CARD_SIZE[1]),
    Seat.EAST: (
        60 + 2 * CARD_SIZE[0] + 20 + CARD_SIZE[0],
        30 + CARD_SIZE[1] + 20 + CARD_SIZE[1],
    ),
    Seat.SOUTH: (
        40 + CARD_SIZE[0] + 10 + 20 + CARD_SIZE[0],
        40 + 2 * CARD_SIZE[1] + 20 + CARD_SIZE[1],
    ),
    Seat.WEST: (60 + CARD_SIZE[0], 30 + CARD_SIZE[1] + 20 + CARD_SIZE[1]),
}


class UI:
    def __init__(self, model: GameModel) -> None:
        pygame.init()
        pygame.display.set_caption("Boeren Bridge")

        self.window_surface = pygame.display.set_mode(RESOLUTION)
        self.background = pygame.Surface(RESOLUTION)
        self.background_color = pygame.Color(50, 168, 82)
        self.background.fill(self.background_color)
        self.manager = pygame_gui.UIManager(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.model = model
        self.model.deal_cards(5)
        # # self.draw_south_cards(cards)
        self.start_game_loop()

    def start_game_loop(self):
        paused = False
        self.clear_table()

        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Space pressed")
                        paused = False

            if not paused:
                # draw background
                self.clear_table()
                # draw played cards of each player
                self.draw_current_table()

                # draw player cards
                self.draw_player_cards()
                paused = True

                pygame.display.update()
                self.clock.tick(60)

    def clear_table(self):
        self.window_surface.blit(self.background, (0, 0))
        pygame.display.update()

    def draw_current_table(self):
        """Draws the cards currently played."""

        for seat, card in self.model.table.items():
            loc = PLAYER_LOC[seat]
            ci = CardImage(card=card, rotate=False)
            rect = pygame.Rect(loc, CARD_SIZE)
            self.window_surface.blit(ci.img, rect)
        pygame.display.update()

    def draw_player_cards(self):
        "Draws all cards that are in each players hand"
        for player in self.model.players:
            if player.seat in [Seat.NORTH, Seat.SOUTH]:
                locs = self.get_north_south_locations(
                    len(player.cards), seat=player.seat
                )
            else:
                locs = self.get_west_east_locations(len(player.cards), seat=player.seat)

            rotate = player.seat in [Seat.WEST, Seat.EAST]

            for idx, card in enumerate(player.cards):
                ci = CardImage(card=card, rotate=rotate)
                rect = pygame.Rect(locs[idx], CARD_SIZE)
                self.window_surface.blit(ci.img, rect)
        pygame.display.update()

    def get_north_south_locations(self, num_cards, seat=Seat.NORTH) -> list:
        """Returns the locations of the North or South player so that we can view his cards"""
        positions = []
        start_l = 50 + CARD_SIZE[0]
        if seat == Seat.NORTH:
            top_val = 30
        else:
            top_val = PLAYER_LOC[Seat.SOUTH][1] + CARD_SIZE[1] + 10
        for i in range(num_cards):
            l = start_l + i * (CARD_SIZE[0] / 3)
            positions.append((l, top_val))
        return positions

    def get_west_east_locations(self, num_cards, seat=Seat.WEST) -> list:
        positions = []
        if seat == Seat.WEST:
            left_val = 30
        else:
            left_val = PLAYER_LOC[Seat.EAST][0] + CARD_SIZE[0] + 10
        start_top = PLAYER_LOC[Seat.NORTH][1] + CARD_SIZE[1] / 2
        for i in range(num_cards):
            top = start_top + i * (CARD_SIZE[0] / 3)
            positions.append((left_val, top))
        return positions


class CardImage:
    def __init__(self, card: Card, rotate: bool, closed=False) -> None:
        self.original_size = (868, 1600)
        self.size = CARD_SIZE
        self.card = card
        self.rotate = rotate
        self.closed = closed
        self.img_src = str(Path(__file__).resolve().parent) + "/img/cards/"
        self.back_side = str(Path(__file__).resolve().parent) + "/img/back-side.png"
        self.img = self.card_to_image()

    def card_to_image(self) -> str:
        if self.card is None or self.closed:
            img = pygame.image.load(self.back_side)
        else:
            value = self.card.rank.value
            suit = str(self.card.suit.name).lower()

            if value < 9:
                value += 2
            else:
                value = str(self.card.rank.name).lower()
            file = str(value) + "_of_" + suit + ".png"
            path = self.img_src + file
            img = pygame.image.load(path)
        img.convert()
        img = pygame.transform.scale(img, CARD_SIZE)
        if self.rotate:
            img = pygame.transform.rotate(img, -90)
        return img


if __name__ == "__main__":
    model = GameModel()
    ui = UI(model)

    # card = Card(CardValue(2), Suit(0))
    # print(CardImage(card).img)
