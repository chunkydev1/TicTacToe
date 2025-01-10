import re
import abc
import random
import names
from dataclasses import dataclass
from typing import Optional

class Game(abc.ABC):

    @abc.abstractmethod
    def get_input_rules(self):
        pass

    @abc.abstractmethod
    def get_win_criteria(self):
        pass

    @abc.abstractmethod
    def get_gameboard(self):
        pass

@dataclass
class BoardBlueprints:
    grid: list[list[str]]


@dataclass
class PlayerMove:
    location: list[str]
    playername: str
    playertype: str


class Board(abc.ABC):

    def __init__(self, blueprints: BoardBlueprints):
        self.__board = blueprints

    @abc.abstractmethod
    def set_move_on_board(self, move: PlayerMove) -> None:
        pass

    def get_board(self) -> BoardBlueprints:
        return self.__board

    @abc.abstractmethod
    def display_board(self) -> None:
        pass


class InputRules(abc.ABC):

    def __init__(self, vinputs: list[str]) -> None:
        self.__vinputs = vinputs

    @abc.abstractmethod
    def valid_inputs(self, pinputs: PlayerMove) -> bool:
        pass

    # spot_is_playable could be in gameboard because its sole responsibility is to look at the board, but I think its better here because the rules of a valid input are 2 things:
    # 1- must be within bounds (def valid_inputs)
    # 2- must be a location not already played (spot_is_playable).
    @abc.abstractmethod
    def spot_is_playable(self, board: BoardBlueprints, playerinputs: PlayerMove) -> bool:
        pass

    def get_valid_inputs(self) -> list[str]:
        return self.__vinputs

@dataclass
class SearchingMaterials:
    board: BoardBlueprints
    row: int
    col: int
    rdir: int
    cdir: int
    length: int
    lookupvalue: str

class WinCriteria(abc.ABC):

    def __init__(self, winlength: int) -> None:
        self.__winlength = winlength

    def get_win_length(self) -> int:
        return self.__winlength

    @abc.abstractmethod
    def game_is_won(self, board: BoardBlueprints) -> bool:
        pass

    @abc.abstractmethod
    def check_pattern(self, board: BoardBlueprints) -> tuple[bool, None or str]:
        pass

    @abc.abstractmethod
    def search_board(self,searchinfo: SearchingMaterials) -> bool:
        pass

    @abc.abstractmethod
    def game_is_tie(self, board: BoardBlueprints) -> bool:
        pass


class players(abc.ABC):

    def __init__(self, name: str, type: str) -> None:
        self.__name = name
        self.__playertype = type

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_player_type(self):
        return self.__playertype

    @abc.abstractmethod
    def get_move(self) -> PlayerMove:
        pass

    def get_random_name(self) -> str:
        randname = names.get_first_name()
        return randname


class tictactoe(Game):

    def __init__(self) -> None:
        self.__board = tttboard(
            blueprints=BoardBlueprints(
                grid=[
                    ["", "", ""],
                    ["", "", ""],
                    ["", "", ""]
                ]
            )
        )
        self.__validinputs = ["0", "1", "2"]
        self.__winlength = 3

        self.__rules = tttinputrules(self.__validinputs)
        self.__win = tttwin(self.__winlength)

    def get_input_rules(self) -> InputRules:
        return self.__rules

    def get_win_criteria(self) -> WinCriteria:
        return self.__win

    def get_gameboard(self) -> Board:
        return self.__board


class tttboard(Board):

    def __int__(self, blueprints: BoardBlueprints):
        super().__init__(blueprints)

    def set_move_on_board(self, move: PlayerMove) -> None:
        board = self.get_board()
        loc = move.location
        name = move.playername

        x = int(loc[0])
        y = int(loc[1])

        board.grid[x][y] = name
        print(name + " has made a move")

    def display_board(self) -> None:
        board = self.get_board()
        for row in board.grid:
            print(row)


