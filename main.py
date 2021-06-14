from full_kripke_player import FullKripkePlayer
import sys
from random_player import RandomPlayer
from greedy_player import GreedyPlayer
from greedy_kripke_player import GreedyKripkePlayer
from game_model import GameModel
from UI import UI
from tqdm import tqdm

if len(sys.argv) == 1:
    ui = UI(GameModel())
else:
    # Run experiments

    num_games = int(sys.argv[1])
    scores = {"greedy": 0, "greedy_kripke": 0, "full_kripke": 0, "random": 0}

    players = ["full_kripke", "full_kripke", "greedy", "greedy"]
    model = GameModel(players=players)
    print(f"Playing {num_games} games with {[type(p) for p in model.players]}")
    for game in tqdm(range(num_games)):
        # At the half of the games, we switch the players to remove the advantage of being NORTH
        if game == num_games / 2:
            players.reverse()

        model = GameModel(players=players)
        while not model.finished:
            model.next_move()

        # get scores
        for p in model.players:
            if type(p) == GreedyKripkePlayer:
                scores["greedy_kripke"] += p.score / 2
            elif type(p) == FullKripkePlayer:
                scores["full_kripke"] += p.score / 2
            elif type(p) == GreedyPlayer:
                scores["greedy"] += p.score / 2
            elif type(p) == RandomPlayer:
                scores["random"] += p.score / 2
    print(f"\nAverage score over {num_games} games per player.")
    for k, v in scores.items():
        print(k, " \t\tscored ", v / num_games)
