import re
import abc

class Game(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def set_move_on_board(self,move,name):
        pass

    #unused
    @abc.abstractmethod
    def get_board(self):
        pass

    @abc.abstractmethod
    def display_board(self):
        pass

    @abc.abstractmethod
    def valid_inputs(self,playerinputs):
        pass

    @abc.abstractmethod
    def spot_is_playable(self,playerinputs):
        pass

    #unused
    @abc.abstractmethod
    def get_valid_inputs(self):
        pass

    @abc.abstractmethod
    def game_is_won(self,name):
        pass

    @abc.abstractmethod
    def check_pattern(self, length):
        pass

    @abc.abstractmethod
    def search_board(self, row, col, xdir, ydir, length):
        pass

    @abc.abstractmethod
    def game_is_tie(self):
        pass


class tictactoe(Game):

    def __init__(self):
        self.__board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.__validinputs = ["0","1","2"]
        self.__winlength = 3


    def set_move_on_board(self,playermove,name):
        x = int(playermove[0])
        y = int(playermove[1])

        self.__board[x][y] = name

    def get_board(self):
        return self.__board

    def display_board(self):
        for row in self.__board:
            print(row)

    def valid_inputs(self,playerinputs):
        if len(playerinputs) != 2:
            return False

        for pi in playerinputs:
            if pi not in self.__validinputs:
                #print("not valid")
                return False
        #print("valid")
        return True

    def spot_is_playable(self,playerinputs):
        x = int(playerinputs[0])
        y = int(playerinputs[1])

        if self.__board[x][y] != "":
            #print("not playable")
            return False
        #print("playable")
        return True


    def get_valid_inputs(self):
        return self.__validinputs


    def game_is_won(self,playername):
        found, winner = self.check_pattern(self.__winlength)
        if found:
            self.display_board()
            print("Winner: " +winner)
            return True


    def check_pattern(self, length):

        rows = len(self.__board)
        cols = len(self.__board[0])

        #             right,   down, right+down, left+down
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(rows):
            for col in range(cols):
                for xdir, ydir in directions:
                    if self.search_board(row, col, xdir, ydir, length):
                        return True, self.__board[row][col]

        return False, None


    def search_board(self, row, col, xdir, ydir, length):

        lookupvalue = self.__board[row][col]
        if lookupvalue == "":
            return False

        for i in range(length):
            r = row + i * xdir
            c = col + i * ydir
            # Check bounds and value
            if not (0 <= r < len(self.__board) and 0 <= c < len(self.__board[0]) and self.__board[r][c] == lookupvalue):
                return False

        return True


    def game_is_tie(self):
        for row in self.__board:
            if "" in row:
                return False

        self.display_board()
        print("game is a tie")
        return True



class Player():

    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def get_move(self):
        pinput = input(self.__name + ", please play your move")

        return re.findall(r'[0-9]+',pinput)


    #Unsure where this game_in_progress should go.
    #Part of me wants it in the game object because the game is responsible for doing game things (the game flow)....
    #BUT the game doesn't know anything about a player object so I know this isn't correct.

def game_in_progress(g,players):
    for p in players:
        g.display_board()
        pname = p.get_name()

        move = p.get_move()
        while not g.valid_inputs(move) or not g.spot_is_playable(move):
            print("Inputs not valid, try again")
            move = p.get_move()
        g.set_move_on_board(move,pname)
        if g.game_is_won(pname) or g.game_is_tie():
            return False
    return True


if __name__ == '__main__':
    ttt = tictactoe()
    players = [Player("Cody"), Player("Troy")]

    #please don't judge me too hard for this. I am unsure how to nicely facilitate the game.
    while game_in_progress(ttt, players):
        pass








"""import re

## Comments:
## - You have a bunch of unused variables in method calls
## - Players should be responsible for their own moves. This is for 2 reasons:
## -- 1) That way you can test player behavior independent of other classes.
## -- 2) That way you can encapsulate the behavior of a player
## -- -- (e.g. you could have 2 different player classes passed into the game at creation)
## - I like your use of Game -> TicTacToe inheritence, but I'd recommend moving content out
## - - out of Game and start to leverage the base class as more of an interface rather than an abstract class
## - - You're spreading the content out in a way that is confusing - for example 'check_catsgame' is in generic `Game` class.
## - - Game makes sense to be an interface OR a template class.  (See bottom for examples)
## - Single source of truth
## - - This isn't something we've talked about much but you're repeating yourself in the code and you should never do that.
## - - The big example is in the Game class you have a method called "search_board" and "set_board" but then later
## - - you are manually checking the content (self._board[x][y] == ?) or setting content. If your logic was wrong,
## - - you'd have to refactor a bunch of code rather than just one place.

## This pass
# - remove unused variables.
# - check out any !!! comments

class Game():
    def __init__(self):
        self.__board = None
        self.__finish = False

    def create_board(self,xlength,ylength):
        self.__board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]

    def get_board(self):
        return self.__board

    ## !!! Accepts illegal values (e.g. xpos and ypos out of bounds)
    def set_board(self, xpos,ypos,name):
        self.__board[int(xpos)][int(ypos)] = name

    def display_board(self):
        self.__board = self.get_board()
        for row in self.__board:
            print(row)

    ## What the hell is dr dc?
    def search_board(self, row, col, dr, dc, length):

        value = self.__board[row][col]
        if value == "":
            return False

        for i in range(length):
            r = row + i * dr
            c = col + i * dc
            # Check bounds and value
            if not (0 <= r < len(self.__board) and 0 <= c < len(self.__board[0]) and self.__board[r][c] == value):
                return False

        return True

    def check_pattern(self, length):

        rows = len(self.__board)
        cols = len(self.__board[0])

        #            right, down, diagonal-r, diagonal-l
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(rows):
            for col in range(cols):
                for dr, dc in directions:
                    ## !!! Consider improved naming for dr/dc naming
                    ## Feel free to use helper functions to avoid impossibly long functions
                    if self.search_board(row, col, dr, dc, length):
                        return True, self.__board[row][col]

        return False, None

    def check_catsgame(self):
        self.__board = self.get_board()
        for row in self.__board:
            if '' in row:
                return False

        return True

    def is_game_over(self):
        # Check for a winner (3 in a row)
        found, winner = self.check_pattern(3)
        catsGame = self.check_catsgame()
        if found:
            print(f"Winner: {winner}")
            return True
        elif catsGame:
            print("No one wins, it's a cats-game")
            return True



class TicTacToe(Game):
    def __init__(self,plist):
        super().__init__()
        self.__validInputs = ["0","1","2"]
        self.create_board(xlength=3, ylength=3)
        self.__board = self.get_board()

    def get_valid_inputs(self):
        return self.__validInputs

    def add_move_to_board(self, move,name):
        self.__xpos = int(move[0])
        self.__ypos = int(move[1])
        ## !!! You're directly modifying the board rather than using the interfaced methods.
        ## You implement the interface, so respect it.
        self.__board[self.__xpos][self.__ypos] = name

    def is_spot_played(self,move):
        ## !!! You should be using your search methods here!! You implement the interface, respect it.
        if self.__board[int(move[0])][int(move[1])] == "":
            return False
        else:
            return True


class GameManager:

    def __init__(self,currentgame,playerlist):
        self.__currentGame = currentgame
        self.__players = playerlist
        self.__validInputs = None
        self.__playerInput = None

    def run_game(self):

        while not self.__currentGame.is_game_over():
            #print("new loop")
            self.play_turn(self.__players)
        #print("finished running game")


    def play_turn(self,playerList):

        for player in playerList:
            self.__currentGame.display_board()
            self.ask_for_move(player.get_name())
            if self.__currentGame.is_game_over():
                return


    def ask_for_move(self,playername):
        ## !!! Players should manage their own moves!
        self.__playerName = playername
        self.__playerInput = input(self.__playerName + ", enter your move in this format: row,col")

        if not self.check_if_valid_inputs() or self.__currentGame.is_spot_played(self.__playerInput):
            print("Not valid. Asking again")
            self.ask_for_move(self.__playerName)
        else:
            #print("everything looks good")
            self.__currentGame.add_move_to_board(self.__playerInput,self.__playerName)

    def check_if_valid_inputs(self):
        ## !!! The board should manage validity. You created a class to hold the board, so that should be the one to
        ## error check the content. However, in the context of the game you still need someone to manage the flow.
        ## So while you're close here (in the sense that you do need a method to facilitate the getting -> checking)
        ## The wrong clases are doing the checking.
        ##
        ## Ask yourself: Who is responsible about this? Who knows about this?
        self.__validInputs = self.__currentGame.get_valid_inputs()
        self.__playerInput = re.findall(r'[0-9]+',self.__playerInput)

        for val in self.__playerInput:
            if val not in self.__validInputs:
                print("Invalid Input, try again")
                return False

        #print("Done checking inputs")
        return True


class Player:
    def __init__(self,name):
        self.__name = name

    def get_name(self):
        return self.__name


if __name__ == '__main__':
    players = [Player('Cody'),Player('Troy')]
    TTT = TicTacToe(players)

    GameManager(TTT,players).run_game()

    TTT.display_board()
    """
    
    
"""----------------------------------------------------------------------------------------------"""
    

"""
import abc
class GameInterfaceExample(abc.ABC):
    '''
        This game interface has a bucnch of content about a specific game board, but it doesn't implement
        any of the behaviors, this is becuase it's JUST an interface. While this seems pedantic now, it comes with
        more value later.
    '''

    @abc.abstractmethod
    def initialize_game_board(self, max_x, max_y):
        pass

    @abc.abstractmethod
    def set_board(self, x_pos, y_pos, content):
        pass

    @abc.abstractmethod
    def get_board(self):
        pass

    @abc.abstractmethod
    def display(self):
        pass

    @abc.abstractmethod
    def is_game_over(self):
        pass

    @abc.abstractmethod
    def is_game_tie(self):
        pass


import abc


class GameTemplateExample(abc.ABC):

    '''
        This example is used to demonstrate how you can combine the interface and
        abstract class patterns to create a "template" class. A template class is one of the few
        areas where I actually use abstract classes - otherwise it's just an interface.

        The idea is that there exists 1 common algorithm that's shared across all classs instances
        In this cases it's "initialize_square_game_board."

        However, that method will leverage interfaced methods to do the actual work
        As is shown by set_board_content and build_empty_square_board.

        This pattern allows you to reuse a specific structure but change the output by modifying ONLY the methods
        that are doing work, while keeping the general pattern the same.

    '''

    def __init__(self):
        self._board = None

    @abc.abstractmethod
    def build_empty_square_board(self, max_x, max_y):
        pass

    @abc.abstractmethod
    def set_board_content(self, x_pos, y_pos, content):
        pass

    def initialize_square_game_board(self, max_x, max_y, default_value):
        self._board = self.build_empty_square_board(max_x, max_y)
        for column in self._board:
            for row in column:
                self.set_board_content(column, row, default_value)

'''
    Example of how I would think about your play_turn method. 
    
    Note that excluding 'self.' there are 0 calls to direct objects. 
    everything is 'get an object from x and move it over there' 
    This is the heart of object oriented programming. You're either building:
     - A class that holds and manipulates data or objects
     - A class that holds data or objects 
'''
def play_turn(self, player_list):
    for player in player_list:
        self.__current_game.display_board()
        move = player.get_move()
        if not self.__current_game.is_valid(move):
            raise RuntimeError("Invalid Move")
        self.__current_game.make_move(player, move)
        if self.__currentGame.is_game_over():
            return"""