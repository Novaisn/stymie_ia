from typing import Tuple

from random import choice
from games.state import State

from games.Stymie.action import StymieAction
from games.Stymie.player import StymiePlayer
from games.Stymie.state import StymieState
from games.Stymie.action import StymiePlacementAction
from games.Stymie.action import StymieAddAction
from games.Stymie.action import StymieMoveAction


class GreedyStymiePlayer(StymiePlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_closest_move(self, state: StymieState, position: Tuple[int, int]) -> Tuple[int, int]:
        possible_moves = state.get_possible_move()
        center = [(i, j) for i in range(2, 5) for j in range(2, 5)]
        min_distance = float('inf')
        best_move = None
        for move in possible_moves:
            if (move.get_rowIni(), move.get_colIni()) == position:
                distance = min([abs(move.get_rowFim() - x) + abs(move.get_colFim() - y) for x, y in center])
                if distance < min_distance:
                    min_distance = distance
                    best_move = (move.get_colFim(), move.get_rowFim())
        if best_move is None:
            raise Exception("There is no valid action")
        return best_move

    def get_closest_piece(self, state: StymieState) -> Tuple[int, int]:
        center = [(i, j) for i in range(2, 5) for j in range(2, 5)]
        grid = state.get_grid()

        # Find the closest piece to the center
        min_distance = float('inf')
        closest_piece = None
        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                if (row, col) not in center:
                    piece = grid[row][col]
                    if piece == state.get_acting_player():
                        distance = min([abs(row - x) + abs(col - y) for x, y in center])
                        if distance < min_distance:
                            min_distance = distance
                            closest_piece = (row, col)

        if closest_piece is None:
            raise Exception("There is no valid action")
        return closest_piece

    def get_action(self, state: StymieState):
        grid = state.get_grid()
        stage = state._stage
        canpalce = state._canpalce

        if stage == "placement":
            max_count = -1
            selected_col = None
            selected_row = None
            for col in range(state.get_num_cols()):
                for row in range(state.get_num_rows() - 1, -1, -1):
                    if state.validate_action(StymieAddAction(col, row)):
                        count = 0
                        for i in range(state.get_num_rows()):
                            if grid[i][col] == self.get_current_pos():
                                count += 1
                        if count > max_count:
                            max_count = count
                            selected_col = col
                            selected_row = row
                        elif count == max_count and row < selected_row:
                            selected_col = col
                            selected_row = row

            if selected_col is None:
                raise Exception("There is no valid action")
            if selected_row is None:
                raise Exception("There is no valid action")

            print("placeG")
            return StymieAddAction(selected_col, selected_row)

        else:
            if canpalce:
                max_count = -1
                selected_col = None
                selected_row = None
                for col in range(state.get_num_cols()):
                    for row in range(state.get_num_rows() - 1, -1, -1):
                        if state.validate_action(StymieAddAction(col, row)):
                            count = 0
                            for i in range(state.get_num_rows()):
                                if grid[i][col] == self.get_current_pos():
                                    count += 1
                            if count > max_count:
                                max_count = count
                                selected_col = col
                                selected_row = row
                            elif count == max_count and row < selected_row:
                                selected_col = col
                                selected_row = row

                if selected_col is None:
                    raise Exception("There is no valid action")
                if selected_row is None:
                    raise Exception("There is no valid action")

                print("placeG")
                return StymieAddAction(selected_col, selected_row)
            else:
                print("PROBLEM")
                position = self.get_closest_piece(state)
                print(position)
                best_move = self.get_closest_move(state, position)
                print(best_move)
                print("PROBLEM2")

                return StymieMoveAction(position[1], position[0], best_move[1], best_move[0])

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
