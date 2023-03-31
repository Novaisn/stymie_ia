import sys

from random import choice
from games.TicTacToe.action import TicTacToeAction
from games.TicTacToe.player import TicTacToePlayer
from games.TicTacToe.result import TicTacToeResult
from games.TicTacToe.state import TicTacToeState
from games.state import State


class Nelson4Player(TicTacToePlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: TicTacToeState):
        grid = state.get_grid()

        selected_col = None
        max_count = 0

        for col in range(0, state.get_num_cols()):
            if not state.validate_action(TicTacToeAction(col)):
                continue

            count = 0
            for row in range(0, state.get_num_rows()):
                if grid[row][col] == (self.get_current_pos()):
                    count += 3
                if grid[row][3] == (self.get_current_pos() is None):
                    count += 2
                if grid[3][col] == (self.get_current_pos() is None):
                    count += 2



            # it swap the column if we exceed the count. if the count of chips is the same, we swap 50% of the times
            if selected_col is None or count > max_count or (count == max_count and choice([False, True])):
                selected_col = col
                max_count = count

        if selected_col is None:
            raise Exception("There is no valid action")

        return TicTacToeAction(selected_col)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass