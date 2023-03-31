from games.Stymie.player import StymiePlayer
from games.Stymie.state import StymieState
from games.Stymie.action import StymieAction

from games.Stymie.action import StymiePlacementAction


class HumanStymiePlayer(StymiePlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: StymieState):
        state.display()
        while True:
            # noinspection PyBroadException
            try:
                return StymiePlacementAction(int(input(f"Player {state.get_acting_player()}, choose a column: ")),
                                       int(input(f"Player {state.get_acting_player()}, choose a row: ")))
            except Exception:
                continue

    def event_action(self, pos: int, action, new_state: StymieState):
        # ignore
        pass

    def event_end_game(self, final_state: StymieState):
        # ignore
        pass
