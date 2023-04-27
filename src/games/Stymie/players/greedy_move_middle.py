import random
from typing import Tuple

from games.state import State
from games.Stymie.player import StymiePlayer
from games.Stymie.state import StymieState
from games.Stymie.action import StymieAddAction
from games.Stymie.action import StymieMoveAction


class GreedyMoveStymiePlayer(StymiePlayer):

    def __init__(self, name):
        super().__init__(name)

    ''' Escolhe o movimento que faz com que a peça, passado como parametro, fica mais perto da area objetivo
    Retorna um Tuple, com a linha e coluna selecionadas'''

    def get_closest_move(self, state: StymieState, piece: Tuple[int, int]) -> Tuple[int, int]:
        possible_moves = state.get_possible_move()
        center = [(i, j) for i in range(2, 5) for j in range(2, 5)]
        min_distance = float('inf')
        best_move = None

        for move in possible_moves:
            if (move.get_rowIni(), move.get_colIni()) == piece:
                distance = min([abs(move.get_rowFim() - x) + abs(move.get_colFim() - y) for x, y in center])
                
                if distance < min_distance:
                    min_distance = distance
                    best_move = (move.get_rowFim(), move.get_colFim())
                    
        if best_move is None:
            raise Exception("There is no valid action")
        return best_move

    ''' Escolhe qual a peça que está mais perto da area objetivo
    Retorna um Tuple, com a linha e coluna selecionadas'''
    def get_closest_piece(self, state: StymieState) -> Tuple[int, int]:
        center = [(i, j) for i in range(2, 5) for j in range(2, 5)]
        grid = state.get_grid()
        possible_moves = state.get_possible_move()
        possible_place = state.get_possible_add()
        # Find the closest piece to the center
        min_distance = float('inf')
        closest_piece = None
        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                if (row, col) not in center:
                    if grid[row][col] == state.get_acting_player():
                        distance = min([abs(row - x) + abs(col - y) for x, y in center])
                        if distance < min_distance:
                            min_distance = distance
                            closest_piece = (row, col)

        if closest_piece is None:
            if possible_moves is not None:
                aux = random.choice(possible_moves)
                closest_piece = (aux.get_rowIni(),aux.get_colIni())
        if closest_piece is None:
            if possible_place is not None:
                aux = random.choice(possible_place)
                closest_piece = (aux.get_row(),aux.get_col())
        return closest_piece

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
                piece = self.get_closest_piece(state)
                best_move = self.get_closest_move(state, piece)
                return StymieMoveAction(piece[1], piece[0], best_move[1], best_move[0])

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
