from games.Stymie.player import StymiePlayer
from games.Stymie.state import StymieState
from games.Stymie.action import StymieAction

from games.Stymie.action import StymiePlacementAction
from games.Stymie.action import StymieAddAction
from games.Stymie.action import StymieMoveAction


class HumanStymiePlayer(StymiePlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: StymieState):
        state.display()
        stage = state._stage
        print("CAN PALCE",state._canpalce)

        if stage == "placement":
            while True:

                try:
                    return StymiePlacementAction(int(input(f"Player {state.get_acting_player()}, choose a column: ")),
                                           int(input(f"Player {state.get_acting_player()}, choose a row: ")))
                except Exception:
                    continue
        else:
            if state._canpalce:
                while True:
                    op = (int(input(f"Add Piece(1) or Move Piece(2): ")))
                    if op == 1 or op == 2:
                        break
                if op == 1:
                    return StymieAddAction(int(input(f"Player {state.get_acting_player()}, choose a column: ")),
                                           int(input(f"Player {state.get_acting_player()}, choose a row: ")))
                elif op == 2:
                    return StymieMoveAction(int(input(f"Player {state.get_acting_player()}, choose the starting column: ")),
                                            int(input(f"Player {state.get_acting_player()}, choose the starting row: ")),
                                            int(input(f"Player {state.get_acting_player()}, choose the final column: ")),
                                            int(input(f"Player {state.get_acting_player()}, choose the final row: ")))
            else:
                return StymieMoveAction(int(input(f"Player {state.get_acting_player()}, choose the starting column: ")),
                                        int(input(f"Player {state.get_acting_player()}, choose the starting row: ")),
                                        int(input(f"Player {state.get_acting_player()}, choose the final column: ")),
                                        int(input(f"Player {state.get_acting_player()}, choose the final row: ")))
    def event_action(self, pos: int, action, new_state: StymieState):
        # ignore
        pass

    def event_end_game(self, final_state: StymieState):
        # ignore
        pass
