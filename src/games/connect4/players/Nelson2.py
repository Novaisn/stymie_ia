import sys


from random import choice
from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.result import Connect4Result
from games.connect4.state import Connect4State
from games.state import State



class Nelson2(Connect4Player):
    def __init__(self, name):
        super().__init__(name)

    '''
    This heuristic will simply count the maximum number of consecutive pieces that the player has
    It's not a great heuristic as it doesn't take into consideration a defensive approach
    '''

    def __heuristic(self, state: Connect4State):
        grid = state.get_grid()
        longest = 0

        for col in range(0, state.get_num_cols()):
            if not state.validate_action(Connect4Action(col)):
                continue

            count = 0
            for row in range(0, state.get_num_rows()):
                if col < 4 and grid[row][col + 1] == self.get_current_pos() and grid[row][
                    col + 2] == self.get_current_pos() and grid[row][col + 3] == self.get_current_pos():
                    count += 1
                if col > 2 and grid[row][col - 1] == self.get_current_pos() and grid[row][
                    col - 2] == self.get_current_pos() and grid[row][col - 3] == self.get_current_pos():
                    count += 1
                if row < 3 and grid[row + 1][col] == self.get_current_pos() and grid[row + 2][
                    col] == self.get_current_pos() and grid[row + 3][col] == self.get_current_pos():
                    count += 1

            # it swap the column if we exceed the count. if the count of chips is the same, we swap 50% of the times
            if count > longest or (count == longest and choice([False, True])):
                longest = count

        return longest

    """Implementation of minimax search (recursive, with alpha/beta pruning) :param state: the state for which the 
    search should be made :param depth: maximum depth of the search :param alpha: to optimize the search :param beta: 
    to optimize the search :param is_initial_node: if true, the function will return the action with max ev, 
    otherwise it return the max ev (ev = expected value) """

    def minimax(self, state: Connect4State, depth: int, alpha: int = -sys.maxsize, beta: int = sys.maxsize,
                is_initial_node: bool = True):
        # first we check if we are in a terminal node (victory, draw or loose)
        if state.is_finished():
            return {
                Connect4Result.WIN: 4,
                Connect4Result.LOOSE: -4,
                Connect4Result.DRAW: 0
            }[state.get_result(self.get_current_pos())]

        # if we reached the maximum depth, we will return the value of the heuristic
        if depth == 0:
            return self.__heuristic(state)

        # if we are the acting player
        if self.get_current_pos() == state.get_acting_player():
            # very small integer
            value = sys.maxsize
            selected_pos = -1

            for pos in range(0, state.get_num_cols()):
                action = Connect4Action(pos)
                if state.validate_action(action):
                    previous_a = value
                    next_state = state.clone()
                    next_state.play(action)
                    value = max(value, self.minimax(next_state, depth - 1, alpha, beta, False))
                    alpha = max(alpha, value)

                    if value >= previous_a:
                        selected_pos = pos
                    if alpha > beta:
                        break

            if is_initial_node:
                return selected_pos
            return value
        # if it is the opponent's turn
        else:
            # very big integer
            value = -sys.maxsize
            for pos in range(0, state.get_num_cols()):
                action = Connect4Action(pos)
                if state.validate_action(action):
                    next_state = state.clone()
                    next_state.play(action)
                    value = min(value, self.minimax(next_state, depth - 1, alpha, beta, True))
                    beta = min(beta, value)

                    if beta <= alpha:
                        break
            return value

    def get_action(self, state: Connect4State):
        return Connect4Action(self.minimax(state, 3))

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass