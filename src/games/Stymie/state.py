from typing import Optional
from games.state import State

from games.Stymie.action import StymieAction
from games.Stymie.result import StymieResult

from games.Stymie.action import StymiePlacementAction

from games.Stymie.action import StymieInPlayAction


class StymieState(State):
    EMPTY_CELL = -1

    def __init__(self, grid: int):
        super().__init__()
        self._stage = "placement"

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
        self.__grid = [[StymieState.EMPTY_CELL for _i in range(self.__num_cols)] for _j in range(self.__num_rows)]

        center_row = self.__num_rows // 2
        center_col = self.__num_cols // 2
        center_piece = 3
        self.__grid[center_col][center_row] = center_piece
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
    def __check_can_place(self):
        arraynotplace = []
        arrayspaces = []
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                arrayspaces.append((row, col))
                if self.__grid[row][col] != StymieState.EMPTY_CELL:
                    arraynotplace.append((row,col))
                    if row - 1 < self.__num_rows and col - 1 < self.__num_cols:
                        arraynotplace.append((row-1, col-1))
                    if row -1 < self.__num_rows and col < self.__num_cols:
                        arraynotplace.append((row-1, col))
                    if row < self.__num_rows and col -1 < self.__num_cols:
                        arraynotplace.append((row, col-1))
                    if row +1 < self.__num_rows and col +1 < self.__num_cols:
                        arraynotplace.append((row+1, col+1))
                    if row +1 < self.__num_rows and col < self.__num_cols:
                        arraynotplace.append((row+1, col))
                    if row < self.__num_rows and col+1 < self.__num_cols:
                        arraynotplace.append((row, col+1))
                    if row - 1 < self.__num_rows and col + 1 < self.__num_cols:
                        arraynotplace.append((row-1, col +1))
                    if row +1 < self.__num_rows and col -1 < self.__num_cols:
                        arraynotplace.append((row+1, col-1))

        set1 = set(arraynotplace)
        set2 = set(arrayspaces)
        diff = set2 -set1
        print("Not",len(arraynotplace))
        print("Spacce",len(arrayspaces))
        print("Diff",diff)
        itens = []
        for item in diff:
            itens.append(item)
        if len(itens)==0:
            return False
        if len(arraynotplace) == len(arrayspaces):
            return False


        if arraynotplace != arrayspaces:
            return True
        else:
            return False

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

    def validate_place_action(self, action: StymiePlacementAction) -> bool:
        col = action.get_col()
        row = action.get_row()
        # valid column
        if col < 0 or col >= self.__num_cols:
            return False
        if row < 0 or row >= self.__num_rows:
            return False
        # full column
        if self.__grid[row][col] != StymieState.EMPTY_CELL:
            return False
        # adjacent
        if row-1 < self.__num_rows and col-1 < self.__num_cols:
            if self.__grid[row - 1][col - 1] != StymieState.EMPTY_CELL:
                return False
        if row-1 < self.__num_rows and col < self.__num_cols:
            if self.__grid[row - 1][col] != StymieState.EMPTY_CELL:
                return False
        if row < self.__num_rows and col-1 < self.__num_cols:
            if self.__grid[row][col - 1] != StymieState.EMPTY_CELL:
                return False
        if row + 1 < self.__num_rows and col+1 < self.__num_cols:
            if self.__grid[row + 1][col + 1] != StymieState.EMPTY_CELL:
                return False
        if row + 1 < self.__num_rows and col < self.__num_cols:
            if self.__grid[row + 1][col] != StymieState.EMPTY_CELL:
                return False
        if row < self.__num_rows and col + 1 < self.__num_cols:
            if self.__grid[row][col + 1] != StymieState.EMPTY_CELL:
                return False
        if row - 1 < self.__num_rows and col + 1 < self.__num_cols:
            if self.__grid[row - 1][col + 1] != StymieState.EMPTY_CELL:
                return False
        if row + 1 < self.__num_rows and col - 1 < self.__num_cols:
            if self.__grid[row + 1][col - 1] != StymieState.EMPTY_CELL:
                return False
        return True

    def validate_inplay_action(self, action: StymieInPlayAction) -> bool:
        return False

    def validate_action(self, action: StymieAction) -> bool:
        if self._stage == "placement":
            return self.validate_place_action(action)
        else:
            return self.validate_inplay_action(action)

    def update(self, action: StymieAction):
        if self._stage == "placement":
            col = action.get_col()
            row = action.get_row()
            self.__grid[row][col] = self.__acting_player
            print("AQUI",self.__check_can_place())
            if not self.__check_can_place():
                self._stage = "inplay" # quando todas as pecas estiverem colocadas
        else:
            pass

        # determine if there is a winner
        self.__has_winner = self.__check_winner(self.__acting_player)

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1

    def __display_cell(self, row, col):
        cell_value = self.__grid[row][col]
        if cell_value == 0:
            print('\033[33mX\033[0m', end="")
        elif cell_value == 1:
            print('\033[37;1mO\033[0m', end="")  # prata
        elif cell_value == 2:
            print('\033[33;1mA\033[0m', end="")  # amarelo
        elif cell_value == 3:
            print('\033[37;1mA\033[0m', end="")  # prata
        else:
            print({
                      StymieState.EMPTY_CELL: ' '
                  }[cell_value], end="")

    def __display_numbers(self):

        for col in range(0, self.__num_cols):
            if col < 10:
                print('', end="")
            if col == 0:
                print(" ", col, end="")
            else:
                print("", col, end="")
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
            print(row, '|', end="")
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
        cloned_state = StymieState(self.__num_rows)
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                cloned_state.__grid[row][col] = self.__grid[row][col]
        return cloned_state

    def get_result(self, pos) -> Optional[StymieResult]:
        if self.__has_winner:
            return StymieResult.LOOSE if pos == self.__acting_player else StymieResult.WIN
        if self.__is_full():
            return StymieResult.DRAW
        return None

    def get_num_rows(self):
        return self.__num_rows

    def get_num_cols(self):
        return self.__num_cols

    def before_results(self):
        pass

    def get_possible_actions(self):
        actions = []
        for i in range(0, self.__num_rows):
            for j in range(0, self.__num_cols):
                action = StymieAction(i, j)
                if self.validate_action(action):
                    actions.append(action)
        return actions

    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state
