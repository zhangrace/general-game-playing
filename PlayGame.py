#! /usr/bin/env python3
########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2018, Swarthmore College
########################################
# NOTE: you should not need to modify this file.
########################################

from argparse import ArgumentParser

from Hex import HexGame
from Breakthrough import Breakthrough
from Mancala import Mancala
from MysteryGames import MysteryGame0, MysteryGame1
from BasicPlayers import HumanPlayer, RandomPlayer
from HexPlayerBryce import HexPlayerBryce
from TournamentPlayers import BreakthroughTournamentPlayer, \
                               MancalaTournamentPlayer
from MonteCarloTreeSearch import MCTSPlayer

games = {"hex":HexGame,
         "mancala":Mancala,
         "breakthrough":Breakthrough,
         "mystery0":MysteryGame0,
         "mystery1":MysteryGame1}

players = {"random":RandomPlayer,
           "human":HumanPlayer,
           "mcts":MCTSPlayer,
           "bryce":HexPlayerBryce,
           "tournament":"tournament"}

tournament_players = {"mancala":MancalaTournamentPlayer,
                     "breakthrough":BreakthroughTournamentPlayer}

def main():
    args = parse_args()
    if args.p1 == "tournament":
        p1 = tournament_players[args.game]()
    else:
        if args.p1 == "bryce":
            assert args.game == "hex", "HexPlayerBryce only plays Hex"
        p1 = players[args.p1](*args.a1)
    if args.p2 == "tournament":
        p2 = tournament_players[args.game]()
    else:
        if args.p2 == "bryce":
            assert args.game == "hex", "HexPlayerBryce only plays Hex"
        p2 = players[args.p2](*args.a2)
    game = games[args.game](*args.game_args)

    if args.games == 1:
        play_game(game, p1, p2, True)
    else:
        p1_wins = 0
        p2_wins = 0
        draws = 0
        for i in range(args.games):
            if i % 2:
                result = play_game(game, p1, p2, False)
                if result.winner == 1:
                    p1_wins += 1
                elif result.winner == -1:
                    p2_wins += 1
                else:
                    draws += 1
            else:
                result = play_game(game, p2, p1, False)
                if result.winner == -1:
                    p1_wins += 1
                elif result.winner == 1:
                    p2_wins += 1
                else:
                    draws += 1
        print("results after", args.games, "games:")
        print(p1_wins, "wins for player 1 (" + p1.name + ")")
        print(p2_wins, "wins for player 2 (" + p2.name + ")")
        if draws > 0:
            print(draws, "draws")

def parse_args():
    p = ArgumentParser()
    p.add_argument("game", type=str, choices=list(games.keys()),
                   help="Game to be played.")
    p.add_argument("p1", type=str, choices=list(players.keys()),
                   help="Player 1 type.")
    p.add_argument("p2", type=str, choices=list(players.keys()),
                   help="Player 2 type.")
    p.add_argument("-a1", nargs="*", type=float, default=[],
                   help="Arguments for player 1.")
    p.add_argument("-a2", nargs="*", type=float, default=[],
                   help="Arguments for player 2.")
    p.add_argument("-games", type=int, default=1,
                   help="Number of games to play.")
    p.add_argument("-game_args", type=int, nargs="*", default=[],
                   help="Optional arguments to pass to the game constructor, "+
                   "such as board dimensions. Must be listed in order.")
    return p.parse_args()

def play_game(game, player1, player2, show=False):
    """Plays a game then returns the final state."""
    while not game.isTerminal:
        if show:
            print(game)
        if game.turn == 1:
            m = player1.getMove(game)
        else:
            m = player2.getMove(game)
        if m not in game.availableMoves:
            raise Exception("invalid move: " + str(m))
        game = game.makeMove(m)
    if show:
        print(game, "\n")
        if game.winner != 0:
            print("player", game._print_char(game.winner), "(", end='')
            print((player1.name if game.winner == 1 else player2.name)+") wins")
        else:
            print("it's a draw")
    return game

if __name__ == "__main__":
    main()
