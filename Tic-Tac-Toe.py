import numpy as np
import random

from readNPYorZ import readNPYorZ
from compareRRGetStatePos import compareRRGetStatePos

#--Check if win is True--
from ifWin import ifWin

#--Check if Draw is True--
from ifDraw import ifDraw

arena = np.zeros(shape=(3,3), dtype=int)#Tic-Tac-Toe Arena/Grid
#Note 0 in grid is empty, 1 = X and -1 = O
#win = False #If winner then end program
P1UserSymbol = 'X'#User Defaults to O
P2UserSymbol = 'O'#User Defaults to X
NumPlayer = 1#Number of Players Defaults to One

##############AI
GStates = readNPYorZ("GameStatesWOreflecrot.npz")
GSvalues = [readNPYorZ("StateValuesP1.npz"),readNPYorZ("StateValuesP2.npz")]#Both Players in a list for easy usability

epsilon = -1#0.3#Exploration Rate# Made it to pick optimal everytime for strongest AI, #DEFAULT OFF
alpha = 0.0#0.137#Learning Rate #Made it smaller to learn slower, #DEFAULT OFF
#################

def show():# Can expand this to show X and O
    global arena
    print(arena)
    outImg = [['#','#','#'],['#','#','#'],['#','#','#']]
    for row in range(arena[:,0].size):
        for col in range(arena[0,:].size):
            if arena[row,col] == 1:
                outImg[row][col] = P1UserSymbol
            elif arena[row,col] == 2:
                outImg[row][col] = P2UserSymbol
            else:
                outImg[row][col] = " "
            
    print(outImg[0])#Print to console
    print(outImg[1])
    print(outImg[2])

#--User Input Function--
def PlayerInput(CurrentPlayer):
    RowPosIn = -1 #X Position Input. -1 will be default (default is purposly a bad input so that it loops)
    ColPosIn = -1 #Y Position Input.
    while (RowPosIn > 3 or RowPosIn < 1):#Simple Loop, Gives no Feedback
        print ("Player " + str(CurrentPlayer) + " Input Row position (1-3):")#Print Request to console
        RowPosIn = int(input())
    while (ColPosIn > 3 or ColPosIn < 1):#Simple Loop, Gives no Feedback
        print ("Player " + str(CurrentPlayer) + " Input Column position (1-3):")#Print Request to console
        ColPosIn = int(input())
    if arena[RowPosIn -1, ColPosIn -1] == 0:
        arena[RowPosIn -1, ColPosIn -1] = CurrentPlayer
        return True#Return Change made
    return False#Else return Change not made

#def PlayerSetup():
    #--Pre-Game Player Setup--
#    global NumPlayer
 #   NumPlayer = 0
  #  while (NumPlayer < 1 or NumPlayer > 2):
   #     print("1 or 2 Player? (1-2):")
    #    NumPlayer = int(input())
        #TEMP
    
def SymbolSetup():
    #--Pre-Game Symbol setup--
    global P1UserSymbol
    global P2UserSymbol
    P1UserSymbol = None
    P2UserSymbol = None
    #We could do only X/O but where is the fun in that
    #while(not (P1UserSymbol == "X" or  P1UserSymbol == "O")):
    #    print("Player 1 Choose your symbol (X/O):")
    #    P1UserSymbol = input().capitalize()
    #    if P1UserSymbol == "X":
    #        P2UserSymbol = "O"
    #    else:
    #        P2UserSymbol = "X"
    while(P1UserSymbol == None):
        print("Player 1 Choose your symbol: ")
        P1UserSymbol = input().capitalize()
    while(P2UserSymbol == None or P2UserSymbol == P1UserSymbol):
        print("Player 2 Choose your symbol: ")
        P2UserSymbol = input().capitalize()

def setLearnRate():
    global alpha
    UserIn = 2
    while(UserIn > 1 ):
        try:
            UserIn = int(input("Input decimal Learn Rate Value:"))
            break
        except:
            print("Input numbers only")
    alpha = UserIn

