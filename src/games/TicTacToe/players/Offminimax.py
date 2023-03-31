from games.TicTacToe.action import TicTacToeAction
from games.TicTacToe.player import TicTacToePlayer
from games.TicTacToe.state import TicTacToeState
from games.state import State


class OffMinimaxTicTacToePlayer(TicTacToePlayer):
    def __init__(self, name, depth=3):
        super().__init__(name)
        self.depth = depth

    def get_action(self, state: TicTacToeState):
        grid = state.get_grid()
        max_score = float('-inf')
        best_action = None

        for col in range(state.get_num_cols()):
            for row in range(state.get_num_rows()):
                action = TicTacToeAction(col, row)
                if state.validate_action(action):
                    new_state = state.apply_action(action)
                    score = self.minimax(new_state, False, self.depth)
                    if score > max_score:
                        max_score = score
                        best_action = action

        if best_action is None:
            raise Exception("There is no valid action")

        return best_action

    def minimax(self, state, is_maximizing, depth):
        result = state.get_result()
        if result is not None:
            if result == self.get_current_pos():
                return 1
            elif result == 0:
                return 0
            else:
                return -1

        if depth == 0:
            return 0

        if is_maximizing:
            max_score = float('-inf')
            for col in range(state.get_num_cols()):
                for row in range(state.get_num_rows()):
                    action = TicTacToeAction(col, row)
                    if state.validate_action(action):
                        new_state = state.apply_action(action)
                        score = self.minimax(new_state, False, depth-1)
                        max_score = max(max_score, score)
            return max_score
        else:
            min_score = float('inf')
            for col in range(state.get_num_cols()):
                for row in range(state.get_num_rows()):
                    action = TicTacToeAction(col, row)
                    if state.validate_action(action):
                        new_state = state.apply_action(action)
                        score = self.minimax(new_state, True, depth-1)
                        min_score = min(min_score, score)
            return min_score

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
