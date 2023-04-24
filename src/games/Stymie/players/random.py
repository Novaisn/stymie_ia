import random

from random import randint
from games.state import State

from games.Stymie.action import StymieAction
from games.Stymie.player import StymiePlayer
from games.Stymie.state import StymieState
from games.Stymie.action import StymiePlacementAction
from games.Stymie.action import StymieAddAction
from games.Stymie.action import StymieMoveAction


class RandomStymiePlayer(StymiePlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: StymieState):
        stage = state._stage
        canpalce = state._canpalce
        actionsplacemnt = state.get_possible_actions()
        actionsadd= state.get_possible_add()
        actionsmove = state.get_possible_move()

        if stage == "placement":
            return random.choice(actionsplacemnt)

        else:
            if canpalce:
                op = randint(1, 2)
                if op == 1:
                    return random.choice(actionsadd)
                elif op == 2:
                    return random.choice(actionsmove)
            else:
                return random.choice(actionsmove)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
