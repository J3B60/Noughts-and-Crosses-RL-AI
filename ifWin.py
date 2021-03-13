import numpy as np

def ifWin(arena, CurrentPlayer):
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
