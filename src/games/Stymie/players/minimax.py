import math

from games.state import State
from games.Stymie.player import StymiePlayer
from games.Stymie.state import StymieState
from games.Stymie.result import StymieResult

from games.Stymie.action import StymiePlacementAction

from games.Stymie.action import StymieAddAction

from games.Stymie.action import StymieInPlayAction


class MinimaxStymiePlayer(StymiePlayer):

    def __init__(self, name):
        super().__init__(name)

    '''
    This heuristic will simply count the maximum number of consecutive pieces that the player has
    It's not a great heuristic as it doesn't take into consideration a defensive approach
    '''

    def __heuristic(self, state: StymieState):
        grid = state.get_grid()
        stage = state._stage
        longest = 0
        total_pieces = 0
        max_count = -1

        if stage == 'placement':
            longest = 1
            for col in range(state.get_num_cols()):
                for row in range(state.get_num_rows()):
                    count = 0
                    for i in range(state.get_num_rows()):
                        if grid[i][col] == self.get_current_pos():
                            count += 1
                            longest += 1
                    if count > max_count:
                        max_count = count
                        longest += 2
            longest = 2
        else:
            longest =2

        if state.get_acting_player() == 1:
            longest = state._StymieState__count_acting0 - state._StymieState__count_acting1
        else:
            longest = state._StymieState__count_acting1 - state._StymieState__count_acting0

        return longest

    """Implementation of minimax search (recursive, with alpha/beta pruning) :param state: the state for which the 
    search should be made :param depth: maximum depth of the search :param alpha: to optimize the search :param beta: 
    to optimize the search :param is_initial_node: if true, the function will return the action with max ev, 
    otherwise it return the max ev (ev = expected value) """

    def minimax(self, state: StymieState, depth: int, alpha: int = -math.inf, beta: int = math.inf,
                is_initial_node: bool = True):
        # first we check if we are in a terminal node (victory, draw or loose)
        if state.is_finished():
            return {
                StymieResult.WIN: 40,
                StymieResult.LOOSE: -40,
                StymieResult.DRAW: 0
            }[state.get_result(self.get_current_pos())]

        # if we reached the maximum depth, we will return the value of the heuristic
        if depth == 0:
            return self.__heuristic(state)

        # if we are the acting player
        if self.get_current_pos() == state.get_acting_player():
            # very small integer
            value = -math.inf
            selected_action = None

            if state._stage == 'placement':
                for action in state.get_possible_actions():
                    pre_value = value
                    value = max(value, self.minimax(state.sim_play(action), depth - 1, alpha, beta, False))
                    if value > pre_value:
                        selected_action = action
                    if value > beta:
                        break
                    alpha = max(alpha, value)
            else:
                for action in state.get_possible_move():
                    pre_value = value
                    value = max(value, self.minimax(state.sim_play(action), depth - 1, alpha, beta, False))
                    if value > pre_value:
                        #if isinstance(action, StymieInPlayAction):
                        selected_action = action
                    if value > beta:
                        break
                    alpha = max(alpha, value)
                for action in state.get_possible_add():
                    pre_value = value
                    value = max(value, self.minimax(state.sim_play(action), depth - 1, alpha, beta, False))
                    if value > pre_value:
                        #if isinstance(action, StymieInPlayAction):
                        selected_action = action
                    if value > beta:
                        break
                    alpha = max(alpha, value)
            return selected_action if is_initial_node else value

        # if it is the opponent's turn
        else:
            value = math.inf
            for action in state.get_possible_actions():
                value = min(value, self.minimax(state.sim_play(action), depth - 1, alpha, beta, False))
                if value < alpha:
                    break
                beta = min(beta, value)
            return value

    def get_action(self, state: StymieState):
        return self.minimax(state, 1)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass