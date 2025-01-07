import re
import abc
import random
import names
from dataclasses import dataclass
from typing import Optional


class Gameboard(abc.ABC):

    @abc.abstractmethod
    def set_move_on_board(self, move: list[str], name: str) -> None:
        pass

    # unused
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

    def __init__(self, inputs: list[str]) -> None:
        self.__vinputs = inputs

    @abc.abstractmethod
    def valid_inputs(self, playerinputs: list[str]) -> bool:
        pass

    # spot_is_playable could be in gameboard because its sole responsibility is to look at the board, but I think its better here because the rules of a valid input are 2 things:
    # 1- must be within bounds (def valid_inputs)
    # 2- must be a location not already played (spot_is_playable).
    @abc.abstractmethod
    def spot_is_playable(self, board: list[list[str]], playerinputs: list[str]) -> bool:
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

    def __init__(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str) -> None:
        self.name = name

    @abc.abstractmethod
    def get_move(self) -> list[str]:
        pass

    def get_random_name(self) -> str:
        randname = names.get_first_name()
        return randname


### A thought on "Interfaces"
### 
### Often times your implementation/the choices you make about your design 
### will determine what the interface should be, and while that's a great place 
### to start it can lead to backwards interfaces. 
### 
### What is an example of that? Let's look at your Player interface
### you includes the "set_name" method in the public scope. That means that 
### a future developer could (in theory) change the name of a player during the game.
### That would be (IMO) a bugged experience for future developers. 
###
### When you define an interface I often find it valuable to think about less being more. 
### Determine the flow of the code, but also determine what's ABSOLUTELY necessary, 
### think about how your interface could be abused, and what objects should REALLY be in charge of the data/behavior.
### 
### In the case of tic-tac-toe some of those thoughts are wildly overkill. But 
### They're important for bigger projects so I gotta mention them. 
###
### Another example of your interface design that works and is not problematic now, 
### but could be in the future: The wincriteria <-> gameboard relationship. 
### Wincriteria holds an instance of a gameboard - 100% good call. 
### wincriteria has a "search_board" method, i'm not sure if that's a good call - it's a bit clunky at best. 
### it means that wincriteria has to have some kind of understanding of what 
### the board is made up of/looks like. This could be somewhat solved 
### by wrapping "row: int, col: int, xdir: int, ydir: int," in a helper class 
### that's like "board-node" or something, but the bigger problem is what's 
### being implemented later. The fact that the "check_pattern" and "search_board" methods
### are indirectly operating ON the board. 
### 
### Some Alternative options: 
### 
### # The board can be iterated over (gameboard supports forloops directly)
### for node in board: 
###     ...
### 
###
### # gameboard has a "get neighbors" method or "get_directed_neighbor" class: 
### from_node = ... # Starting location
### horizontal = [starting_node] + board.get_directed_neighbor(direction=horizontal, start=from_node, include_start=True)
### vertical = [starting_node] + board.get_directed_neighbor(direction=vertical, start=from_node, include_start=True)
### diag_one = [starting_node] + board.get_directed_neighbors(direction=y_equals_x, start=from_node, include_start=True)
### diag_two = [starting_node] + board.get_directed_neighbors(direction=y_equals_negative_x, start=from_node, include_start=True)
### to_check = [horizontal, vertical, diag_one, diag_two]
### 
### The idea is that every class has it's 1 responsibility but also that it only 
### has knowledge/direct access to it's 1 thing. 
### Often times we see those responsibilities bleed between the lines, but at the onset 
### it's can be valuable to try to gate keep them clean and refactor at the end if 
### you let them co-mingle. 



