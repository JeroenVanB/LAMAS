from PIL import Image
import pygame
import pygame_gui
from pathlib import Path
from card import Card, CardValue, Suit
from player import Seat, Player
from typing import List, Tuple
from game_model import GameModel

RESOLUTION = (600, 800)
MSG_BOX_HEIGHT = 200
MSG_LOC = (10, RESOLUTION[1] - MSG_BOX_HEIGHT + 20)
CARD_SIZE = (75, 100)
PLAYER_LOC = {
    # (LEFT, TOP)
    Seat.NORTH: (70 + 2 * CARD_SIZE[0], 40 + CARD_SIZE[1]),
    Seat.EAST: (80 + 3 * CARD_SIZE[0], 50 + 2 * CARD_SIZE[1]),
    Seat.SOUTH: (70 + 2 * CARD_SIZE[0], 60 + 3 * CARD_SIZE[1]),
    Seat.WEST: (60 + CARD_SIZE[0], 50 + 2 * CARD_SIZE[1]),
}
GUESS_LOC = {
    Seat.NORTH: (62 + 2.5 * CARD_SIZE[0], 45 + 2 * CARD_SIZE[1]),
    Seat.EAST: (52 + 3 * CARD_SIZE[0], 37 + 2.5 * CARD_SIZE[1]),
    Seat.SOUTH: (65 + 2.5 * CARD_SIZE[0], 30 + 3 * CARD_SIZE[1]),
    Seat.WEST: (67 + 2 * CARD_SIZE[0], 37 + 2.5 * CARD_SIZE[1]),
}


class UI:
    def __init__(self, model: GameModel) -> None:
        print("Making font object, this can take a few seconds. ", end="")
        pygame.font.init()
        pygame.init()
        # self.big_font = pygame.font.SysFont(None, 20)
        self.font_size = 16
        self.font = pygame.font.Font("seguisym.ttf", self.font_size)
        self.font_color = pygame.Color(0, 0, 0)
        pygame.display.set_caption("Boeren Bridge")

        self.window_surface = pygame.display.set_mode(RESOLUTION)
        self.background = pygame.Surface(
            (RESOLUTION[0], RESOLUTION[1] - MSG_BOX_HEIGHT)
        )
        self.background_color = pygame.Color(50, 168, 82)
        self.background.fill(self.background_color)

        self.msg_box = pygame.Surface((RESOLUTION[0], MSG_BOX_HEIGHT))
        self.msg_box.fill(pygame.Color(255, 255, 255))
        # self.manager = pygame_gui.UIManager(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.model = model
        self.start_game_loop()

    def start_game_loop(self):
        self.clear_table()
        paused = False

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Space pressed")
                        paused = False
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False

            if not paused:
                if self.model.finished:
                    exit(0)
                # Go to the next game state
                self.model.next_move()
                self.clear_table()  # draw background
                self.draw_current_table()  # draw played cards of each player
                self.draw_player_cards()
                self.draw_game_info()
                self.draw_score_info()
                self.draw_guesses()
                self.draw_message()
                paused = True

                pygame.display.update()
                self.clock.tick(60)

    def clear_table(self):
        """Reset the view by drawing the background"""
        self.window_surface.blit(self.background, (0, 0))
        self.window_surface.blit(self.msg_box, (0, RESOLUTION[1] - MSG_BOX_HEIGHT))
        pygame.display.update()

    def draw_current_table(self):
        """Draws the cards currently played."""
        for seat, card in self.model.table.items():
            loc = PLAYER_LOC[seat]
            ci = CardImage(card=card, rotate=False)
            rect = pygame.Rect(loc, CARD_SIZE)
            self.window_surface.blit(ci.img, rect)
        pygame.display.update()

    def draw_player_cards(self) -> None:
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

    def draw_score_info(self) -> None:
        """Draws player score information"""
        location = (PLAYER_LOC[Seat.EAST][0] + CARD_SIZE[0] + 100, 20)
        n = [p.score for p in self.model.players if p.seat == Seat.NORTH][0]
        e = [p.score for p in self.model.players if p.seat == Seat.EAST][0]
        s = [p.score for p in self.model.players if p.seat == Seat.SOUTH][0]
        w = [p.score for p in self.model.players if p.seat == Seat.WEST][0]
        text = ["Scores", f"North: {n}", f"East: {e}", f"South: {s}", f"West: {w}"]
        self.draw_multiline_text(text, location)

    def draw_guesses(self) -> None:
        """Draw all player trick guesses on the screen"""
        for p in self.model.players:
            loc = GUESS_LOC[p.seat]
            label = self.font.render(
                str(p.wins) + "/" + str(p.guessed_wins), True, self.font_color
            )
            self.window_surface.blit(label, loc)

    def draw_message(self) -> None:
        self.draw_multiline_text(self.model.status, location=MSG_LOC)

    def draw_game_info(self) -> None:
        """Draws information about the current round and trick"""
        trump_ico = self.suit_to_icon(self.model.trump)
        trick_suit_ico = self.suit_to_icon(self.model.trick_suit)
        location = (PLAYER_LOC[Seat.EAST][0] + CARD_SIZE[0], 20)
        # resolve possible index out of bounds error
        if self.model.cur_round >= len(self.model.cards_per_round):
            total_tricks = self.model.cards_per_round[self.model.cur_round - 1]
        else:
            total_tricks = self.model.cards_per_round[self.model.cur_round]

        text = ["Game"]
        text.append(
            f"Round: {self.model.cur_round + 1}/{len(self.model.cards_per_round)}"
        )
        text.append(f"Trick: {self.model.cur_trick + 1}/{total_tricks}")
        text.append(f"Trump: {trump_ico}")
        text.append(f"Trick suit: {trick_suit_ico}")
        self.draw_multiline_text(text, location)

    def draw_multiline_text(self, text: list, location: tuple) -> None:
        """Draws multiline strings since pygame does not support this

        Args:
            text (list): list of lines of strings
            location (tuple): screen location
        """
        label = []
        for line in text:
            label.append(self.font.render(line, True, self.font_color))
        for line in range(len(label)):
            self.window_surface.blit(
                label[line],
                (location[0], location[1] + (line * self.font_size) + (8 * line)),
            )

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

    def suit_to_icon(self, suit: Suit) -> str:
        if suit == Suit.HEARTS:
            return "♥"
        elif suit == Suit.DIAMONDS:
            return "♦"
        elif suit == Suit.CLUBS:
            return "♣"
        elif suit == Suit.SPADES:
            return "♠"
        return ""


class CardImage:
    def __init__(self, card: Card, rotate: bool, closed=False) -> None:
        self.original_size = (868, 1600)
        self.size = CARD_SIZE
        self.card = card
        self.rotate = rotate
        self.closed = closed
        self.img_src = str(Path(__file__).resolve().parent) + "/img/cards/"
        self.back_side = str(Path(__file__).resolve().parent) + "/img/back-side.png"
        self.placeholder = str(Path(__file__).resolve().parent) + "/img/placeholder.png"
        self.img = self.card_to_image()

    def card_to_image(self) -> str:
        if self.card is None:
            img = pygame.image.load(self.placeholder)
        elif self.closed:
            img = pygame.image.load(self.back_side)
        else:
            value = self.card.rank.value
            suit = str(self.card.suit.name).lower()

            if value < 9:  # value iteration starts at 0 so we have to adjust
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
    # img = Image.new("RGB", CARD_SIZE, (105, 105, 105))
    # img.show()
    # img.save("img/placeholder.png")

    model = GameModel()
    ui = UI(model)

    # card = Card(CardValue(2), Suit(0))
    # print(CardImage(card).img)
