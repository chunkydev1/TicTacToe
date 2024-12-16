import re
import abc
import random
import names
from dataclasses import dataclass
from typing import Optional


class Gameboard(abc.ABC):

    @abc.abstractmethod
    def set_move_on_board(self,move: list[str],name: str) -> None:
        pass

    #unused
    @abc.abstractmethod
    def get_board(self) -> list[list[str]]:
        pass

    @abc.abstractmethod
    def get_input_rules(self):
        pass

    @abc.abstractmethod
    def get_win_criteria(self):
        pass

    @abc.abstractmethod
    def display_board(self) -> None:
        pass





class InputRules(abc.ABC):

    def __init__(self,inputs: list[str]) -> None:
        self.__vinputs = inputs

    @abc.abstractmethod
    def valid_inputs(self,playerinputs: list[str]) -> bool:
        pass

    #spot_is_playable could be in gameboard because its sole responsibility is to look at the board, but I think its better here because the rules of a valid input are 2 things:
    # 1- must be within bounds (def valid_inputs)
    # 2- must be a location not already played (spot_is_playable).
    @abc.abstractmethod
    def spot_is_playable(self,board: list[list[str]], playerinputs: list[str]) -> bool:
        pass

    def get_valid_inputs(self) -> list[str]:
        return self.__vinputs






class WinCriteria(abc.ABC):

    def __init__(self, getboard: callable(Gameboard), winlength: int) -> None:
        self.__getboard = getboard
        self.__winlength = winlength

    def get_win_length(self) -> int:
        return self.__winlength

    @abc.abstractmethod
    def game_is_won(self) -> bool:
        pass

    @abc.abstractmethod
    def check_pattern(self) -> tuple[bool, None or str]:
        pass

    @abc.abstractmethod
    def search_board(self, row: int, col: int, xdir: int, ydir: int, length: int, lookupvalue: str) -> bool:
        pass

    @abc.abstractmethod
    def game_is_tie(self) -> bool:
        pass









class players(abc.ABC):

    def __init__(self,name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_name(self,name: str) -> None:
        self.name = name


    @abc.abstractmethod
    def get_move(self) -> list[str]:
        pass

    def get_random_name(self) -> str:
        randname = names.get_first_name()
        return randname















class tictactoe(Gameboard):

    def __init__(self) -> None:
        self.__board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.__validinputs = ["0","1","2"]
        self.__winlength = 3

        self.__rules = tttinputrules(self.__validinputs)
        self.__win = tttwin(self.get_board(),self.__winlength)

    def set_move_on_board(self,playermove: list[str],name: str) -> None:
        x = int(playermove[0])
        y = int(playermove[1])

        self.__board[x][y] = name

    def get_board(self) -> list[list[str]]:
        return self.__board

    def get_input_rules(self) -> InputRules:
        return self.__rules

    def get_win_criteria(self) -> WinCriteria:
        return self.__win

    def display_board(self) -> None:
        for row in self.__board:
            print(row)









class tttinputrules(InputRules):

    def __init__(self, inputs: list[str]) -> None:
        super().__init__(inputs)
        self.__validinputs = self.get_valid_inputs()

    def valid_inputs(self,playerinputs: list[str]) -> bool:
        if len(playerinputs) != 2:
            return False

        for pi in playerinputs:
            if pi not in self.__validinputs:
                #print("not valid")
                return False
        #print("valid")
        return True

    def spot_is_playable(self, board: list[list[str]], playerinputs: list[str]) -> bool:
        x = int(playerinputs[0])
        y = int(playerinputs[1])

        if board[x][y] != "":
            #print("not playable")
            return False
        #print("playable")
        return True


@dataclass
class PatternResult:
    found: bool
    winner: Optional[str]


class tttwin(WinCriteria):

    def __init__(self,getboard: callable(Gameboard), winlength: int) -> None:
        super().__init__(getboard,winlength)
        self.__winlength = self.get_win_length()
        self.__getboard = getboard



    def game_is_won(self) -> bool:

        found, winner = self.check_pattern()
        if found:
            print("Winner: " + winner)
            return True


    def check_pattern(self) -> PatternResult:

        board = self.__getboard

        rows = len(board)
        cols = len(board[0])

        #             right,   down, right+down, left+down
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(rows):
            for col in range(cols):
                for xdir, ydir in directions:
                    valuetolookup = board[row][col]
                    if self.search_board(row, col, xdir, ydir, self.__winlength, valuetolookup):
                        return PatternResult(found= True, winner= board[row][col])

        return PatternResult(found= False, winner= None)


    def search_board(self, row: int, col: int, xdir: int, ydir: int, length: int, lookupvalue: str) -> bool:

        board = self.__getboard

        if lookupvalue == "":
            return False

        for i in range(length):
            r = row + i * xdir
            c = col + i * ydir
            # Check bounds and value
            if not (0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == lookupvalue):
                return False

        return True


    def game_is_tie(self) -> bool:

        board = self.__getboard

        for row in board:
            if "" in row:
                return False

        print("game is a tie")
        return True




class manualplayer(players):

    def __init__(self) -> None:
        super().__init__(name= self.get_random_name())
        self.__name = self.get_name()

    def get_move(self) -> list[str]:
        pinput = input(self.__name + ", please play your move")

        return re.findall(r'[0-9]+',pinput)



class playerAI(players):

    def __init__(self, name: str = "NPC") -> None:
        super().__init__(name=name)
        self.__name = self.get_name()

    def get_move(self) -> list[str]:
        x = str(random.randint(0, 2))
        y = str(random.randint(0, 2))
        print(self.__name + " has made a move")
        return [x,y]



def run_game(g: Gameboard, playersingame: list[players]) -> None:
    for p in playersingame:
        board = g.get_board()
        move = p.get_move()
        name = p.get_name()
        
        gameinputs = g.get_input_rules()

        while not gameinputs.valid_inputs(move) or not gameinputs.spot_is_playable(board, move):
            print("Input not valid, try again")
            move = p.get_move()

        g.set_move_on_board(move,name)
        g.display_board()
        
        winrules = g.get_win_criteria()

        if winrules.game_is_won() or winrules.game_is_tie():
            return
    run_game(g,playersingame)


if __name__ == '__main__':
    AI = playerAI()
    ttt = tictactoe()
    playersingame = [manualplayer(), AI]
    ttt.display_board()


    run_game(ttt,playersingame)