import numpy as np
import itertools
from joblib import Parallel, delayed
import multiprocessing

from MMGenParallelBlock import FromParallelModule_ParallelValidGameStateSearch
from readNPYorZ import readNPYorZ

print("Reading File")
ListOfNodes = readNPYorZ("GameTree.npz")
print("Start")
ListOfGameStates = Parallel(n_jobs=-1, prefer="threads", verbose=11)(delayed(FromParallelModule_ParallelValidGameStateSearch)(combo, ListOfNodes) for combo in itertools.product((0,1,2), repeat=9))#Imported
print("Saving to file")
np.savez("GameStates", ListOfGameStates)
print("Done")
