from full_kripke_player import FullKripkePlayer
import sys
from random_player import RandomPlayer
from greedy_player import GreedyPlayer
from greedy_kripke_player import GreedyKripkePlayer
from game_model import GameModel
from UI import UI
from tqdm import tqdm
from statistics import mean, stdev

if len(sys.argv) == 1:
    ui = UI(GameModel())
else:
    # Run experiments

    num_games = int(sys.argv[1])
    scores = {"greedy": [], "greedy_kripke": [], "full_kripke": [], "random": []}

    players = ["full_kripke", "greedy_kripke", "greedy", "random"]
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
                scores["greedy_kripke"].append(p.score)
            elif type(p) == FullKripkePlayer:
                scores["full_kripke"].append(p.score)
            elif type(p) == GreedyPlayer:
                scores["greedy"].append(p.score)
            elif type(p) == RandomPlayer:
                scores["random"].append(p.score)
    print(f"\nAverage score over {num_games} games per player.")
    for k, v in scores.items():
        if v:
            print(k, " \t\tscored ", mean(v), "\t\tstd", stdev(v), "\t\tlowest", min(v), "\t\tmax", max(v))