class tttinputrules(InputRules):

    def __init__(self, vinputs: list[str]) -> None:
        super().__init__(vinputs)

    def valid_inputs(self, playerinputs: PlayerMove) -> bool:
        if len(playerinputs.location) != 2:
            return False

        for pi in playerinputs.location:
            if pi not in self.get_valid_inputs():
                # print("not valid")
                return False
        # print("valid")
        return True

    def spot_is_playable(self, board: BoardBlueprints, playerinputs: PlayerMove) -> bool:
        x = int(playerinputs.location[0])
        y = int(playerinputs.location[1])

        if board.grid[x][y] != "":
            # print("not playable")
            return False
        # print("playable")
        return True


@dataclass
class PatternResult:
    found: bool
    name: Optional[str]


class tttwin(WinCriteria):

    def __init__(self, winlength: int) -> None:
        super().__init__( winlength)

    def game_is_won(self, board: BoardBlueprints) -> bool:

        winner = self.check_pattern(board)
        if winner.found:
            print("Winner: " + winner.name)
            return True

    def check_pattern(self, board: BoardBlueprints) -> PatternResult:

        # print(f"board recieved: {type(board)}")

        rows = len(board.grid)
        cols = len(board.grid[0])

        #             right,   down, right+down, left+down
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(rows):
            for col in range(cols):
                for rdir, cdir in directions:
                    valuetolookup = board.grid[row][col]
                    if self.search_board(SearchingMaterials(board=board,
                                                            row=row,
                                                            col=col,
                                                            rdir=rdir,
                                                            cdir=cdir,
                                                            length=self.get_win_length(),
                                                            lookupvalue=valuetolookup
                                                            )
                                         ):
                        return PatternResult(found=True, name=board.grid[row][col])
        return PatternResult(found=False, name=None)

    def search_board(self, searchinfo: SearchingMaterials) -> bool:

        if searchinfo.lookupvalue == "":
            return False

        for i in range(searchinfo.length):
            r = searchinfo.row + i * searchinfo.rdir
            c = searchinfo.col + i * searchinfo.cdir
            # Check bounds and value
            if not (0 <= r < len(searchinfo.board.grid) and
                    0 <= c < len(searchinfo.board.grid[0]) and
                    searchinfo.board.grid[r][c] == searchinfo.lookupvalue
            ):
                return False

        return True

    def game_is_tie(self, board: BoardBlueprints) -> bool:
        for row in board.grid:
            if "" in row:
                return False

        print("game is a tie")
        return True


class manualplayer(players):

    def __init__(self) -> None:
        super().__init__(name=self.get_random_name(), type="Real")

    def get_move(self) -> PlayerMove:
        pinput = input(self.get_name() + ", please play your move")

        return PlayerMove(location=re.findall(r'[0-9]+', pinput), playername=self.get_name(),
                          playertype=self.get_player_type())


class playerAI(players):

    def __init__(self, name: str = "NPC", ptype: str = "Fake") -> None:
        super().__init__(name=name, type=ptype)

    def get_move(self) -> PlayerMove:
        x = str(random.randint(0, 2))
        y = str(random.randint(0, 2))
        return PlayerMove(location=[x, y], playername=self.get_name(), playertype=self.get_player_type())


def run_game(g: Game, playersingame: list[players]) -> None:
    for p in playersingame:
        b = g.get_gameboard()
        move = p.get_move()

        gameinputs = g.get_input_rules()

        while not gameinputs.valid_inputs(move) or not gameinputs.spot_is_playable(b.get_board(), move):
            if move == "Real":
                print("Input not valid, try again")
            move = p.get_move()

        b.set_move_on_board(move)
        b.display_board()

        winrules = g.get_win_criteria()

        if winrules.game_is_won(b.get_board()) or winrules.game_is_tie(b.get_board()):
            return
    run_game(g, playersingame)


if __name__ == '__main__':
    AI = playerAI()
    ttt = tictactoe()
    playersingame = [manualplayer(), AI]
    #ttt.display_board()

    run_game(ttt, playersingame)
