import re

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
        """        self.__board = [
            ["Troy", "Cody", ""],
            ["Cody", "Troy", "Troy"],
            ["Cody", "Troy", "Cody"]
        ]"""

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


class newGame():


    def __init__(self):
        self.board = [[0,0,0],
                      [0,0,0],
                      [0,0,0]]
        self.finish = False

        #print(self.board[1])

    def displayBoard(self):
        print(str(self.board[0]) + '\n' + str(self.board[1]) + '\n' + str(self.board[2]))

    def play(self,p1, p2):
        roundNum = 0

        while self.finish==False:

            #display the board every round
            game.displayBoard()

            #figure out which player is up to move
            if roundNum % 2 == 0:
                player = p1
            else:
                player = p2

            #Ask them add the move to board
            row, col = askForMove(player)
            player.move(row, col)

            #Check if the game is over
            self.finish = checkIsOver(roundNum)
            roundNum += 1




class player():
    def __init__(self,name):
        self.name = name

    def move(self,xpos,ypos):
        #print(game.board[xpos][ypos])
        game.board[xpos][ypos] = self.name

def askForMove(player):
    validInputs = False


    while validInputs == False:
        row = input(player.name + ", input the ROW you want to play in as an integer (0-2): ")

        if row in ("0","1","2"):
            row = int(row)
            col = input(player.name + ", input COLUMN you want to play in as an integer (0-2): ")

            if col in ("0", "1", "2"):
                col = int(col)

                if type(game.board[row][col]) == int:
                    validInputs = True

                else:
                    print(game.board[row][col] + " already played there. Try again.")
            else:
                print("invalid COLUMN input. Try again.")
        else:
            print("invalid ROW input. Try again.")

    return row, col


def checkIsOver(roundNum):


    
    For reference. These are all the winning x,y coordinates.

    [[[0,0],[1,0],[2,0]], #Vertical
    [[0,1],[1,1],[2,1]], #Vertical
    [[0,2],[1,2],[2,2]], #Vertical
    [[0,0],[0,1],[0,2]], #Horizontal
    [[1,0],[1,1],[1,2]], #Horizontal
    [[2,0],[2,1],[2,2]], #Horizontal
    [[0,0],[1,1],[2,2]], #Diagonal
    [[0,2],[1,1],[2,0]]] #Diagonal
    

    #Splits the winning combinations up into row and col values to use in a for loop

    #First lookupValue
    winRow1 = [0,0,0,0,1,2,0,0]
    winCol1 = [0,1,2,0,0,0,0,2]

    #Second lookupValue
    winRow2 = [1,1,1,0,1,2,1,1]
    winCol2 = [0,1,2,1,1,1,1,1]

    #Third lookupValue
    winRow3 = [2,2,2,0,1,2,2,2]
    winCol3 = [0,1,2,2,2,2,2,0]


    if roundNum == 8:
        game.displayBoard()
        print("Cats game")
        return True



    for i in range(0,len(winRow1)):

        lookupValue1 = game.board[winRow1[i]][winCol1[i]]
        lookupValue2 = game.board[winRow2[i]][winCol2[i]]
        lookupValue3 = game.board[winRow3[i]][winCol3[i]]
        #print(lookupValue1,lookupValue2,lookupValue3)

        if type(lookupValue1) == str and lookupValue1 == lookupValue2 == lookupValue3:
            game.displayBoard()
            print(lookupValue1 + " wins")
            return True

    return False




if __name__ == '__main__':

    game = newGame()
    game.play(p1= player("Cody") , p2= player("Troy"))
    
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
            return