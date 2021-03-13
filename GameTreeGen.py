import numpy as np
import itertools
from joblib import Parallel, delayed
import multiprocessing

#from MMGenParallelBlock import FromParallelModule_ParallelValidGameStateSearch

x=0
arena = np.zeros(shape=(3,3), dtype=int)
#ListOfNodes=[[],[],[],[],[],[],[],[],[],[]]#TEMP? #Sort Nodes by Depth
ListOfNodes = []
ListOfGameStates = []

def ifWin(CurrentPlayer, board):
    sym = CurrentPlayer
    if (
        np.all(board[0,0:3] == sym) or#Horizontal1
        np.all(board[1,0:3] == sym) or#Horizontal2
        np.all(board[2,0:3] == sym) or#Horizontal3
        np.all(board[0:3,0] == sym) or#Vertical1
        np.all(board[0:3,1] == sym) or#Vertical2
        np.all(board[0:3,2] == sym) or#Vertical3
        (board[0,0] == sym and board[1,1] == sym and board[2,2] == sym) or#Diag1
        (board[2,0] == sym and board[1,1] == sym and board[0,2] == sym)#Diag2
        ):#If the combination is right
        return True#Return the winners symbol
    else:
            return False

def ifDraw(Localarena):
    if np.all(Localarena != 0):
        return True
    else:
        return False

def MinimaxGen(Depth,board):
    global ListOfNodes
    currentDepth = Depth-1
    if currentDepth ==0:#Ignore last node with branch=1, only go up to parent node with two branches, the leaves are the end states
        return

    if currentDepth%2 == 0:
        currentPlayer = 2
        previousPlayer = 1#Just need for ifWin() function
    else:
        currentPlayer = 1
        previousPlayer = 2#Just need for ifWin() function

    #Note I could just pass board but I have passed np.copy(board) just incase 
    if ifWin(previousPlayer, np.copy(board)):#Before taking currentPlayer's move, check if the prevoiusPlayer has already won, if so stop otherwise continue
        return
    if ifDraw(np.copy(board)):#This should be equivalent to if currentDepth == 0
        return
    
    emptyCellsRow, emptyCellsCol = np.where(board == 0)
    ###################################################
    #if len(ListOfNodes) ==0:
    #    ListOfNodes.append(np.copy(board))
    #####TEMP, Maybe I can do these check outside this??, I've just made it append all for now just to see if things are faster

    #ListOfNodes[currentDepth].append(np.copy(board))#TEMP? # SPLIT BY DEPTH
    ListOfNodes.append(np.copy(board))

    #####
    #resultOfForLoop = False
    #for i in ListOfNodes:#UniqueBoards
    #    if np.array_equal(i, board):
    #        resultOfForLoop = True
    #        break
    #if resultOfForLoop == False:
    #    ListOfNodes.append(np.copy(board))
    ###################################################
    for i in range(currentDepth):#for i in range(#ofBranches)
        if not emptyCellsRow.size == 0:#and by extension, emptyCellsCol will be .size ==0
            #print(str(emptyCellsRow.size)+" "+str(board)+" "+str(currentDepth)+" "+str(i))#DEBUG
            TempBoard = np.copy(board)
            TempBoard[emptyCellsRow[i],emptyCellsCol[i]] = currentPlayer#######NEWED TO FIX, NEED TO SET IT TO A COPY OTHERWISE THE CHANGE FROM ONE CHILD OF THIS PARENT NODE IS CARRIED OVER TO THE OTHER CHILD
        MinimaxGen(currentDepth,np.copy(TempBoard))


####################################################################################################################################################
### THIS CODE TAKES TOO LONG, O(n^2) but for each depth
def oldDuplicateNodeSearch():
    global ListOfNodes
    ListOfGameStates = []
    resultOfForLoop = False
    loopIterationNumber = 0
    for depthlevel in ListOfNodes:
        print(loopIterationNumber)
        loopIterationNumber = loopIterationNumber + 1
        if depthlevel == []:#this is for ListOfNodes[0] which will always be empty since we skip depth 0 since we don't care about nodes with 1 branch
            continue
        else:
            for node in depthlevel:
                if len(ListOfGameStates) == 0:
                    ListOfGameStates.append(node)
                for i in ListOfGameStates:
                    if resultOfForLoop == True:
                        break
                    if np.array_equal(node, i):
                        resultOfForLoop = True
                        break
                if resultOfForLoop == False:
                    ListOfGameStates.append(node)
                resultOfForLoop = False
##########################################################

########IterTools generates 3^9 and this is compared to 9!, should be faster
def ValidGameStateSearch(ListOfGTNodes):#Trying to compare a smaller list to the GameTree
    global ListOfGameStates
    #LoopIter = 0#Debug to see speed
    for combo in itertools.product((0,1,2), repeat=9):#Generates Unique Combinations of 0,1,2 in list len=9
        #print(LoopIter)#Debug to see speed
        #LoopIter = LoopIter + 1#DEBUG to see speed
        comboState = np.asarray(combo)#Turn the unique combo into numpy array
        comboState = np.reshape(comboState, (3,3))#Turn numpy array into 3x3grid
        for node in ListOfGTNodes:
            if np.array_equal(comboState, node):#So compare a unique combination with legal states to get legal and unique combinations
                ListOfGameStates.append(comboState)
#########################################################################

#NOTE: NOT USED, USING THE ONE IMPORTED FROM MMGenParallelBlock instead
def ParallelValidGameStateSearch(combo):#Literally the same except this is parallelisable
    global ListOfNodes#Just Reading
    print()
    comboState = np.array(combo)
    comboState = np.reshape(comboState, (3,3))#Turn numpy array into 3x3grid
    for node in ListOfNodes:#Reading collisions shouldn't be an issue
        if np.array_equal(comboState, node):#So compare a unique combination with legal states to get legal and unique combinations
            return comboState

##########################################################################

print("Start")
MinimaxGen(10, np.copy(arena))#does N-1 ie if N =10, it does 9! aka fact(9)
#After running minimaxGen we get the gametree which is split by depth, now we can do cleaning and get unique game boards
print("Finished Game Tree Gen")
print("output to file")
np.savez("GameTree", ListOfNodes)

#We are skipping this bit bellow, this part if for the UniqueGameStateGen.py, This is just leftover from testing in the #scratchpad
#oldDuplicateNodeSearch()#Not good either, even though I sorted out the ListOfNodes by depth

#ValidGameStateSearch(ListOfNodes)#Again not fast enough, takes 18 days on this PC, its better but it won't finish in time

#ListOfGameStates = Parallel(n_jobs=-1, verbose=11)(delayed(ParallelValidGameStateSearch)(combo) for combo in itertools.product((0,1,2), repeat=9))#This is slower than serial, its a Windows problem, just need to put the func in another python module

#ListOfGameStates = Parallel(n_jobs=-1, prefer="threads", verbose=11)(delayed(FromParallelModule_ParallelValidGameStateSearch)(combo, ListOfNodes) for combo in itertools.product((0,1,2), repeat=9))#Imported

print("Done")
