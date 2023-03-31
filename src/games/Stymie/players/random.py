from random import randint
from games.state import State

from games.Stymie.action import StymieAction
from games.Stymie.player import StymiePlayer
from games.Stymie.state import StymieState


class RandomStymiePlayer(StymiePlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: StymieState):
        return StymieAction(randint(0, state.get_num_cols()), randint(0, state.get_num_rows()))

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
