from games.game_simulator import GameSimulator
from games.Stymie.state import StymieState

from games.Stymie.player import StymiePlayer


class StymieSimulator(GameSimulator):

    def __init__(self, player1: StymiePlayer, player2: StymiePlayer, size: int = 7):
        super(StymieSimulator, self).__init__([player1, player2])
        """
        the number of rows and cols from the TicTacToe grid
        """
        self.__num_rows = size
        self.__num_cols = size

    def init_game(self):
        return StymieState(self.__num_rows)

    def before_end_game(self, state: StymieState):
        # ignored for this simulator
        pass

    def end_game(self, state: StymieState):
        # ignored for this simulator
        pass
