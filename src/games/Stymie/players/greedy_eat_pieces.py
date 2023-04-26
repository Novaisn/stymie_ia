import random
from typing import Tuple

from games.state import State
from games.Stymie.player import StymiePlayer
from games.Stymie.state import StymieState
from games.Stymie.action import StymieAddAction
from games.Stymie.action import StymieMoveAction


class GreedyEatStymiePlayer(StymiePlayer):

    def __init__(self, name):
        super().__init__(name)

    ''' '''

    def get_eat_move(self, state: StymieState, moving_piece: Tuple[int, int], enemy_piece: Tuple[int, int]) -> Tuple[int, int]:
        possible_moves = state.get_possible_move()
        min_distance = float('inf')
        distances = []
        check_eat = False
        check_friendly_fire = False

        for move in possible_moves:
            if (move.get_rowIni(), move.get_colIni()) == moving_piece:
                check_eat = abs(move.get_rowFim() - move.get_rowIni()) > 1 or \
                           abs(move.get_colFim() - move.get_colIni()) > 1
                for i in (-1, 2):
                    if (move.get_rowIni() + i, move.get_colIni()) == state.get_acting_player() or \
                        (move.get_rowIni(), move.get_colIni() + i) == state.get_acting_player():
                        check_friendly_fire = True

                if check_eat and not check_friendly_fire:
                    return move.get_rowFim(), move.get_colFim()
                elif not check_eat:
                    distance = min([abs(move.get_rowFim() - enemy_piece[0]) + abs(move.get_colFim() - enemy_piece[1])])

                    if distance < min_distance:
                        min_distance = distance
                        distances.append((move.get_rowFim(), move.get_colFim()))

                    if len(distances) > 1:
                        best_move = random.choice(distances)
                    elif len(distances) == 1:
                        best_move = distances[0]
                    else:
                        raise Exception("There is no valid action")

        return best_move

    ''' Escolhe qual a peça que está mais perto da area objetivo
    Retorna um Tuple, com a linha e coluna selecionadas'''
    def get_moving_piece(self, state: StymieState) -> Tuple[int, int]:
        grid = state.get_grid()
        pieces = []

        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                if grid[row][col] == state.get_acting_player():
                    pieces.append((row, col))

        return random.choice(pieces)

    def get_enemy_closest_to_moving(self, state: StymieState, moving_piece) -> Tuple[int, int]:

        grid = state.get_grid()
        enemy_distances = []

        # Find all player's pieces and their distances to the enemy pieces
        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                if grid[row][col] != state.get_acting_player() and grid[row][col] != state.EMPTY_CELL:
                    enemy_distance = [abs(row - moving_piece[0]) + abs(col - moving_piece[1])]
                    enemy_distances.append((enemy_distance, (row, col)))

        # Choose the closest piece to an enemy piece
        if len(enemy_distances) == 0:
            raise Exception("There are no pieces to choose from.")
        sorted_enemy_distances = sorted(enemy_distances, key=lambda x: x[0])

        return sorted_enemy_distances[0][1][0], sorted_enemy_distances[0][1][0]


    '''Escolhe qual é a melhor posição para adicionar uma peça, utilizando uma forma greedy
    Retorna um tuplo com a coluna e linha selecionada'''
    def get_greedy_add(self, state: StymieState) -> Tuple[int, int]:
        grid = state.get_grid()
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

        return selected_col, selected_row

    def get_action(self, state: StymieState):
        stage = state._stage
        canplace = state._canpalce

        if stage == "placement":
            add_move = self.get_greedy_add(state)
            return StymieAddAction(add_move[0], add_move[1])

        else:
            if canplace:
                add_move = self.get_greedy_add(state)
                return StymieAddAction(add_move[0], add_move[1])
            else:
                moving_piece = self.get_moving_piece(state)
                enemy_piece = self.get_enemy_closest_to_moving(state, moving_piece)
                best_move = self.get_eat_move(state, moving_piece, enemy_piece)

                return StymieMoveAction(moving_piece[1], moving_piece[0], best_move[1], best_move[0])

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
