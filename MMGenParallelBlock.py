import numpy as np
import itertools
from joblib import Parallel, delayed
import multiprocessing

def FromParallelModule_ParallelValidGameStateSearch(combo, ListOfNodesGT):#Literally the same except this is parallelisable
    comboState = np.array(combo)
    comboState = np.reshape(comboState, (3,3))#Turn numpy array into 3x3grid
    for node in ListOfNodesGT:#Reading collisions shouldn't be an issue
        if np.array_equal(comboState, node):#So compare a unique combination with legal states to get legal and unique combinations
            return comboState
