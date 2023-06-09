from typing import Optional
from games.state import State

from games.TicTacToe.action import TicTacToeAction
from games.TicTacToe.result import TicTacToeResult


class TicTacToeState(State):
    EMPTY_CELL = -1

    def __init__(self,grid: int):
        super().__init__()
        if grid < 3:
            raise Exception("the number of cols must be 3 or over")
        """
        the dimensions of the board
        """
        self.__num_rows = grid
        self.__num_cols = grid
        """
        the grid
        """
        self.__grid = [[TicTacToeState.EMPTY_CELL for _i in range(self.__num_cols)] for _j in range(self.__num_rows)]

        """
        counts the number of turns in the current game
        """
        self.__turns_count = 1

        """
        the index of the current acting player
        """
        self.__acting_player = 0

        """
        determine if a winner was found already 
        """
        self.__has_winner = False

    def __check_winner(self, player):
        # check for 4 across
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols - 2):
                if self.__grid[row][col] == player and \
                        self.__grid[row][col + 1] == player and \
                        self.__grid[row][col + 2] == player:
                    return True

        # check for 4 up and down
        for row in range(0, self.__num_rows - 2):
            for col in range(0, self.__num_cols):
                if self.__grid[row][col] == player and \
                        self.__grid[row + 1][col] == player and \
                        self.__grid[row + 2][col] == player:
                    return True

        # check upward diagonal
        for row in range(2, self.__num_rows):
            for col in range(0, self.__num_cols - 2):
                if self.__grid[row][col] == player and \
                        self.__grid[row - 1][col + 1] == player and \
                        self.__grid[row - 2][col + 2] == player:
                    return True

        # check downward diagonal
        for row in range(0, self.__num_rows - 2):
            for col in range(0, self.__num_cols - 2):
                if self.__grid[row][col] == player and \
                        self.__grid[row + 1][col + 1] == player and \
                        self.__grid[row + 2][col + 2] == player:
                    return True

        return False

    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2

    def validate_action(self, action: TicTacToeAction) -> bool:
        col = action.get_col()
        row = action.get_row()
        # valid column
        if col < 0 or col >= self.__num_cols:
            return False
        if row < 0 or row >= self.__num_rows:
            return False
        # full column
        if self.__grid[row][col] != TicTacToeState.EMPTY_CELL:
            return False

        return True

    def update(self, action: TicTacToeAction):
        col = action.get_col()
        row = action.get_row()

        self.__grid[row][col] = self.__acting_player

        # determine if there is a winner
        self.__has_winner = self.__check_winner(self.__acting_player)

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1

    def __display_cell(self, row, col):
        print({
                  0: 'X',
                  1: 'O',
                  TicTacToeState.EMPTY_CELL: ' '
              }[self.__grid[row][col]], end="")

    def __display_numbers(self):

        for col in range(0, self.__num_cols):
            if col < 10:
                print('', end="")
            if col == 0:
                print(" ",col, end="")
            else:
                print("",col, end="")
        print("")
    def __display_separator(self):
        for col in range(0, self.__num_cols):
            print("---", end="")
        print("-")

    def display(self):
        print(" ", end="")
        self.__display_numbers()
        self.__display_separator()

        for row in range(0, self.__num_rows):
            print(row,'|', end="")
            for col in range(0, self.__num_cols):
                self.__display_cell(row, col)
                print('|', end="")

            print("")
            self.__display_separator()
        print(" ", end="")
        self.__display_numbers()
        print("")

    def __is_full(self):
        return self.__turns_count > (self.__num_cols * self.__num_rows)

    def is_finished(self) -> bool:
        return self.__has_winner or self.__is_full()

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = TicTacToeState(self.__num_rows)
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                cloned_state.__grid[row][col] = self.__grid[row][col]
        return cloned_state

    def get_result(self, pos) -> Optional[TicTacToeResult]:
        if self.__has_winner:
            return TicTacToeResult.LOOSE if pos == self.__acting_player else TicTacToeResult.WIN
        if self.__is_full():
            return TicTacToeResult.DRAW
        return None

    def get_num_rows(self):
        return self.__num_rows

    def get_num_cols(self):
        return self.__num_cols

    def before_results(self):
        pass

    def get_possible_actions(self):
        actions = []
        for i in range(0,self.__num_rows):
            for j in range(0,self.__num_cols):
                action = TicTacToeAction(i,j)
                if self.validate_action(action):
                    actions.append(action)
        return actions

    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state
