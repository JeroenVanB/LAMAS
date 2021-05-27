import pygame
from pathlib import Path
from card import Card, CardValue, Suit


class UI:
    img_src = str(Path(__file__).resolve().parent) + "/img/cards/"
    back_side = str(Path(__file__).resolve().parent) + "/img/back-side.png"

    def card_to_image(self, card: Card) -> str:
        value = card.rank.value
        suit = str(card.suit.name).lower()

        if value < 9:
            value += 2
        else:
            value = str(card.rank.name).lower()
        file = str(value) + "_of_" + suit + ".png"
        path = self.img_src + file
        return path


if __name__ == "__main__":
    ui = UI()

    card = Card(CardValue(2), Suit(0))
    print(ui.card_to_image(card))
