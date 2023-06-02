import sys

from games.game_simulator import GameSimulator
from games.Stymie.simulator import StymieSimulator
from games.Stymie.players.greedy_move_middle import GreedyMoveStymiePlayer
from games.Stymie.players.greedy_eat_pieces import GreedyEatStymiePlayer
from games.Stymie.players.random_bot import RandomStymiePlayer
from games.Stymie.players.human import HumanStymiePlayer
from games.Stymie.players.minimax import MinimaxStymiePlayer


def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(0, iterations):
        simulator.change_player_positions()
        simulator.run_simulation()

    print("Results for the game:")
    simulator.print_stats()

def main():
    while True:
        print("\n")
        print("ESTG IA Games Simulator - Stymie")
        print("*******Stymie*******")
        print("Autores: 24844 -- Nelson Novais -- 28236 -- Guilherme Pinto")
        print("Informações sobre o jogo: https://www.boardspace.net/stymie/english/stymie-rules.pdf")
        print("\n")
        print("Bem-vindo ao menu!")
        print("Por favor, escolha duas opções:")
        print("1 - Fácil (Greedy Eat)")
        print("2 - Médio (Greedy Move)")
        print("3 - Difícil (Minimax)")
        print("4 - Aleatório (Random)")
        print("5 - Humano (Human)")
        print("0 - Sair")

        option1 = None
        option2 = None

        while option1 is None:
            try:
                option1 = int(input("Digite o número do primeiro jogador: "))
                if option1 == 0:
                    sys.exit()
                if option1 not in [1, 2, 3, 4, 5]:
                    print("Opção inválida. Por favor, escolha um número de 1 a 5.")
                    option1 = None
            except ValueError:
                print("Opção inválida. Por favor, digite um número.")

        while option2 is None:
            try:
                option2 = int(input("Digite o número do segundo jogador: "))
                if option2 not in [1, 2, 3, 4, 5]:
                    print("Opção inválida. Por favor, escolha um número de 1 a 5.")
                    option2 = None
                elif option2 == option1:
                    print("Por favor, escolha duas opções diferentes.")
                    option2 = None
            except ValueError:
                print("Opção inválida. Por favor, digite um número.")
        player1 = None
        player2 = None
        x = input("Nº iterations: ")
        num_iterations = int(x)
        if option1 == 1:
            player1 = GreedyEatStymiePlayer("facil1")
        elif option1 == 2:
            player1 = GreedyMoveStymiePlayer("medio1")
        elif option1 == 3:
            player1 = MinimaxStymiePlayer("dificil1")
        elif option1 == 4:
            player1 = RandomStymiePlayer("random1")
        elif option1 == 5:
            player1 = HumanStymiePlayer("humano1")

        if option2 == 1:
            player2 = GreedyEatStymiePlayer("facil2")
        elif option2 == 2:
            player2 = GreedyMoveStymiePlayer("medio2")
        elif option2 == 3:
            player2 = MinimaxStymiePlayer("dificil2")
        elif option2 == 4:
            player2 = RandomStymiePlayer("random2")
        elif option2 == 5:
            player2 = HumanStymiePlayer("humano2")

        stymie_simulations = [
            {
                "name": f"Stymie - {option1} VS {option2}",
                "player1": player1,
                "player2": player2
            }
        ]
        for sim in stymie_simulations:
            run_simulation(sim["name"], StymieSimulator(sim["player1"], sim["player2"]), num_iterations)


if __name__ == "__main__":
    main()
