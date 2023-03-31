from random import choice
from games.TicTacToe.action import TicTacToeAction
from games.TicTacToe.player import TicTacToePlayer
from games.TicTacToe.state import TicTacToeState
from games.state import State


class DefGreedyTicTacToePlayer(TicTacToePlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: TicTacToeState):
        grid = state.get_grid()
        select_row = None
        selected_col = None
        aux_col = None
        aux_row = None
        max_count = 0
        aux = state.clone()
        for col in range(0, state.get_num_cols()):
            count = 0
            for row in range(0, state.get_num_rows()):
                if self.get_current_pos() != grid[col][row] and grid[col][row] != -1:
                    aux_col = col
                    aux_row = row
                if not state.validate_action(TicTacToeAction(col, row)):
                    continue
                count_aux = 0
                for i in range(state.get_num_cols()):
                    if grid[i][row] != self.get_current_pos():
                        count_aux += 1
                    elif grid[i][row] == -1:
                        count_aux -= 1
                    if count_aux == 2:
                        if col < 2:
                            if not state.validate_action(TicTacToeAction(col+1, row)):
                                return TicTacToeAction(col, row)
                            else:
                                return TicTacToeAction(col+1, row)
                if count_aux == 2:
                    return TicTacToeAction(col, row)

                count_aux = 0
                for j in range(state.get_num_rows()):
                    if grid[col][j] != self.get_current_pos() and grid[col][j] != -1:
                        count_aux  += 1
                    elif grid[col][j] != -1:
                        count_aux -= 1
                    if count_aux == 2:
                        if row < 2:
                            if not state.validate_action(TicTacToeAction(col, row+1)):
                                return TicTacToeAction(col, row)
                            else:
                                return TicTacToeAction(col, row+1)
                    if count_aux == 2:
                        return TicTacToeAction(col, row)
                if aux_col == col:
                    count += 4
                if grid[col][row] != self.get_current_pos() and grid[col][row] != -1:
                     count += 6
                if grid[row][col] == self.get_current_pos():
                    count -= 4
                else:
                    count = 0
                if selected_col is None or select_row is None or count > max_count or (count == max_count and choice([False, True])):
                    selected_col = col
                    select_row = row
                    max_count = count
        for row in range(0, state.get_num_rows()):
            count = 0
            for col in range(0, state.get_num_cols()):

                if self.get_current_pos() != grid[col][row] and grid[col][row] != -1:
                    aux_col = col
                    aux_row = row
                if not state.validate_action(TicTacToeAction(col, row)):
                    continue
                if aux_row == row:
                    count += 4
                if grid[col][row] != self.get_current_pos() and grid[col][row] != -1:
                     count += 6
                if grid[col][row] == self.get_current_pos():
                    count -= 4
                # it swap the column if we exceed the count. if the count of chips is the same, we swap 50% of the times
                if selected_col is None or select_row is None or count > max_count or (count == max_count and choice([False, True])):
                    selected_col = col
                    select_row = row
                    max_count = count

        if selected_col is None:
            raise Exception("There is no valid action")
        if select_row is None:
            raise Exception("There is no valid action")
        print("aqui1")
        return TicTacToeAction(selected_col, select_row)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
