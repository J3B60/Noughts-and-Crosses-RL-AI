from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import numpy as np
import random
import sys

from readNPYorZ import readNPYorZ
from compareRRGetStatePos import compareRRGetStatePos

#--Check if win is True--
from ifWin import ifWin

#--Check if Draw is True--
from ifDraw import ifDraw

arena = np.zeros(shape=(3,3), dtype=int)#Tic-Tac-Toe Arena/Grid
#Note 0 in grid is empty, 1 = X and -1 = O
gameType = 0
P1UserSymbol = 'X'#User Defaults to O
P2UserSymbol = 'O'#User Defaults to X
CurrentPlayer = 1#Number of Players Defaults to One

##############AI
GStates = readNPYorZ("GameStatesWOreflecrot.npz")
GSvalues = [readNPYorZ("StateValuesP1.npz"),readNPYorZ("StateValuesP2.npz")]#Both Players in a list for easy usability

epsilon = -1#0.3#Exploration Rate# Made it to pick optimal everytime for strongest AI, #DEFAULT OFF
alpha = 0.0#0.137#Learning Rate #Made it smaller to learn slower, #DEFAULT OFF
#################

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("rsc/gui/gameGUI.ui", self)

        self.Setup()
        self.show()

    def Setup(self):
        btnNameList = ["cell00","cell01","cell02","cell10","cell11","cell12","cell20","cell21","cell22"]#DOESNT WORK, C is False for some reason, maybe garbage collector removes it
        btnNumber = [0,1,2,3,4,5,6,7,8]
        self.btnList = []
        for idx, name in enumerate(btnNameList):
            self.btnList.append(self.findChild(QPushButton, name))
        self.btnList[0].clicked.connect(lambda: self.GameInput(0))#Tried doing in the for loop, tried everyting and it doesn't work so doing this manually
        self.btnList[1].clicked.connect(lambda: self.GameInput(1))
        self.btnList[2].clicked.connect(lambda: self.GameInput(2))
        self.btnList[3].clicked.connect(lambda: self.GameInput(3))
        self.btnList[4].clicked.connect(lambda: self.GameInput(4))
        self.btnList[5].clicked.connect(lambda: self.GameInput(5))
        self.btnList[6].clicked.connect(lambda: self.GameInput(6))
        self.btnList[7].clicked.connect(lambda: self.GameInput(7))
        self.btnList[8].clicked.connect(lambda: self.GameInput(8))
            
        actionHuman_vs_Human = self.findChild(QAction, "actionHuman_vs_Human")
        actionAI_vs_Human = self.findChild(QAction, "actionAI_vs_Human")
        actionHuman_vs_AI = self.findChild(QAction, "actionHuman_vs_AI")
        actionLearning_Rate = self.findChild(QAction, "actionLearning_Rate")
        actionEpsilon = self.findChild(QAction, "actionEpsilon")
        actionExit = self.findChild(QAction, "actionExit")

        actionHuman_vs_Human.triggered.connect(lambda: self.GameSetup(0))
        actionAI_vs_Human.triggered.connect(lambda: self.GameSetup(1))
        actionHuman_vs_AI.triggered.connect(lambda: self.GameSetup(2))
        actionLearning_Rate.triggered.connect(self.setLearnRate)
        actionEpsilon.triggered.connect(self.setEpsilon)
        actionExit.triggered.connect(sys.exit)

    def GameInput(self, btnNumber):
        #print("here")#DEBUG
        global gameType
        global CurrentPlayer
        global arena
        btnPos = (int((btnNumber)/3),(btnNumber)%3)
        if CurrentPlayer == 1 and arena[btnPos[0], btnPos[1]] == 0:
            self.btnList[btnNumber].setIcon(QIcon(QPixmap("rsc/img/X.png")))
            #CurrentPlayer = 2#DEBUG
        elif CurrentPlayer == 2 and arena[btnPos[0], btnPos[1]] == 0:
            self.btnList[btnNumber].setIcon(QIcon(QPixmap("rsc/img/O.png")))
            #CurrentPlayer = 1#DEBUG
        #-Play game, depending on game type
        if gameType == 0:
            rtn = Game(btnPos)
        elif gameType == 1:
            rtn = Game_AvH(btnPos)
        elif gameType == 2:
            rtn = Game_HvA(btnPos)
            
        #Update GUI#NEED THIS FOR AI MOVES
        self.GUI_Update()
        
        #-Check win, lose, draw state
        if rtn == 0:
            QMessageBox.about(self, "Tic-Tac-Toe", "Draw!")
            self.GameSetup(gameType)
        elif rtn == 1:
            plyer = "Player 1"
            if gameType == 1:
                plyer = "AI 1"
            QMessageBox.about(self, "Tic-Tac-Toe", plyer+" Wins!")
            self.GameSetup(gameType)
        elif rtn == 2:
            plyer = "Player 2"
            if gameType == 2:
                plyer = "AI 2"
            QMessageBox.about(self, "Tic-Tac-Toe", plyer+" Wins!")
            self.GameSetup(gameType)
        #else: (in other cases it will Game() will return None) therefore do nothing

    def GameSetup(self, GType):#0 = HvH, 1 = AvH, 2 = HvA, #GType just used for setting global variable gameType
        global arena
        global gameType
        arena = np.zeros(shape=(3,3), dtype=int)
        gameType = GType
        for idx in range(len(self.btnList)):
            #print(idx)#DEBUG
            self.btnList[idx].setIcon(QIcon(QPixmap("rsc/img/blank.png")))
        if gameType == 1:
            Game_AvH_AI_FirstMove()
            self.GUI_Update()

    def GUI_Update(self):
        #Update GUI#NEED THIS FOR AI MOVES
        global arena
        for idx,sym in enumerate(arena.flatten()):
            if sym == 0:
                self.btnList[idx].setIcon(QIcon(QPixmap("rsc/img/blank.png")))#SHOULD NOT HAVE TO RUN BUT JUST TO DEBUG AND SE IF THERE ARE PROBLEMS
            elif sym == 1:
                self.btnList[idx].setIcon(QIcon(QPixmap("rsc/img/X.png")))
            elif sym == 2:
                self.btnList[idx].setIcon(QIcon(QPixmap("rsc/img/O.png")))
            #else: ERROR PROBLEM, SHOULD NOT GET ANY OTHER VALUES

    def setLearnRate(self):
        global alpha
        d, okPressed = QInputDialog.getDouble(self, "Alpha","Value:", alpha, 0, 1, 10)
        if okPressed:
            alpha = d

    def setEpsilon(self):
        global epsilon
        d, okPressed = QInputDialog.getDouble(self, "Epsilon","Value:", epsilon, -1, 1, 10)
        if okPressed:
            epsilon = d

    def DEAD_MSG(self):
        QMessageBox.about(self, "Tic-Tac-Toe", "I ran out of time to deal with this in the GUI but it works in the Console Version which is tic-tac-toe.py")

