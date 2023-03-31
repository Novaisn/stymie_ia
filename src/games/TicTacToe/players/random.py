from random import randint
from games.state import State
from games.TicTacToe.player import TicTacToePlayer

from games.TicTacToe.state import TicTacToeState

from games.TicTacToe.action import TicTacToeAction


class RandomTicTacToePlayer(TicTacToePlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: TicTacToeState):
        return TicTacToeAction(randint(0, state.get_num_cols()), randint(0, state.get_num_rows()))

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
