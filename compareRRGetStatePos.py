import numpy as np

#Similar to compareRotReflec but instead of true and false, we get the array index, we can then use this index to get GSvalue
def compareRRGetStatePos(State, inputGS):
    for i in range(inputGS.shape[0]):#Assume numpy array NOT LIST, NOTE .shape[0] and not .size
        if (np.array_equal(State, inputGS[i]) or
            np.array_equal(np.fliplr(State), inputGS[i]) or
            np.array_equal(np.flipud(State), inputGS[i]) or
            np.array_equal(np.rot90(State, 3), inputGS[i]) or
            np.array_equal(np.rot90(State, 2), inputGS[i]) or
            np.array_equal(np.rot90(State, 1), inputGS[i]) or
            np.array_equal(np.fliplr(np.rot90(State, 3)), inputGS[i]) or
            np.array_equal(np.fliplr(np.rot90(State, 1)), inputGS[i])):
            return i
    return None#ERRor there is a problem if it hasn't found a match