def setEpsilon():
    global epsilon
    UserIn = 2
    while(UserIn > 1 ):
        try:
            UserIn = int(input("Input decimal Exploration Value:"))
            break
        except:
            print("Input numbers only")
    epsilon = UserIn

############The important AI bit###############################
def updateGSvalue(CurrentPlayer, parent_index, child_index):
    #Note CurrentPlayer is 1 or 2, we need 0 or 1 so every CurrentPlayer needs a -1 when using Lists or np arrays
    global GSvalues
    global alpha#Learning Rate
    GSvalues[CurrentPlayer-1][parent_index] = GSvalues[CurrentPlayer-1][parent_index] + alpha*(GSvalues[CurrentPlayer-1][child_index]-GSvalues[CurrentPlayer-1][parent_index])
    #makes changes directly to global memory space so no return needed, can debug here

def exploration(CurrentPlayer, board):
    global GStates
    emptyCellsRow, emptyCellsCol = np.where(board == 0)
    randPos = random.randint(0, emptyCellsRow.size-1)
    ParentIndex = compareRRGetStatePos(board, GStates)
    boardCOPY = np.copy(board)
    boardCOPY[emptyCellsRow[randPos], emptyCellsCol[randPos]] = CurrentPlayer#For each statement like this we could check if current position is taken but thats incase things execute bad, sicne we depend on emptyRow emptyCol we assume the place is empty
    ChildIndex = compareRRGetStatePos(boardCOPY, GStates)
    return [np.copy(boardCOPY), ParentIndex, ChildIndex]
    
def exploitation(CurrentPlayer, board):
    #Note, there isn't a need for alpha-beta pruning because this is more of a breadth first search style approach, it only looks as far as the current depth
    global GStates
    global GSvalues
    ParentIndex = compareRRGetStatePos(board, GStates)#So find the ParentIndex, basically find current board in GStates
    childNodeValues = []
    childNodeGSIndex = []
    emptyCellsRow, emptyCellsCol = np.where(board == 0)
    for i in range(emptyCellsRow.size):#Note emptyCellsRow and emptyCellsCol should be and must be the exact same size otherwise somethings has gone badly wrong
        boardCOPY = np.copy(board)#Just being overly cautious
        boardCOPY[emptyCellsRow[i],emptyCellsCol[i]] = CurrentPlayer#Looking at a move
        GSindex = -1#should not be -1 after this for loop, if it is then we have messed up the GStates file.
        GSindex = compareRRGetStatePos(boardCOPY, GStates)
        if GSindex == None:
            print("ERROR, GSindex == None :( This board has not been found: " + str(boardCOPY))
        childNodeValues.append(GSvalues[CurrentPlayer-1][GSindex])#Find the GSvalue using that index found and add to an array of actions# This is a policy-less action Based approach
        childNodeGSIndex.append(GSindex)#Each index corresponds to childNodeValues
    maxCNVLIndecies = [index for index,value in enumerate(childNodeValues) if value==max(childNodeValues)]#chose the max value from the list, if tie pick at random
    playBoard = np.copy(board)#Actual move to be played
    #########DEBUG output childNodeValues
    temp = np.zeros(shape=(3,3))
    print("Empty Cell Rows: " +str(emptyCellsRow))
    print("Empty Cell Cols: " +str(emptyCellsCol))
    print("ChildNodeValues: " +str(childNodeValues))
    for i in range(emptyCellsRow.size):
        temp[emptyCellsRow[i],emptyCellsCol[i]] = childNodeValues[i]
    print(temp)
    #########
    randPos = random.choice(maxCNVLIndecies)#Changed to Choice
    playBoard[emptyCellsRow[randPos], emptyCellsCol[randPos]] = CurrentPlayer#Basically this is equivalent to playBoard = GStates[childNodeIndexValuePair[randPos][0]]
    return [playBoard, ParentIndex, childNodeGSIndex[randPos]]
    
