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
output = []
for State in ListOfGameStates:#Something like this, instead of running this in this file, I just ran this in the python terminal, saves me from having to re-run this whole program since after running Python doesn't restart the terminal, so even though the output was bad, I could still access the ListOfGameStates in memory and fix my output
    if type(State) == np.ndarray:
        output.append(State)
np.savez("GameStates", output)
print("Done")
