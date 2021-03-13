import numpy as np

arena = np.zeros(shape=(3,3))#Tic-Tac-Toe Arena/Grid
#Note 0 in grid is empty, 1 = X and -1 = O
win = False #If winner then end program
P1UserSymbol = 'O'#User Defaults to O
P2UserSymbol = 'X'#User Defaults to X
NumPlayer = 1#Number of Players Defaults to One

def show():# Can expand this to show X and O
    global arena
    outImg = [['#','#','#'],['#','#','#'],['#','#','#']]
    for y in range(arena[:,0].size):
        for x in range(arena[0,:].size):
            if arena[y,x] == 1:
                outImg[x][y] = P1UserSymbol
            elif arena[y,x] == 2:
                outImg[x][y] = P2UserSymbol
            else:
                outImg[x][y] = " "
            
    print(outImg[0])#Print to console
    print(outImg[1])
    print(outImg[2])

#--User Input Function--
def PlayerInput(CurrentPlayer):
    XPosIn = -1 #X Position Input. -1 will be default (default is purposly a bad input so that it loops)
    YPosIn = -1 #Y Position Input.
    while (XPosIn > 3 or XPosIn < 1):#Simple Loop, Gives no Feedback
        print ("Player " + str(CurrentPlayer) + " Input X position (1-3):")#Print Request to console
        XPosIn = int(input())
    while (YPosIn > 3 or YPosIn < 1):#Simple Loop, Gives no Feedback
        print ("Player " + str(CurrentPlayer) + " Input Y position (1-3):")#Print Request to console
        YPosIn = int(input())
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
def ifDraw():
    global arena
    if np.all(arena != 0):
        return True
    else:
        return False

def PlayerSetup():
    #--Pre-Game Player Setup--
    global NumPlayer
    NumPlayer = 0
    while (NumPlayer < 1 or NumPlayer > 2):
        print("1 or 2 Player? (1-2):")
        NumPlayer = int(input())
        #TEMP
    
def SymbolSetup():
    #--Pre-Game Symbol setup--
    global P1UserSymbol
    global P2UserSymbol
    P1UserSymbol = '#'
    while(not (P1UserSymbol == "X" or  P1UserSymbol == "O")):
        print("Player 1 Choose your symbol (X/O):")
        P1UserSymbol = input().capitalize()
        if P1UserSymbol == "X":
            P2UserSymbol = "O"
        else:
            P2UserSymbol = "X"

############The important AI bit###############################


#AI_input is a recursive function
#Everytime this function is called, it alternates between the TurnsPlayer
#TurnsPlayer starts as the AI player's number
def AI_input(TurnsPlayer, decisionArena): #CurrentPlayer is just AI's number in arena
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
    show()#SHOW
    while(not win):
        if (CurrentPlayer == 1):
            CurrentPlayer = 2
        else:
            CurrentPlayer = 1
        while (not PlayerInput(CurrentPlayer)):#Stuck in loop until we get a good input
            pass
        show()#SHOW
        if (ifWin(CurrentPlayer)):
            print("Player " + str(CurrentPlayer) + " Wins!")
            win = True
            break
        if (ifDraw()):
            print("Draw!")
            arena = np.zeros(shape=(3,3))#Arena Reset Until Win
            show()
    #--Game Over--
    print("Game Over")

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
        Game()
        menuIn = 0
    elif menuIn == 2:
        PlayerSetup()
        menuIn = 0
    elif menuIn == 3:
        SymbolSetup()
        menuIn = 0
    elif menuIn == 4:
        break
    else:
        print("\n1.Start\n2.Players (1/2): " + str(NumPlayer) + "\n3.Symbols: P1: " + str(P1UserSymbol) + " P2: " + str(P2UserSymbol) + "\n4.Exit\n\nEnterNumber:")
        menuIn = int(input())
print("Good Bye!")
