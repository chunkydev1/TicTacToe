import numpy as np

class Game():
    def __init__(self):
        self.__board = None
        self.__finish = False

    def create_board(self,xlength,ylength):
        self.__board = np.zeros([xlength,ylength])

    def get_board(self):
        return self.__board

    def set_board(self, xpos,ypos,name):
        self.__board[xpos][ypos] = name

    def display_board(self):
        print(self.get_board())

    def check_is_game_over(self):
        pass



class TicTacToe(Game):
    def __init__(self,pList):
        super().__init__()
        self.__validInputs = ["0","1","2"]
        self.create_board(xlength=3, ylength=3)

    def get_valid_inputs(self):
        return self.__validInputs


class GameManager:

    def __init__(self,currentGame,playerList):
        self.__game = currentGame
        self.play_turn(playerList)

    def play_turn(self,playerList):

        for player in playerList:
            self.ask_for_move(player.get_name())

    def ask_for_move(self,playerName):
        self.__playerName = playerName
        self.__playerInput = input("Enter your move: " + self.__playerName)

        self.check_if_valid_inputs(self.__playerInput)

    def check_if_valid_inputs(self,pin):
        self.__validInputs = self.__game.get_valid_inputs()

        if pin in self.__validInputs:
            print("yay")
        else:
            print("nope")


class Player:
    def __init__(self,name):
        self.__name = name

    def get_name(self):
        return self.__name


if __name__ == '__main__':
    players = [Player('Cody'),Player('Troy')]
    TTT = TicTacToe(players)
    gm = GameManager(TTT,players)
    #TTT.display_board()





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