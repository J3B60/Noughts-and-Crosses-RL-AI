import numpy as np
import math
import random

from readNPYorZ import readNPYorZ
from compareRRGetStatePos import compareRRGetStatePos

arena = np.zeros(shape=(3,3), dtype=int)#Tic-Tac-Toe Arena/Grid#Note 0 in grid is empty, 1 = X and 2 = O
P1UserSymbol = 'O'#User Defaults to O
P2UserSymbol = 'X'#User Defaults to X
NumPlayer = 1#Number of Players Defaults to One

GStates = readNPYorZ("GameStatesWOreflecrot.npz")
GSvalues = [readNPYorZ("StateValuesP1.npz"),readNPYorZ("StateValuesP2.npz")]#Both Players in a list for easy usability

epsilon = 0.3#Exploration Rate
alpha = 0.369#Learning Rate

#--User Input Function--
#def BoardInput(CurrentPlayer, XPosIn, YPosIn, board):#Alternative PlayerInput but for AI
    #if board[XPosIn -1, YPosIn -1] == 0:
        #board[XPosIn -1, YPosIn -1] = CurrentPlayer
    #return board#Return Changes or  made

from ifWin import ifWin

#--Check if Draw is True--
from ifDraw import ifDraw

############The important AI bit###############################
#THIS BIT IS OLD
#AI_input is a recursive function
#Everytime this function is called, it alternates between the TurnsPlayer
#TurnsPlayer starts as the AI player's number
#def AI_input(TurnsPlayer, decisionArena): #CurrentPlayer is just AI's number in arena #This is the Agent
#    ifWin(TurnsPlayer)
#    ifDraw(decisionArena)
#    listOfEmptyPos = []#Get list of the empty positions
#    for row in range(decisionArena[:,0].size):
#        for col in range(decisionArena[0,:].size):
#            if not (decisionArena[row,col] == 1 or decisionAarena[row,col] == 2):
#                listOfEmptyPos.append((row,col))#x,y coordinates of positions in a tuple#

#    for pos in listOfEmptyPos:#
#        decisionArena = arena#Just so nothing is changed on the original board until AI decision has been made
#        #-check if move good-
#        decisionArena[pos[0],pos[2]] = TurnsPlayer
        
#THIS BIT IS THE NEW BIT, #MinimaxGen() from GameTreeGen.py
def MinimaxGen(Depth,board):
    
    currentDepth = Depth-1
    if currentDepth ==0:#Ignore last node with branch=1, only go up to parent node with two branches, the leaves are the end states
        return

    if currentDepth%2 == 0:
        currentPlayer = 2
        previousPlayer = 1#Just need for ifWin() function
    else:
        currentPlayer = 1
        previousPlayer = 2#Just need for ifWin() function

    if ifWin(previousPlayer, np.copy(board)):#Before taking currentPlayer's move, check if the prevoiusPlayer has already won, if so stop otherwise continue
        return
    if ifDraw(np.copy(board)):#This should be equivalent to if currentDepth == 0
        return
    
    emptyCellsRow, emptyCellsCol = np.where(board == 0)

    ListOfNodes.append(np.copy(board))
    for i in range(currentDepth):#for i in range(#ofBranches)
        if not emptyCellsRow.size == 0:#and by extension, emptyCellsCol will be .size ==0
            #print(str(emptyCellsRow.size)+" "+str(board)+" "+str(currentDepth)+" "+str(i))#DEBUG
            TempBoard = np.copy(board)
            TempBoard[emptyCellsRow[i],emptyCellsCol[i]] = currentPlayer
        MinimaxGen(currentDepth,np.copy(TempBoard))

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
    ####OLD, found out updating Both AI is better. Problem with AI using prevoius method was that the AI had no idea if it won or lost since the ifWin and ifDraw breaks the loop not allowing AI to update. Also updating both is better since both AI have all board states not just their own moves
    #updateGSvalue(CurrentPlayer, output[1], output[2])#Output is (board, ParentIndex, ChildIndex)
    ####
    updateGSvalue(1, output[1], output[2])#Update BOTH AI
    updateGSvalue(2, output[1], output[2])#Update BOTH AI
    #print("BoardOut")#DEBUG
    return np.copy(output[0])
    
############################################################
def Game():#AI Training
    #--Game--
    global arena
    CurrentPlayer = 2#Player 1 always goes first
    while(1):
        if (CurrentPlayer == 1):
            CurrentPlayer = 2
        else:
            CurrentPlayer = 1
        arena = AI_input(CurrentPlayer, arena)#Usually, for Human, Stuck in loop until we get a good input
        if (ifWin(arena, CurrentPlayer)):
            break
        if (ifDraw(arena)):
            #arena = np.zeros(shape=(3,3), dtype=int)#Arena Reset Until Win #NOTE just end game when draw, otherwise P2 starts first and I don't want to have to deal with that.
            break#Just end the game and start a new one
    
#--Game Title--
print("""
  ________________   _________   ______   __________  ______         ___    ____   __________  ___    _____   ____________ 
 /_  __/  _/ ____/  /_  __/   | / ____/  /_  __/ __ \/ ____/        /   |  /  _/  /_  __/ __ \/   |  /  _/ | / / ____/ __ \
  / /  / // /        / / / /| |/ /        / / / / / / __/ (_)      / /| |  / /     / / / /_/ / /| |  / //  |/ / __/ / /_/ /
 / / _/ // /___     / / / ___ / /___     / / / /_/ / /____        / ___ |_/ /     / / / _, _/ ___ |_/ // /|  / /___/ _, _/ 
/_/ /___/\____/    /_/ /_/  |_\____/    /_/  \____/_____(_)      /_/  |_/___/    /_/ /_/ |_/_/  |_/___/_/ |_/_____/_/ |_|  
""")

#--Menu--
menuIn = 0
while int(menuIn < 1):
    print("\nStart Training\nChoose Number of Epochs:")
    menuIn = int(input())
for n in range(menuIn):
    Game()
    #print("Game Over: " + str(n))
    print("Game Over: " + str(n) + " Saving to file")
    np.savez("StateValuesP1", GSvalues[0])#Saves at every Epoch. Storage I/O slows down program
    np.savez("StateValuesP2", GSvalues[1])#Saves at every Epoch. Storage I/O slow down
    arena = np.zeros(shape=(3,3), dtype=int)
#print("Saving the GSvalues to file, Note that the training is cumulative everytime it is run, if you want to train from the begining replace the StateValuesP#.npz files with StateValuesP#Default.npz files")

#print("Saving to File")
#np.savez("StateValuesP1", GSvalues[0])#Saves at End of program
#np.savez("StateValuesP2", GSvalues[1])#Saves at End of program

print("Training Over. Good Bye!")