def AI_input(CurrentPlayer, board):
    global epsilon
    boardCOPY = np.copy(board)
    if random.random() < epsilon:#Default epsilon = 0.3
        output = exploration(CurrentPlayer, boardCOPY)#Random Move
    else:#Hence eploitation = 1-epsilon = 0.7 default
        output = exploitation(CurrentPlayer, boardCOPY)#Best Move
    #updateGSvalue(CurrentPlayer, output[1], output[2])#Output is (board, ParentIndex, ChildIndex)#BAD
    updateGSvalue(1, output[1], output[2])
    updateGSvalue(2, output[1], output[2])
    #print("BoardOut")#DEBUG
    return np.copy(output[0])
    
############################################################
def Game():
    #--Game--
    global win
    global arena
    CurrentPlayer = 2#Player 1 always goes first
    show()#SHOW
    while(1):
        if (CurrentPlayer == 1):
            CurrentPlayer = 2
        else:
            CurrentPlayer = 1
        while (not PlayerInput(CurrentPlayer)):#Stuck in loop until we get a good input
            pass
        show()#SHOW
        if (ifWin(arena, CurrentPlayer)):
            print("Player " + str(CurrentPlayer) + " Wins!")
            #win = True
            break
        if (ifDraw(arena)):
            print("Draw!")
            arena = np.zeros(shape=(3,3))#Arena Reset Until Win
            show()
    #--Game Over--
    print("Game Over")

#####
def Game_HvA():#Player 1, AI = 2
    global win
    global arena
    while(1):
        #--Human--
        while (not PlayerInput(1)):
            pass
        show()
        if (ifWin(arena, 1)):
            print("Player 1 Wins!")
            #win = True
            break#Break should stop loop anyway
        if (ifDraw(arena)):
            print("Draw!")
            break
        #--AI--
        arena = AI_input(2, arena)
        show()
        if (ifWin(arena, 2)):
            print("AI Wins!")
            break
        if ifDraw(arena):
            print("Draw!")
            #arena = np.zeros(shape=(3,3))#Arena Reset Until Win
            break

#####
def Game_AvH():#AI = 1, Player 2
    global win
    global arena
    while(1):
        #--AI--
        arena = AI_input(1, arena)
        show()
        if (ifWin(arena, 1)):
            print("AI Wins!")
            break
        if ifDraw(arena):
            print("Draw!")
            break
        #--Human--
        while (not PlayerInput(2)):
            pass
        show()
        if (ifWin(arena, 2)):
            print("Player 1 Wins!")
            break#Break should stop loop anyway
        if (ifDraw(arena)):
            print("Draw!")
            #arena = np.zeros(shape=(3,3))#Arena Reset Until Win
            break

#--Game Title--
print("""
  ________________   _________   ______   __________  ______
 /_  __/  _/ ____/  /_  __/   | / ____/  /_  __/ __ \/ ____/
  / /  / // /        / / / /| |/ /        / / / / / / __/   
 / / _/ // /___     / / / ___ / /___     / / / /_/ / /___   
/_/ /___/\____/    /_/ /_/  |_\____/    /_/  \____/_____/                                                             
""")

#--Menu--
menuIn = 0
while (True):
    if menuIn == 1:
        arena = np.zeros(shape=(3,3), dtype=int)
        Game()
        menuIn = 0
    elif menuIn == 2:
        arena = np.zeros(shape=(3,3), dtype=int)
        Game_AvH()
        menuIn = 0
    elif menuIn == 3:
        arena = np.zeros(shape=(3,3), dtype=int)
        show()
        Game_HvA()
        menuIn = 0
    elif menuIn == 4:
        SymbolSetup()
        menuIn = 0
    elif menuIn == 5:
        setLearnRate()
        menuIn = 0
    elif menuIn == 6:
        setEpsilon()
        menuIn = 0
    elif menuIn == 7:
        break
    else:
        print("\n1.Human vs Human\n2.AI vs Human\n3.Human vs AI\n4.Symbols: P1: " + str(P1UserSymbol) + " P2: " + str(P2UserSymbol) + "\n5.AI Learn Rate: " + str(alpha) + "\n6.AI Exploration: " + str(epsilon)+ "\n7.Exit\n\nEnterNumber:")
        menuIn = int(input())
print("Good Bye!")
