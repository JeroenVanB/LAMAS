import operator
import pygame
from pygame import Color
from pathlib import Path
from card import Card, Suit
from player import Seat
from UI_buttons import RadioButton
from game_model import GameModel


RESOLUTION = (1200, 800)
MSG_BOX_HEIGHT = 200
MSG_LOC = (10, RESOLUTION[1] - MSG_BOX_HEIGHT + 20)
KB_BOX_WIDTH = 600
KB_SUIT_BUTTON_LOC = (RESOLUTION[0] - KB_BOX_WIDTH + 10, 550)
KB_CARD_BUTTON_LOC = (RESOLUTION[0] - KB_BOX_WIDTH + 10, 600)
KB_PLAYER_BOX_SIZE = (110, 24)
KB_PLAYER_LOC = {
    Seat.NORTH: (KB_BOX_WIDTH / 2 - (KB_PLAYER_BOX_SIZE[0] / 2), 40),
    Seat.WEST: (40, (700 - 160) / 2),
    Seat.EAST: (KB_BOX_WIDTH - KB_PLAYER_BOX_SIZE[0] - 40, (700 - 160) / 2),
    Seat.SOUTH: (KB_BOX_WIDTH / 2 - (KB_PLAYER_BOX_SIZE[0] / 2), 700 - 200),
}
LEGEND_LOC = (KB_BOX_WIDTH - 100, 10)
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
PLAYER_COLOR = {
    Seat.NORTH: (255, 0, 0),
    Seat.EAST: (0, 255, 0),
    Seat.SOUTH: (0, 0, 255),
    Seat.WEST: (0, 255, 255),
}


