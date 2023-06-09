from typing import Optional
from games.state import State
from games.Stymie.action import StymieAction
from games.Stymie.result import StymieResult
from games.Stymie.action import StymiePlacementAction
from games.Stymie.action import StymieInPlayAction
from games.Stymie.action import StymieAddAction
from games.Stymie.action import StymieMoveAction
from games.Stymie.player import StymiePlayer
from games.game_simulator import GameSimulator

class StymieState(State):
    EMPTY_CELL = -1

    def __init__(self, grid: int):
        super().__init__()
        self._stage = "placement"
        self._canpalce = True
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

        self.__count_acting0 = 0
        self.__count_acting1 = 0
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
                    arraynotplace.append((row, col))
                    if row - 1 >= 0 and col - 1 >= 0:
                        arraynotplace.append((row - 1, col - 1))
                    if row - 1 >= 0 and col < self.__num_cols:
                        arraynotplace.append((row - 1, col))
                    if row < self.__num_rows and col - 1 >= 0:
                        arraynotplace.append((row, col - 1))
                    if row + 1 < self.__num_rows and col + 1 < self.__num_cols:
                        arraynotplace.append((row + 1, col + 1))
                    if row + 1 < self.__num_rows and col < self.__num_cols:
                        arraynotplace.append((row + 1, col))
                    if row < self.__num_rows and col + 1 < self.__num_cols:
                        arraynotplace.append((row, col + 1))
                    if row - 1 >= 0 and col + 1 < self.__num_cols:
                        arraynotplace.append((row - 1, col + 1))
                    if row + 1 < self.__num_rows and col - 1 >= 0:
                        arraynotplace.append((row + 1, col - 1))

        set1 = set(arraynotplace)
        set2 = set(arrayspaces)
        diff = set2 - set1
        itens = []
        for item in diff:
            itens.append(item)
        if len(itens) == 0:
            return False
        else:
            return True
    def __check_winner(self, player):
        if self.__count_acting1 == 7 or self.__count_acting0 == 7:
            return True
        countpieces = 0
        for row in range(1, self.__num_rows-1):
            for col in range(1, self.__num_cols-1):
                if self.__grid[row][col] == player:
                    countpieces += 1

        if countpieces == 7:
            return True

        return False

    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2
    def validate_inplay_place_action(self, action: StymieAddAction) -> bool:
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
        if row - 1 < self.__num_rows and col - 1 < self.__num_cols and row - 1 >= 0 and col -1 >= 0:
            if self.__grid[row - 1][col - 1] != StymieState.EMPTY_CELL:
                return False
        if row - 1 < self.__num_rows and col < self.__num_cols and row - 1 >= 0:
            if self.__grid[row - 1][col] != StymieState.EMPTY_CELL:
                return False
        if row < self.__num_rows and col - 1 < self.__num_cols and col -1 >= 0:
            if self.__grid[row][col - 1] != StymieState.EMPTY_CELL:
                return False
        if row + 1 < self.__num_rows and col + 1 < self.__num_cols:
            if self.__grid[row + 1][col + 1] != StymieState.EMPTY_CELL:
                return False
        if row + 1 < self.__num_rows and col < self.__num_cols:
            if self.__grid[row + 1][col] != StymieState.EMPTY_CELL:
                return False
        if row < self.__num_rows and col + 1 < self.__num_cols:
            if self.__grid[row][col + 1] != StymieState.EMPTY_CELL:
                return False
        if row - 1 < self.__num_rows and col + 1 < self.__num_cols and row -1 >= 0:
            if self.__grid[row - 1][col + 1] != StymieState.EMPTY_CELL:
                return False
        if row + 1 < self.__num_rows and col - 1 < self.__num_cols and col -1 >= 0:
            if self.__grid[row + 1][col - 1] != StymieState.EMPTY_CELL:
                return False
        return True
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
        if row - 1 >= 0 and col - 1 >= 0:
            if self.__grid[row - 1][col - 1] != StymieState.EMPTY_CELL:
                return False
        if row - 1 >= 0 and col < self.__num_cols:
            if self.__grid[row - 1][col] != StymieState.EMPTY_CELL:
                return False
        if row < self.__num_rows and col - 1 >= 0:
            if self.__grid[row][col - 1] != StymieState.EMPTY_CELL:
                return False
        if row + 1 < self.__num_rows and col + 1 < self.__num_cols:
            if self.__grid[row + 1][col + 1] != StymieState.EMPTY_CELL:
                return False
        if row + 1 < self.__num_rows and col < self.__num_cols:
            if self.__grid[row + 1][col] != StymieState.EMPTY_CELL:
                return False
        if row < self.__num_rows and col + 1 < self.__num_cols:
            if self.__grid[row][col + 1] != StymieState.EMPTY_CELL:
                return False
        if row - 1 >= 0 and col + 1 < self.__num_cols:
            if self.__grid[row - 1][col + 1] != StymieState.EMPTY_CELL:
                return False
        if row + 1 < self.__num_rows and col - 1 >= 0:
            if self.__grid[row + 1][col - 1] != StymieState.EMPTY_CELL:
                return False
        return True
    def validate_move_action(self, action: StymieMoveAction) -> bool:
        colini = action.get_colIni()
        rowini = action.get_rowIni()
        colfim = action.get_colFim()
        rowfim = action.get_rowFim()
        if self.__grid[rowfim][colfim] != StymieState.EMPTY_CELL:
            return False
        if self.__grid[rowini][colini] != self.__acting_player:
            if self.__grid[rowini][colini] != 2 and self.__acting_player == 0 or self.__grid[rowini][colini] != 3 \
                    and self.__acting_player == 1:
                return False
        for i in range(-1, 2):
            for j in range(-1, 2):
                if rowini + i >= 0 and rowini + i < len(self.__grid) and colini + j >= 0 and colini + j < len(
                        self.__grid[0]):
                    if self.__grid[rowini + i][
                        colini + j] != StymieState.EMPTY_CELL:
                        if rowini + i * 2 == rowfim and colini + j * 2 == colfim:
                            return True
        if abs(rowfim - rowini) > 1 or abs(colfim - colini) > 1:
            return False

        return True

    def validate_inplay_action(self, action: StymieInPlayAction) -> bool:
        if isinstance(action, StymieAddAction):
            return self.validate_inplay_place_action(action)
        elif isinstance(action, StymieMoveAction):
            return self.validate_move_action(action)

    def validate_action(self, action: StymieAction) -> bool:
        if self._stage == "placement":
            if isinstance(action, StymiePlacementAction):
                return self.validate_place_action(action)
            else:
                return False
        else:
            if isinstance(action, StymieInPlayAction):
                return self.validate_inplay_action(action)
            else:
                return False

    def is_diagonal_move(self,row_ini, col_ini, row_fim, col_fim):
        delta_row = abs(row_fim - row_ini)
        delta_col = abs(col_fim - col_ini)

        return delta_row == delta_col

    def is_orthogonal_move(self,row_ini, col_ini, row_fim, col_fim):
        delta_row = abs(row_fim - row_ini)
        delta_col = abs(col_fim - col_ini)

        return delta_row == 0 or delta_col == 0

    def get_path_pieces(self, rowini, colini, rowfim, colfim):

        if rowini == rowfim and colini == colfim:
            return []

        path_pieces = []
        if self.is_diagonal_move(rowini, colini, rowfim, colfim):
            delta_row = 1 if rowfim > rowini else -1
            delta_col = 1 if colfim > colini else -1
            row, col = rowini + delta_row, colini + delta_col
            while row != rowfim and col != colfim:
                if self.__grid[row][col] != StymieState.EMPTY_CELL:
                    path_pieces.append((row, col))
                row += delta_row
                col += delta_col



        elif self.is_orthogonal_move(rowini, colini, rowfim, colfim):
            if rowini == rowfim:
                delta_col = 1 if colfim > colini else -1
                col = colini + delta_col
                while col != colfim:
                    if self.__grid[rowini][col] != StymieState.EMPTY_CELL:
                        path_pieces.append((rowini, col))
                    col += delta_col
            else:
                delta_row = 1 if rowfim > rowini else -1
                row = rowini + delta_row
                while row != rowfim:
                    if self.__grid[row][colini] != StymieState.EMPTY_CELL:
                        path_pieces.append((row, colini))
                    row += delta_row

        return path_pieces

    def update(self, action: StymieAction):
        if self._stage == "placement":
            col = action.get_col()
            row = action.get_row()
            self.__grid[row][col] = self.__acting_player
            self._canpalce = self.__check_can_place()
            if not self.__check_can_place():
                self._stage = "inplay"  # quando todas as pecas estiverem colocadas
        else:
            if isinstance(action, StymieMoveAction):
                colini = action.get_colIni()
                rowini = action.get_rowIni()
                colfim = action.get_colFim()
                rowfim = action.get_rowFim()
                if self.__grid[rowini][colini] == 2:
                    self.__grid[rowfim][colfim] = 2
                elif self.__grid[rowini][colini] == 3:
                    self.__grid[rowfim][colfim] = 3
                else:
                    self.__grid[rowfim][colfim] = self.__acting_player
                self.__grid[rowini][colini] = self.EMPTY_CELL
                pieces = self.get_path_pieces(rowini, colini, rowfim, colfim)
                for i in pieces:
                    if self.__grid[i[0]][i[1]] == 2:
                        self.__grid[i[0]][i[1]] = 3
                        continue
                    elif self.__grid[i[0]][i[1]] == 3:
                        self.__grid[i[0]][i[1]] = 2
                        continue
                    if self.__grid[i[0]][i[1]] != self.__acting_player:
                        self.__grid[i[0]][i[1]] = self.EMPTY_CELL
                        if self.__acting_player == 0:
                            self.__count_acting0 += 1
                        elif self.__acting_player == 1:
                            self.__count_acting1 += 1
            elif isinstance(action, StymieAddAction):
                col = action.get_col()
                row = action.get_row()
                self.__grid[row][col] = self.__acting_player
            self._canpalce = self.__check_can_place()
        # determine if there is a winner
        self.__has_winner = self.__check_winner(self.__acting_player)
        # switch to next player

        self.__acting_player = 1 if self.__acting_player == 0 else 0
        #self.display()

        #print(self._stage)
        self.__turns_count += 1

    def __display_cell(self, row, col):
        cell_value = self.__grid[row][col]
        if cell_value == 0:
            print('\033[33mX\033[0m', end="")
        elif cell_value == 1:
            print('\033[37;1mO\033[0m', end="")
        elif cell_value == 2:
            print('\033[33;1mA\033[0m', end="")
        elif cell_value == 3:
            print('\033[37;1mA\033[0m', end="")
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
        return self.__has_winner

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = StymieState(self.__num_rows)
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
        cloned_state._stage = self._stage
        cloned_state._canpalce = self._canpalce
        cloned_state.__count_acting0 = self.__count_acting0
        cloned_state.__count_acting1 = self.__count_acting1
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
        return list(filter(
            lambda action: self.validate_place_action(action),
            [
                StymiePlacementAction(col, row)
                for row in range(self.get_num_rows())
                for col in range(self.get_num_cols())
            ]
        ))
    def get_possible_add(self):
        return list(filter(
            lambda action: self.validate_inplay_place_action(action),
            [
                StymieAddAction(col, row)
                for row in range(self.get_num_rows())
                for col in range(self.get_num_cols())
            ]
        ))

    def get_possible_move(self):
        return list(filter(
            lambda action: self.validate_move_action(action),
            [
                StymieMoveAction(colini, rowini, colfim, rowfim)
                for rowini in range(self.get_num_rows())
                for colini in range(self.get_num_cols())
                for rowfim in range(self.get_num_rows())
                for colfim in range(self.get_num_cols())
            ]
        ))

    def get_player_pieces(self):
        pieces = []

        for col in range(0, self.get_num_cols()):
            for row in range(0, self.get_num_rows()):
                if self.__grid[col][row] == self.__acting_player:
                    pieces.append((col, row))

        return pieces
    def get_possible_actions_minimax(self):
        if self._stage == 'placement':
            return self.get_possible_actions()
        else:
            return self.get_possible_move() +self.get_possible_add()
    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state
