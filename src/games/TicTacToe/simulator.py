from games.game_simulator import GameSimulator
from games.TicTacToe.player import TicTacToePlayer
from games.TicTacToe.state import TicTacToeState


class TicTacToeSimulator(GameSimulator):

    def __init__(self, player1: TicTacToePlayer, player2: TicTacToePlayer, size: int = 4):
        super(TicTacToeSimulator, self).__init__([player1, player2])
        """
        the number of rows and cols from the TicTacToe grid
        """
        self.__num_rows = size
        self.__num_cols = size

    def init_game(self):
        return TicTacToeState(self.__num_rows)

    def before_end_game(self, state: TicTacToeState):
        # ignored for this simulator
        pass

    def end_game(self, state: TicTacToeState):
        # ignored for this simulator
        pass
