import numpy as np
import math

arena = np.zeros(shape=(3,3))#Tic-Tac-Toe Arena/Grid
#Note 0 in grid is empty, 1 = X and -1 = O
win = False #If winner then end program
P1UserSymbol = 'O'#User Defaults to O
P2UserSymbol = 'X'#User Defaults to X
NumPlayer = 1#Number of Players Defaults to One

#Create states
AI_1_stateValuesDepth0 = np.zeros(shape=(9))#Depth 0 has 9 options, Depth 1 has 8, 2-7,3-6,4-5,5-4,6-3,7-2,8-1,9-0ie draw
AI_1_stateValuesDepth1 = np.zeros(shape=(9,8))
AI_1_stateValuesDepth2 = np.zeros(shape=(8,7))
AI_1_stateValuesDepth3 = np.zeros(shape=(7,6))
AI_1_stateValuesDepth4 = np.zeros(shape=(6,5))
AI_1_stateValuesDepth5 = np.zeros(shape=(5,4))#####????????????
AI_1_stateValuesDepth6 = np.zeros(shape=(4,3))
AI_1_stateValuesDepth7 = np.zeros(shape=(3,2))
AI_1_stateValuesDepth8 = np.zeros(shape=(2,1))

#--User Input Function--
def PlayerInput(CurrentPlayer):
    if arena[XPosIn -1, YPosIn -1] == 0:
        arena[XPosIn -1, YPosIn -1] = CurrentPlayer
        return True#Return Change made
    return False#Else return Change not made

#--Check if win is True--
def ifWin(CurrentPlayer):
    global arena
    sym = CurrentPlayer
    if (
        np.all(arena[0,0:3] == sym) or#Horizontal1
        np.all(arena[1,0:3] == sym) or#Horizontal2
        np.all(arena[2,0:3] == sym) or#Horizontal3
        np.all(arena[0:3,0] == sym) or#Vertical1
        np.all(arena[0:3,1] == sym) or#Vertical2
        np.all(arena[0:3,2] == sym) or#Vertical3
        (arena[0,0] == sym and arena[1,1] == sym and arena[2,2] == sym) or#Diag1
        (arena[2,0] == sym and arena[1,1] == sym and arena[0,2] == sym)#Diag2
        ):#If the combination is right
        return True#Return the winners symbol
    else:
            return False

#--Check if Draw is True--
def ifDraw(Localarena):
    if np.all(Localarena != 0):
        return True
    else:
        return False

############The important AI bit###############################


#AI_input is a recursive function
#Everytime this function is called, it alternates between the TurnsPlayer
#TurnsPlayer starts as the AI player's number
def AI_input(TurnsPlayer, decisionArena): #CurrentPlayer is just AI's number in arena #This is the Agent
    ifWin(TurnsPlayer)
    ifDraw(decisionArena)
    listOfEmptyPos = []#Get list of the empty positions
    for row in range(decisionArena[:,0].size):
        for col in range(decisionArena[0,:].size):
            if not (decisionArena[row,col] == 1 or decisionAarena[row,col] == 2):
                listOfEmptyPos.append((row,col))#x,y coordinates of positions in a tuple

    for pos in listOfEmptyPos:
        decisionArena = arena#Just so nothing is changed on the original board until AI decision has been made
        #-check if move good-
        decisionArena[pos[0],pos[2]] = TurnsPlayer
        



############################################################
def Game():
    #--Game--
    global win
    global arena
    CurrentPlayer = 2#Player 1 always goes first
    while(not win):
        if (CurrentPlayer == 1):
            CurrentPlayer = 2
        else:
            CurrentPlayer = 1
        while (not AI_input(CurrentPlayer, arena)):#Stuck in loop until we get a good input
            pass
        if (ifWin(CurrentPlayer)):
            win = True
            break
        if (ifDraw(arena)):
            arena = np.zeros(shape=(3,3))#Arena Reset Until Win

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
print("\nStart Training\nChoose Number of Epochs:")
menuIn = int(input())
for n in range(menuIn):
    Game()
    print("Game Over: " + str(n))
print("Training Over. Good Bye!")