class UI:
    def __init__(self, model: GameModel) -> None:
        pygame.font.init()
        pygame.init()
        self.font_size = 16
        self.font = pygame.font.Font("seguisym.ttf", self.font_size)
        self.big_font = pygame.font.Font("seguisym.ttf", self.font_size + 4)
        self.font_color = pygame.Color(0, 0, 0)
        pygame.display.set_caption("Boeren Bridge")

        self.window_surface = pygame.display.set_mode(RESOLUTION)
        self.background = pygame.Surface(
            (RESOLUTION[0] - KB_BOX_WIDTH, RESOLUTION[1] - MSG_BOX_HEIGHT)
        )
        self.background_color = pygame.Color(50, 168, 82)
        self.background.fill(self.background_color)

        self.msg_box = pygame.Surface((RESOLUTION[0] - KB_BOX_WIDTH, MSG_BOX_HEIGHT))
        self.msg_box.fill(pygame.Color(255, 255, 255))

        self.suit_buttons = [
            RadioButton(
                KB_SUIT_BUTTON_LOC[0],
                KB_SUIT_BUTTON_LOC[1],
                30,
                30,
                self.font,
                "???",
                Suit.HEARTS,
            ),
            RadioButton(
                KB_SUIT_BUTTON_LOC[0] + 35,
                KB_SUIT_BUTTON_LOC[1],
                30,
                30,
                self.font,
                "???",
                Suit.DIAMONDS,
            ),
            RadioButton(
                KB_SUIT_BUTTON_LOC[0] + 70,
                KB_SUIT_BUTTON_LOC[1],
                30,
                30,
                self.font,
                "???",
                Suit.CLUBS,
            ),
            RadioButton(
                KB_SUIT_BUTTON_LOC[0] + 105,
                KB_SUIT_BUTTON_LOC[1],
                30,
                30,
                self.font,
                "???",
                Suit.SPADES,
            ),
        ]
        for rb in self.suit_buttons:
            rb.setRadioButtons(self.suit_buttons)
        self.suit_buttons[0].clicked = True
        self.suit_button_group = pygame.sprite.Group(self.suit_buttons)
        self.selected_suit = None
        self.rank_buttons = []
        self.rank_button_group = None
        self.selected_rank = None

        self.kb_box = pygame.Surface((KB_BOX_WIDTH, RESOLUTION[1]))

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.model = model
        self.start_game_loop()

    def draw_kb_box(self):
        """Initialize and draw all elements in the Kripke model viewer."""
        self.kb_box.fill(pygame.Color(255, 255, 255))  # draw background
        border = pygame.Rect(0, 0, KB_BOX_WIDTH, RESOLUTION[1])
        pygame.draw.rect(self.kb_box, (0, 0, 0), border, width=2)  # draw border
        # Draw title and legend
        title_label = self.big_font.render("Kripke Models", True, self.font_color)
        self.kb_box.blit(title_label, (10, 10))  # draw title
        self.draw_legend()
        # Draw instructions:
        t = [
            "Press the buttons above to switch the Kripke Model.",
            "Press SPACE to go the next move. ",
            "Press ESC to quit.",
        ]
        self.draw_multiline_text(t, (10, 725), self.kb_box)
        # Draw all lines in the Kripke model
        num_lines = self.draw_kb_lines()
        # Draw all worlds and find the true world
        true_world = self.draw_worlds()
        # If there is only one world possible, hide the others
        if num_lines == 0:
            self.hide_player_boxes(true_world=true_world)

        # draw the whole box on the window surface
        self.window_surface.blit(self.kb_box, (RESOLUTION[0] - KB_BOX_WIDTH, 0))

    def draw_worlds(self):
        """Draw all possible player boxes"""
        for seat, loc in KB_PLAYER_LOC.items():
            rect = pygame.Rect(loc, KB_PLAYER_BOX_SIZE)
            surface = pygame.Surface(KB_PLAYER_BOX_SIZE)
            surface.fill((255, 255, 255))
            self.kb_box.blit(surface, rect)
            pygame.draw.rect(self.kb_box, (0, 0, 0), rect, width=1)
            true_world = self.draw_true_world_box()  # draw the true world box
            t = seat.name.capitalize() + " has card"
            self.kb_box.blit(self.font.render(t, True, (0, 0, 0)), (loc[0] + 2, loc[1]))
        return true_world

    def hide_player_boxes(self, true_world: Seat):
        """Hides all worlds except for the true world.

        Args:
            true_world (Seat): The true world
        """
        for seat, loc in KB_PLAYER_LOC.items():
            if seat == true_world:
                continue
            rect = pygame.Rect(loc, KB_PLAYER_BOX_SIZE)
            surface = pygame.Surface(KB_PLAYER_BOX_SIZE)
            surface.fill((255, 255, 255))
            self.kb_box.blit(surface, rect)

    def draw_true_world_box(self):
        """Draws a gold box around the true world in the Kripke Model."""
        if self.selected_rank is None or self.selected_suit is None:
            return None
        c = Color(255, 215, 0)
        card = self.model.deck.get_card_by_rank_and_suit(
            self.selected_rank, self.selected_suit
        )
        if not card:
            return None
        loc = KB_PLAYER_LOC[card.owner.seat]
        rect = pygame.Rect(loc, KB_PLAYER_BOX_SIZE)
        surface = pygame.Surface(KB_PLAYER_BOX_SIZE)
        surface.fill((255, 255, 255))
        pygame.draw.rect(self.kb_box, c, rect, width=2)
        return card.owner.seat

    def draw_suit_rank_buttons(self, event_list):
        """Draws and updates the suit and rank buttons

        Args:
            event_list (list): list of pygame events.
        """
        self.suit_button_group.update(event_list)
        self.suit_button_group.draw(self.window_surface)
        new_suit = self.get_selected_suit()

        # if there are no cards for the suit, select another suit
        kb = self.model.players[0].kb
        if not [card for card in kb.all_cards if card.suit == new_suit]:
            self.select_suit_with_cards()

        if new_suit is not self.selected_suit:
            self.selected_suit = new_suit
            self.draw_kb_card_buttons()

        new_rank = self.get_selected_rank()
        if new_rank is not None:
            if new_rank is not self.selected_rank:
                self.selected_rank = new_rank
        self.rank_button_group.update(event_list)
        self.rank_button_group.draw(self.window_surface)

    def draw_kb_lines(self):
        """Draws all lines from possible states in the Kripke model viewer"""
        num_lines = 0
        if self.selected_rank is None or self.selected_suit is None:
            return num_lines
        for p in self.model.players:
            color = PLAYER_COLOR[p.seat]
            card = Card(self.selected_rank, self.selected_suit)
            knowledge = p.kb.get_card_knowledge(card)
            if not knowledge:
                continue
            # Only keep possible knowledges
            knowledge = {
                seat: value for (seat, value) in knowledge.items() if value == True
            }
            # Draw lines from/to each possible seat
            for (s, v) in knowledge.items():
                for (s2, v2) in knowledge.items():
                    if s == s2:
                        continue
                    start = self.get_line_location(p.seat, knowledge_seat=s)
                    end = self.get_line_location(p.seat, knowledge_seat=s2)
                    pygame.draw.line(self.kb_box, color, start, end, width=3)
                    num_lines += 1
        return num_lines

    def draw_legend(self):
        """Draws the legend in the Kripke Model viewer."""
        # Draw border
        size = (97, 150)
        rect = pygame.Rect(LEGEND_LOC, size)
        surface = pygame.Surface(size)
        surface.fill((255, 255, 255))
        self.kb_box.blit(surface, rect)
        pygame.draw.rect(self.kb_box, (0, 0, 0), rect, width=1)

        # Draw text
        labels = []
        labels.append(self.font.render("Legend:", 1, self.font_color))
        labels.append(self.font.render("True world ???", 1, Color(255, 215, 0)))
        labels.append(self.font.render("North", 1, PLAYER_COLOR[Seat.NORTH]))
        labels.append(self.font.render("East", 1, PLAYER_COLOR[Seat.EAST]))
        labels.append(self.font.render("South", 1, PLAYER_COLOR[Seat.SOUTH]))
        labels.append(self.font.render("West", 1, PLAYER_COLOR[Seat.WEST]))
        for line in range(len(labels)):
            self.kb_box.blit(
                labels[line],
                (LEGEND_LOC[0] + 3, LEGEND_LOC[1] + line * self.font_size + 8 * line),
            )

    def start_game_loop(self):
        """Contains the loop for running the game and drawing the UI."""
        self.clear_table()
        paused = False

        while self.is_running:
            self.clock.tick(60)
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False

            self.draw_kb_box()  # the kripke knowledge screen
            self.draw_suit_rank_buttons(event_list)  # The card selectors

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

    def clear_table(self):
        """Reset the view by drawing the background"""
        self.window_surface.blit(self.background, (0, 0))
        self.window_surface.blit(self.msg_box, (0, RESOLUTION[1] - MSG_BOX_HEIGHT))

    def draw_current_table(self):
        """Draws the cards currently played."""
        for seat, card in self.model.table.items():
            loc = PLAYER_LOC[seat]
            ci = CardImage(card=card, rotate=False)
            rect = pygame.Rect(loc, CARD_SIZE)
            self.window_surface.blit(ci.img, rect)

    def get_selected_suit(self):
        selected_button = [button for button in self.suit_buttons if button.clicked]
        if not selected_button:
            return None
        return selected_button[0].suit

    def get_selected_rank(self):

        selected_button = [button for button in self.rank_buttons if button.clicked]
        if not selected_button:
            return None
        return selected_button[0].rank

    def draw_kb_card_buttons(self):
        """Draws the card selector buttons in the Kripke viewer"""
        # load the knowledge of a player to find all cards still in the game
        kb = self.model.players[0].kb
        suit = self.get_selected_suit()
        cards = [card for card in kb.all_cards if card.suit == suit]
        # draw all sorted ranks for that suit
        cards = sorted(cards, key=operator.attrgetter("rank"))
        self.rank_buttons = []
        for i, card in enumerate(cards):
            self.rank_buttons.append(
                RadioButton(
                    KB_CARD_BUTTON_LOC[0] + i * 53,
                    KB_CARD_BUTTON_LOC[1],
                    48,
                    30,
                    self.font,
                    str(card.rank.name).capitalize(),
                    card.suit,
                    card.rank,
                )
            )
        for rb in self.rank_buttons:
            rb.setRadioButtons(self.rank_buttons)
        if cards:
            self.rank_buttons[0].clicked = True

        self.rank_button_group = pygame.sprite.Group(self.rank_buttons)

    def select_suit_with_cards(self):
        """Selects the first suit that still has cards in the game"""
        kb = self.model.players[0].kb  # load a kb to get all cards
        for suit in Suit:
            cards = [card for card in kb.all_cards if card.suit == suit]
            if cards:
                break

        for s in Suit:
            self.suit_buttons[s].clicked = False
        self.suit_buttons[suit].clicked = True

    def draw_player_cards(self) -> None:
        """Draws all cards that are in each players hand"""
        for player in self.model.players:
            if player.seat in [Seat.NORTH, Seat.SOUTH]:
                locs = self.get_north_south_locations(
                    len(player.cards), seat=player.seat
                )
            else:
                locs = self.get_west_east_locations(len(player.cards), seat=player.seat)
            # rotate the cards if drawing for west and east
            rotate = player.seat in [Seat.WEST, Seat.EAST]

            for idx, card in enumerate(player.cards):
                ci = CardImage(card=card, rotate=rotate)
                rect = pygame.Rect(locs[idx], CARD_SIZE)
                self.window_surface.blit(ci.img, rect)

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
        """Draws the status in the text box."""
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

    def draw_multiline_text(self, text: list, location: tuple, surface=None) -> None:
        """Draws multiline strings since pygame does not support this

        Args:
            text (list): list of lines of strings
            location (tuple): screen location
        """
        label = []
        for line in text:
            label.append(self.font.render(line, True, self.font_color))
        for line in range(len(label)):
            if surface is not None:
                surface.blit(
                    label[line],
                    (location[0], location[1] + (line * self.font_size) + (8 * line)),
                )
            else:
                self.window_surface.blit(
                    label[line],
                    (location[0], location[1] + (line * self.font_size) + (8 * line)),
                )

    def get_line_location(self, seat, knowledge_seat):
        """Gives the location of the start/end of a line in the 'X has card' box.
         X here is the knowledge player, 'player' is the player from which we show the knowledge.

        Args:
            player (Player): The player from which we view the knowledge base
            knowledge_player (Player): The 'X has card' player.

        Returns:
            [tuple(int,int)]: location of the point.
        """
        extra_width = 0
        extra_height = 0
        for s in Seat:
            extra_width += 10
            extra_height += 3
            if s == seat:
                break
        loc = (
            KB_PLAYER_LOC[knowledge_seat][0] + extra_width,
            KB_PLAYER_LOC[knowledge_seat][1] + extra_height,
        )
        return loc

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
        """Compute the locations for drawing the cards for the west and east player

        Args:
            num_cards (int): number of cards
            seat (Seat, optional): Either WEST or EAST. Defaults to Seat.WEST.

        Returns:
            list: locations of the cards on the screen
        """
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
        """Convert a suit name to a small icon

        Args:
            suit (Suit): the suit

        Returns:
            str: the icon
        """
        if suit == Suit.HEARTS:
            return "???"
        elif suit == Suit.DIAMONDS:
            return "???"
        elif suit == Suit.CLUBS:
            return "???"
        elif suit == Suit.SPADES:
            return "???"
        return ""


class CardImage:
    """Image class of the card."""

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
        """Converts the card to an image

        Returns:
            image: pygame image
        """
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
