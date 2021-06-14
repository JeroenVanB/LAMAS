import sys
from random_player import RandomPlayer
from greedy_player import GreedyPlayer
from greedy_kripke_player import GreedyKripkePlayer
from game_model import GameModel
from UI import UI

if len(sys.argv) == 1:
    ui = UI(GameModel())
else:
    # Run experiments

    num_games = int(sys.argv[1])
    scores = {"greedy": 0, "greedy_kripke": 0, "random": 0}
    model = GameModel()
    print(f"Playing {num_games} games with {[type(p) for p in model.players]}")
    for game in range(num_games):
        model = GameModel()

        while not model.finished:
            model.next_move()

        # get scores
        for p in model.players:
            if type(p) == GreedyKripkePlayer:
                scores["greedy_kripke"] += p.score / 2
            elif type(p) == GreedyPlayer:
                scores["greedy"] += p.score / 2
            elif type(p) == RandomPlayer:
                scores["random"] += p.score / 2
    print(f"\nAverage score over {num_games} games per player.")
    for k, v in scores.items():
        print(k, " \t\tscored ", v / num_games)
