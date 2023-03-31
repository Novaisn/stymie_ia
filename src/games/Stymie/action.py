from abc import ABC


class StymieAction(ABC):
    def __init__(self):
        self

class StymieInPlayAction(StymieAction, ABC):
    def __init__(self):
        self

class StymieMoveAction(StymieInPlayAction):
    __colIni: int
    __rowIni: int
    __colFim: int
    __rowFim: int
    def __init__(self, colIni: int, rowIni: int,colFim:int, rowFim:int):
        self.__colIni = colIni
        self.__rowIni = rowIni
        self.__colFim = colFim
        self.__rowFim = rowFim
    def get_colIni(self):
        return self.__colIni
    def get_rowIni(self):
        return self.__rowIni
    def get_colFim(self):
        return self.__colFim
    def get_rowFim(self):
        return self.__rowFim
class StymieAddAction(StymieInPlayAction):
    __col: int
    __row: int

    def __init__(self, col: int, row: int):
        self.__col = col
        self.__row = row

    def get_col(self):
        return self.__col

    def get_row(self):
        return self.__row


class StymiePlacementAction(StymieAction):
    """
    a tictactoe action is simple - it only takes the value of the column to play
    """
    __col: int
    __row: int

    def __init__(self, col: int, row: int):
        self.__col = col
        self.__row = row

    def get_col(self):
        return self.__col

    def get_row(self):
        return self.__row