class tictactoe(Gameboard):

    def __init__(self) -> None:
        self.__board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.__validinputs = ["0", "1", "2"]
        self.__winlength = 3

        ### Rules and win condition should be passed in
        ### having them directly implemented makes it more difficult on you later 
        ### when it comes to testing. Imagine if in your tests you just did something like: 
        ### 
        ### class MockInputRules(InputRules): ... 
        ### class MockWinCriteria(WinCriteria): ... 
        ### 
        ### And then assembled your gameboard from there? It works similarly to what you 
        ### actually did, but simplifies what's happening. Also, the way you did mock/patch
        ### don't really work in other languages. You need to pass actual objects in 
        ### rather than rewrite what's available. Some languages have ways to hide/replace 
        ### but if at the onset you're designing the flexibility in, it creates more options 
        self.__rules = tttinputrules(self.__validinputs)
        self.__win = tttwin(self.get_board(), self.__winlength)

    def set_move_on_board(self, playermove: list[str], name: str) -> None:
        ### I'm not sure if you've thought about it, but this List[Str] shenanigans for a move
        ### Creates a bunch of extra code for you all over the place. 
        ### 
        ### Something like "class PlayerMove" would probably simplify.
        ### AGAIN, that's probably uneccessary for the scale of this code, but it's one 
        ### of those things where if you practice like you play then you play 
        ### better in the long run... Something to think about. 
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

    ### Why are we passing in the valid inputs for the tictac toe rules? 
    ### do valid inputs for tic tac toe ever change? 
    ### if anything, they should be an optional argument and defaulted
    def __init__(self, inputs: list[str]) -> None:
        super().__init__(inputs)
        ### I don't know why you do this, it's really weird. 
        ### you have self.__validinputs and self.__vinputs and self.get_valid_inputs()
        ### Why the re-definition in the child? Just use self.get_valid_inputs() 
        ### whenever you need __validinputs
        self.__validinputs = self.get_valid_inputs()

    def valid_inputs(self, playerinputs: list[str]) -> bool:
        ### This is one of the things I was getting at by the comment about "class PlayerMove"
        ### There are things you don't need to check when you've controlled them via 
        ## a class. 
        if len(playerinputs) != 2:
            return False


        ### Minor python optimization :
        ### return all([pi in self.get_valid_inputs() for pi in playerinputs])
        ### 
        ### I think it's helpful to think about things in terms of list comprehension
        ### and list actions. It's just a bit more pythonic. Not all languages
        ### have this type of toolset, but I think it's valuable to consider the 
        ### tools the language provides. 
        for pi in playerinputs:
            if pi not in self.__validinputs:
                # print("not valid")
                return False
        # print("valid")
        return True

    def spot_is_playable(self, board: list[list[str]], playerinputs: list[str]) -> bool:
        x = int(playerinputs[0])
        y = int(playerinputs[1])

        ### Personal Ick: I hate if X return True else False paradigms because 
        ### you could just return X... 
        ###
        ### return (board[x][y] == "")
        if board[x][y] != "":
            # print("not playable")
            return False
        # print("playable")
        return True


### Love your use of a data class here. Think you should 
### considere where else it can be applied. 
@dataclass
class PatternResult:
    found: bool
    winner: Optional[str]

# ## Named Tuple Example: 
# from collections import namedtuple
# PatternResult = namedtuple('PatternResult', ['found', 'winner'])



class tttwin(WinCriteria):

    def __init__(self, getboard: callable(Gameboard), winlength: int) -> None:
        super().__init__(getboard, winlength)
        ### Bruh, this overwriting the parent object habbit you have is bad. 
        ### you have to stop it. It defeats the purpose of shared inheritence. 
        self.__winlength = self.get_win_length()
        self.__getboard = getboard

    def game_is_won(self) -> bool:

        found, winner = self.check_pattern()
        if found:
            print("Winner: " + winner)
            return True

    def check_pattern(self) -> PatternResult:

        ### I'm not sure I understand how this works... 
        ### self.__board is a callable gameboard, but in other places you pass in 
        ### "self.__win = tttwin(self.get_board(), self.__winlength)"
        ### self.get_board() just returns a 2x2 array. That array isn't callable... 
        ###
        ### I think that your tests are only working because you're passing in a fixture: 
        ### return Main.tttwin(getboard=mock_get_board, winlength=3)
        ###
        ### This reads like code that was written to pass a test, not code that 
        ### passes functional behaviors... 
        board = self.__getboard()
        # print(f"board recieved: {type(board)}")

        rows = len(board)
        cols = len(board[0])

        #             right,   down, right+down, left+down
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        ### Why row in range(rows)? Why not just iterate over the board? 
        ### for row in board: 
        ###     for col in board[row]
        for row in range(rows):
            for col in range(cols):
                for rdir, cdir in directions:
                    valuetolookup = board[row][col]
                    if self.search_board(row, col, rdir, cdir, self.__winlength, valuetolookup):
                        return PatternResult(found=True, winner=board[row][col])

        return PatternResult(found=False, winner=None)

    def search_board(self, row: int, col: int, rdir: int, cdir: int, length: int, lookupvalue: str) -> bool:

        board = self.__getboard()

        if lookupvalue == "":
            return False

        for i in range(length):
            r = row + i * rdir
            c = col + i * cdir
            # Check bounds and value
            if not (0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == lookupvalue):
                return False

        return True

    def game_is_tie(self) -> bool:
        ### Nit: Gamestate should be cached so you don't have to iterate over the whole board 
        ### whenever you want to know something about it. Right now 
        ### if you call "game_is_tie" repeatedly it will take O(BoardSize) everytime. 
        ### It should be O(1)
        ###
        ### NOTE: If you've not heard of O(?) notation, it's the number of comparisons 
        ### you have to make to know something. Examples: 
        ### * Is item N in unsorted list M, you have to check every M[X] to know, O(len(M))
        ### * Is item N in SORTED list M, you have to check part of the list: O(log(n))
        ### * If you have to check if there are any duplicates in an unsorted list, 
        ###   It would be O(N^2) because you'd have to compare every element to every element 
        ###   in the list 
        ### * Same as above but a sorted list: O(n log n)
        ### * Same as above but by using a dictionary O(N)'ish - more complicated because the insertions 
        ###   into the dictionary could be nlog(n) but the lookup of any element is O(1)
        board = self.__getboard()

        for row in board:
            if "" in row:
                return False

        print("game is a tie")
        return True


