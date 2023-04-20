
from games.game_simulator import GameSimulator
from games.poker.players.always_bet import AlwaysBetKuhnPokerPlayer
from games.poker.players.always_bet_king import AlwaysBetKingKuhnPokerPlayer
from games.poker.players.always_pass import AlwaysPassKuhnPokerPlayer
from games.poker.players.cfr import CFRKuhnPokerPlayer
from games.poker.players.random import RandomKuhnPokerPlayer
from games.poker.simulator import KuhnPokerSimulator
from games.poker.players.NelsonPoker import NelsonPoker

from games.TicTacToe.simulator import TicTacToeSimulator
from games.TicTacToe.players.Nelson import Nelson4Player
from games.TicTacToe.players.human import HumanTicTacToePlayer
from games.TicTacToe.players.random import RandomTicTacToePlayer
from games.TicTacToe.players.Ofencivegreedy import OffGreedyTicTacToePlayer
from games.TicTacToe.players.Defencivegreedy import DefGreedyTicTacToePlayer
from games.TicTacToe.players.Offminimax import OffMinimaxTicTacToePlayer
from games.TicTacToe.players.minimax import OffMinimaxTicTacToePlayer
from games.TicTacToe.players.Defminimax import DefMinimaxTicTacToePlayer
from games.Stymie.simulator import StymieSimulator
from games.Stymie.players.human import HumanStymiePlayer
from games.Stymie.players.random import RandomStymiePlayer


def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(0, iterations):
        simulator.change_player_positions()
        simulator.run_simulation()

    print("Results for the game:")
    simulator.print_stats()


def main():
    print("ESTG IA Games Simulator")

    num_iterations = 100

    stymie_simulations = [
        {
            "name": "TicTacToe - Human VS Random",
            "player1": RandomStymiePlayer("Random 1"),
            "player2": RandomStymiePlayer("Random 2")
        },
    ]



    for sim in stymie_simulations:
        run_simulation(sim["name"], StymieSimulator(sim["player1"], sim["player2"]), num_iterations)

if __name__ == "__main__":
    main()
