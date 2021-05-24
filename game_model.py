from player import Player, Seat
from deck import Deck
from card import Suit
import sys
import random


class GameModel():
    
    def __init__(self):
        #TODO determine rounds/cards per round
        self.rounds = 1
        self.cards_per_round = [4]
        self.players = [Player(i, Seat(i)) for i in range(4)]
        self.deck = Deck()
        
    def start_game(self):
        for round in range(self.rounds):
            self.play_round(round, self.cards_per_round[round])

    def play_round(self, round, n_cards):
        print('=== Round', round, 'with', n_cards, 'cards',  '===')
        self.deal_cards(n_cards)
        trump = self.pick_trump()
        print('Trump is ', trump)
        for trick in range(n_cards):
            print('--- Trick', trick+1, '/', n_cards , '---')
            # Determine which player starts
            opener = self.get_opener()
            self.order_players(opener)
            # print('The opener is', opener.name)
            print('Player Order : ', [p.seat for p in self.players])

            # TODO make a guess

            # Every player plays a card in order
            played_cards = []
            for idx, p in enumerate(self.players):
                card = p.play_card()
                if idx == 0:
                    trick_suit = card.suit
                    print('Trick suit is :', trick_suit)
                played_cards.append(card)
            # print('cards played', [t.name for t in played_cards])

            # Determine the winner of the trick
            # This is determined using the played_cards and the trick_suit
            self.determine_winner(played_cards, trick_suit)

    def deal_cards(self, n_cards):
        # Get a deck of cards
        self.deck.reset_deck(n_cards)
        print(len(self.deck.cards))
        print(len(self.players)*n_cards)
        assert(len(self.deck.cards) == len(self.players)*n_cards)
        # assert(len(self.deck.cards) == len(self.players)*n_cards)
        for idx, p in enumerate(self.players):
            p.set_cards(self.deck.cards[idx*n_cards:(1+idx)*n_cards])
            # print('player', p.seat, 'has', p.cards)
        # for p in self.players:

            

    def get_opener(self):
        for player in self.players:
            if player.opener:
                return player
        print('Error: Opener could not be found')
        sys.exit(1)

    def order_players(self, opener):
        idx = self.players.index(opener)
        self.players = self.players[-idx:] + self.players[:-idx]

    def pick_trump(self):
        return Suit(random.randint(0, 3))
                
    def determine_winner(self, played_cards, trick_suit):
        for c in played_cards:
            pass

if __name__ == '__main__':
    game_model = GameModel()
    game_model.start_game()