class manualplayer(players):

    def __init__(self) -> None:
        ### Wait, I'm reviewing in reverse right now  
        ### You're using get_random_name for manual players lol 
        ### Use it for AI players too!
        super().__init__(name=self.get_random_name())
        self.__name = self.get_name()

    def get_move(self) -> list[str]:
        pinput = input(self.__name + ", please play your move")
        ### OOOOOOOoooOOooOOOooo look at this hot shot using regex. 
        ### I hate regex, not because it's bad, it's actually the RIGHT 
        ### solution far too often. But the search language for regex 
        ### is so incredibly frustrating to me lol 
        return re.findall(r'[0-9]+', pinput)


class playerAI(players):

    def __init__(self, name: str = "NPC") -> None:
        ### This is good, but a thought for the future: 
        ### Knowing what problems you'll find in the future is hard when 
        ### you've not run into them before.
        ### 
        ### One super common problem is decoding "who's doing what" 
        ### and in this case, your default initiailzation of an AI player 
        ### is always "NPC", so you can't tell the difference between any 
        ### 2 players. 
        ### 
        ### While ENTIRELY unecessary for this code, a "nice to have" 
        ### that you can consider for the future: Set the name to an empty 
        ### string as a default, and in the init, instead of name=name, do something like: 
        ### name=(name if name != '' else self.__get_unique_name()) 
        ### 
        super().__init__(name=name)
        self.__name = self.get_name()

    def get_move(self) -> list[str]:
        x = str(random.randint(0, 2))
        y = str(random.randint(0, 2))
        print(self.__name + " has made a move")
        return [x, y]

###
### I really like your use of "run_game" here. This is an EXCELLENT example of 
### using interfaced objects to do a thing. Everything in this is as generic 
### as worth doing (you can always make thing more generic, but there's a line and you 
### walked right up to it and nailed it - I think at least). 
###
### For the level you're writing code, this is more than perfect. Way to punch up. 
### 
def run_game(g: Gameboard, playersingame: list[players]) -> None:
    for p in playersingame:
        board = g.get_board()
        move = p.get_move()
        name = p.get_name()

        gameinputs = g.get_input_rules()

        while not gameinputs.valid_inputs(move) or not gameinputs.spot_is_playable(board, move):
            print("Input not valid, try again")
            move = p.get_move()

        g.set_move_on_board(move, name)
        g.display_board()

        winrules = g.get_win_criteria()

        if winrules.game_is_won() or winrules.game_is_tie():
            return

    ### Although I find this implementation "perfect" from a design standpoint...
    ### 
    ### I have a complaint about you using recursion here 
    ### but that's more about a personal ick than a real software problem. 
    ### To do it without recursion you could do: 
    ###
    ### while g.still_has_moves(): 
    ###     for p in playersingame:
    ###         ## Your existing code... 
    ###         ....
    ### return 
    run_game(g, playersingame)


if __name__ == '__main__':
    AI = playerAI()
    ttt = tictactoe()
    playersingame = [manualplayer(), AI]
    ttt.display_board()

    run_game(ttt, playersingame)
