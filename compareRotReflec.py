import numpy as np

def compareRotReflec(State, inputGS):#NOTE DONT PASS ALL STATES, PASS THE LIST YOU ARE BULDING, WE DON'T WANT DUPLICATES IN LIST
    for i in inputGS:
        if np.array_equal(State, i):#Note we should never reach this if list is being built, we shouldn't have duplicates either
            return False
        elif (np.array_equal(np.fliplr(State), i) or
              np.array_equal(np.flipud(State), i) or
              np.array_equal(np.rot90(State, 3), i) or
              np.array_equal(np.rot90(State, 2), i) or
              np.array_equal(np.rot90(State, 1), i) or
              np.array_equal(np.fliplr(np.rot90(State, 3)), i) or
              np.array_equal(np.fliplr(np.rot90(State, 1)), i)):
            return False
    return True#When for loop finished, everything has passed so it is unique


####################
#elif np.array_equal(np.fliplr(State), i):#Reflect in the vertical
#    return False
#elif np.array_equal(np.flipud(State), i):#Reflect in the horizontal
#    return False
#elif np.array_equal(np.rot90(State, 3), i):#Rotate 90 Clock
#    return False
#elif np.array_equal(np.rot90(State, 2), i):#Rotate 180
#    return False
#elif np.array_equal(np.rot90(State, 1), i):#Rotate 270 Clock (90 AntiClock)
#    return False
#elif np.array_equal(np.fliplr(np.rot90(State, 3)), i):#Reflect in TopLeft-BottomRight diagonal
#    return False
#elif np.array_equal(np.fliplr(np.rot90(State, 1)), i):#Reflect in TopRight-BottomLeft diagonal
#    return False
#####################
