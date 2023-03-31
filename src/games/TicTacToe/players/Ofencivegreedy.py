from random import choice
from games.TicTacToe.action import TicTacToeAction
from games.TicTacToe.player import TicTacToePlayer
from games.TicTacToe.state import TicTacToeState
from games.state import State


class OffGreedyTicTacToePlayer(TicTacToePlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: TicTacToeState):
        grid = state.get_grid()
        select_row = None
        selected_col = None
        max_count = 0

        for col in range(0, state.get_num_cols()):


            count = 0
            for row in range(0, state.get_num_rows()):

                if not state.validate_action(TicTacToeAction(col, row)):
                    continue
                if grid[row][col] == self.get_current_pos():
                    count += 1

                # it swap the column if we exceed the count. if the count of chips is the same, we swap 50% of the times
                if selected_col is None or count > max_count or (count == max_count and choice([False, True])):
                    selected_col = col
                    select_row = row
                    max_count = count
            for row in range(0, state.get_num_cols()):

                count = 0
                for col in range(0, state.get_num_rows()):

                    if not state.validate_action(TicTacToeAction(col, row)):
                        continue
                    if grid[row][col] == self.get_current_pos():
                        print(self.get_current_pos())
                        count += 1

                    # it swap the column if we exceed the count. if the count of chips is the same, we swap 50% of the times
                    if selected_col is None or count > max_count or (count == max_count and choice([False, True])):
                        selected_col = col
                        select_row = row
                        max_count = count
        if selected_col is None:
            raise Exception("There is no valid action")
        if select_row is None:
            raise Exception("There is no valid action")

        return TicTacToeAction(selected_col, select_row)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass
    def event_end_game(self, final_state: State):
        # ignore
        pass