#--User Input Function--
def PlayerInput(CurrentPlayer, btnPos):
    if arena[btnPos[0], btnPos[1]] == 0:
        arena[btnPos[0], btnPos[1]] = CurrentPlayer
        return True#Return Change made
    return False#Else return Change not made
    
def SymbolSetup():
    #--Pre-Game Symbol setup--
    global P1UserSymbol
    global P2UserSymbol
    P1UserSymbol = None
    P2UserSymbol = None
    while(P1UserSymbol == None):
        print("Player 1 Choose your symbol: ")
        P1UserSymbol = input().capitalize()
    while(P2UserSymbol == None or P2UserSymbol == P1UserSymbol):
        print("Player 2 Choose your symbol: ")
        P2UserSymbol = input().capitalize()

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
    randPos = random.choice(maxCNVLIndecies)
    playBoard[emptyCellsRow[randPos], emptyCellsCol[randPos]] = CurrentPlayer#Basically this is equivalent to playBoard = GStates[childNodeIndexValuePair[randPos][0]]
    return [playBoard, ParentIndex, childNodeGSIndex[randPos]]
    
def AI_input(CurrentPlayer, board):
    global epsilon
    boardCOPY = np.copy(board)
    if random.random() < epsilon:#Default epsilon = 0.3
        output = exploration(CurrentPlayer, boardCOPY)#Random Move
    else:#Hence eploitation = 1-epsilon = 0.7 default
        output = exploitation(CurrentPlayer, boardCOPY)#Best Move
    updateGSvalue(1, output[1], output[2])
    updateGSvalue(2, output[1], output[2])
    #print("BoardOut")#DEBUG
    return np.copy(output[0])
    
############################################################
def Game(btnPos):
    #--Game--
    global CurrentPlayer
    global arena
    if not PlayerInput(CurrentPlayer, btnPos):#If move wasn't valid just stop function using return
        return None
    #print(arena)#DEBUG
    if (ifWin(arena, CurrentPlayer)):
        #print("Player " + str(CurrentPlayer) + " Wins!")#DEBUG console
        return CurrentPlayer#END GAME
    if (ifDraw(arena)):
        #print("Draw!")#DEBUG console
        return 0#END GAME
    if (CurrentPlayer == 1):
        CurrentPlayer = 2
    else:
        CurrentPlayer = 1

#####
def Game_HvA(btnPos):#Player 1, AI = 2
    global arena
    #--Human--
    if not PlayerInput(1, btnPos):
        return None
    if (ifWin(arena, 1)):
        return CurrentPlayer
    if (ifDraw(arena)):
        return 0
    arena = AI_input(2, arena)
    if (ifWin(arena, 2)):
        return 2
    if ifDraw(arena):
        return 0

#####
def Game_AvH(btnPos):#AI = 1, Player 2
    global arena
    #--Human--
    if not PlayerInput(2, btnPos):
        return None
    if (ifWin(arena, 2)):
        return 2
    if (ifDraw(arena)):
        return 0
    #--AI--###############NOTE AI PLAYES FIRST MOVE OUT SIDE OF THIS FUNCTION
    arena = AI_input(1, arena)
    if (ifWin(arena, 1)):
        return 1
    if ifDraw(arena):
        return 0
    
def Game_AvH_AI_FirstMove():
    global arena
    arena = AI_input(1, arena)

app = QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())
