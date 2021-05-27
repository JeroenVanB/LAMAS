import pygame
import pygame_gui
from pathlib import Path
from card import Card, CardValue, Suit
from player import Seat, Player


RESOLUTION = (800, 800)
CARD_SIZE = (75, 100)
PLAYER_LOC = {
    # (LEFT, TOP)
    Seat.NORTH: (20 + CARD_SIZE[0] + 10, 20),
    Seat.EAST: (40 + 2 * CARD_SIZE[0], 30 + CARD_SIZE[1]),
    Seat.SOUTH: (20 + CARD_SIZE[0] + 10, 40 + 2 * CARD_SIZE[1]),
    Seat.WEST: (20, 30 + CARD_SIZE[1]),
}

SOUTH_PLAY_LOCS = [()]


class UI:
    def __init__(self) -> None:
        self.player_centers = {Seat.NORTH: ()}
        pygame.init()
        pygame.display.set_caption("Boeren Bridge")
        self.window_surface = pygame.display.set_mode(RESOLUTION)
        self.background = pygame.Surface(RESOLUTION)
        self.background_color = pygame.Color(50, 168, 82)
        self.background.fill(self.background_color)
        self.manager = pygame_gui.UIManager(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.is_running = True

        for s, loc in PLAYER_LOC.items():
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(loc, CARD_SIZE),
                text=str(s),
                manager=self.manager,
            )

        cards = [
            Card(CardValue(2), Suit(0)),
            Card(CardValue(8), Suit(1)),
            Card(CardValue(10), Suit(2)),
            Card(CardValue(12), Suit(3)),
            Card(CardValue(1), Suit(0)),
        ]
        self.draw_south_cards(cards)
        self.start_game_loop()

    def start_game_loop(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()

    def draw_current_table(self, cards:
        """Draws the cards currently played. 
        """

        pass

    def draw_south_cards(self, cards):
        locs = self.get_south_locations(len(cards))
        for idx, card in enumerate(cards):
            ci = CardImage(card=card)
            rect = pygame.Rect(locs[idx], CARD_SIZE)
            pygame_gui.elements.UIImage(
                relative_rect=rect, manager=self.manager, image_surface=ci.img
            )

    def get_south_locations(self, num_cards) -> list:
        """Returns the locations of the South player so that we can view his cards"""
        positions = []
        top_val = 3 * CARD_SIZE[1] + 50
        for i in range(num_cards):
            l = 30 + i * (CARD_SIZE[0] / 2)
            positions.append((l, top_val))
        return positions


class CardImage:
    def __init__(self, card: Card) -> None:
        self.original_size = (868, 1600)
        self.size = CARD_SIZE
        self.card = card
        self.img_src = str(Path(__file__).resolve().parent) + "/img/cards/"
        self.back_side = str(Path(__file__).resolve().parent) + "/img/back-side.png"
        self.img = self.card_to_image(card)

    def card_to_image(self, card: Card) -> str:
        if card is None:
            img = pygame.image.load(self.back_side)
            img.convert()
            return img
        value = card.rank.value
        suit = str(card.suit.name).lower()

        if value < 9:
            value += 2
        else:
            value = str(card.rank.name).lower()
        file = str(value) + "_of_" + suit + ".png"
        path = self.img_src + file
        img = pygame.image.load(path)
        img.convert()
        return img


if __name__ == "__main__":
    ui = UI()

    # card = Card(CardValue(2), Suit(0))
    # print(CardImage(card).img)
