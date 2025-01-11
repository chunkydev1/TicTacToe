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

### Player move is good. It's general enough to be used for this 
### and other things, and if you wanted to get really specific, you 
### could do something like (see tttMove). That could be something that
### in any ttt tooling you use tttmove, and if you need to pass into 
### something expecting a move generic you get the raw. 
###
### Note that the difference here is that it's not inheritence, it's 
### composition. This is a big sofware difference as you'll USUALLY 
### compose classes not inherit them. 
@dataclass
class PlayerMove:
    location: list[str]
    playername: str
    playertype: str

class TttMove: 
    def __init__(self, playerMove): 
        self.__pm = playerMove
    @property 
    def x(self): 
        return self.__pm[0]
    @property 
    def y(self): 
        return self.__pm[1]
    @property 
    def playerName(self): 
        return self.__pm.playername
    @property 
    def playerType(self):
        return self.__pm.playertype

    def raw(self): return self.__pm

###
### NOTE: This is the only HUGE problem I have with the implementation. 
###       My problem with it sits in the "this _works_ but undermines object
###       oriented coding in a way that's hard to overlook"
###
### I haven't read all the code yet, but I consider this bad on first read. 
### your board class needs to HIDE the board implementation from everybody. 
### This isn't hiding because there's a "get_board" method. 
###
### We hide so that we can change it later. 
@dataclass
class BoardBlueprints:
    grid: list[list[str]]


class Board(abc.ABC):

    ### We're HIDING the board content. Users of the Board class
    ### should never know that the board is a list of list of string 
    def __init__(self, blueprints: BoardBlueprints):
        self.__board = blueprints

    @abc.abstractmethod
    def set_move_on_board(self, move: PlayerMove) -> None:
        pass


    ### Bad bad bad
    ### Hiding doesn't work if you can get the underlying implementation. 
    ### In pure object oriented this should not be here. 
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
    ###
    ### You're very close here. In short, yes but no. 
    ### 
    ### spot_is_playable is a "conceptual" method. The concept of playablity depends on the board and the rules. 
    ###     So yes, the rules need some say - therefore you're right to have this method here. 
    ### HOWEVER, your implementation is where you go astray. You're operating on the guts of the board. 
    ###     you're not respecting the Board classes autonomy. This method should be made up of 
    ###     method calls that allow the board to do the thinking. Things like: 
    ###
    ###     - Board::get_player_at(playerinputs) -> Returns None or player info
    ###     or
    ###     - Board::is_move_empty(playerinputs) -> True/False if empty
    ###     or 
    ###     - Board::check_set_move_on_board() -> Checks if it can set the move on the board. 
    ### 
    ### Each of them have different ups and downs, but all of them protect the core implementation. 
    ###     If you get the BoardBlueprints directly, you have to update a lot of code if you ever change how BoardBlueprints works.
    ###
    @abc.abstractmethod
    def spot_is_playable(self, board: BoardBlueprints, playerinputs: PlayerMove) -> bool:
        pass

    def get_valid_inputs(self) -> list[str]:
        return self.__vinputs


### What was the point of introducing this class? What are you trying to do with it? 
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

    ### Avoid using variable names that are build in commands
    ### type is a command AND a variabile in this method 
    ### how confusing :) 
    def __init__(self, name: str, type: str) -> None:
        self.__name = name
        self.__playertype = type
        ### Consider using setters in constructor: 
        ### self._set_name(name)
        ### self._set_player_type(type)

    def get_name(self) -> str:
        return self.__name

    ### Make this private so it's not accidentally called by someone who can't use it
    ### def _set_name(...)
    def set_name(self, name: str) -> None:
        ### What's the difference between self.__name and self.name? 
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
        ### Alright, I think it's time that we address this valid inputs shenanigans... 
        ### You know that the values are always going to be ints, so why store them as strings? 
        ### 
        ### Also, how do you know that your board and the win length/valid inputs will always match? 
        ### It's a minor nit here, but there's no programmical guarantee
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
    ###
    ### This class is the ONLY place you're allowed to operate on board.grid
    ### 
    ### Just because you're passing the grid in, doesn't mean you can pass it around. 
    ### Passing the grid in is _ok/good_ for testing. For runtime though, 
    ### it's bad. Whenever someone operates on the board, they need to go through 
    ### this class. Not "get this classes content and use the contents", but go 
    ### THROUGH the class. set_move_on_board is a perfect example. Prior implemtnations 
    ### you had would get the board and then see if it could be put on it. The same is 
    ### true for get_spot_playable. 
    ###
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

        ### Copy and pasted from above. 
        # spot_is_playable could be in gameboard because its sole responsibility is to look at the board, but I think its better here because the rules of a valid input are 2 things:
        # 1- must be within bounds (def valid_inputs)
        # 2- must be a location not already played (spot_is_playable).
        ###
        ### You're very close here. In short, yes but no. 
        ### 
        ### spot_is_playable is a "conceptual" method. The concept of playablity depends on the board and the rules. 
        ###     So yes, the rules need some say - therefore you're right to have this method here. 
        ### HOWEVER, your implementation is where you go astray. You're operating on the guts of the board. 
        ###     you're not respecting the Board classes autonomy. This method should be made up of 
        ###     method calls that allow the board to do the thinking. Things like: 
        ###
        ###     - Board::get_player_at(playerinputs) -> Returns None or player info
        ###     or
        ###     - Board::is_move_empty(playerinputs) -> True/False if empty
        ###     or 
        ###     - Board::check_set_move_on_board() -> Checks if it can set the move on the board. 
        ### 
        ### Each of them have different ups and downs, but all of them protect the core implementation. 
        ###     If you get the BoardBlueprints directly, you have to update a lot of code if you ever change how BoardBlueprints works.
        ###

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
        ###
        ### bad bad bad 
        ### You're operating on the grid directly 
        ### bad bad bad 
        ### All of this logic should be interwoven with the Board class 
        ### not the BoardBlueprint class. 
        ###
        rows = len(board.grid)
        cols = len(board.grid[0])

        #             right,   down, right+down, left+down
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(rows):
            for col in range(cols):
                for rdir, cdir in directions:
                    valuetolookup = board.grid[row][col]
                    ### Bad bad bad 
                    ### no operating on the BoardBlueprint directly 
                    ### bad bad bad
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
                    ### Bad bad bad 
                    ### no operating on the BoardBlueprint directly 
                    ### bad bad bad
                    searchinfo.board.grid[r][c] == searchinfo.lookupvalue
            ):
                return False

        return True

    def game_is_tie(self, board: BoardBlueprints) -> bool:
        ### Bad bad bad 
        ### no operating on the BoardBlueprint directly 
        ### bad bad bad
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
