import numpy as np

from readNPYorZ import readNPYorZ
from compareRotReflec import compareRotReflec

print("Reading File")
ListOfGS = readNPYorZ("GameStates.npz")
output = []
####
x = 0##DEBUG
###
for State in ListOfGS:
    ###
    x += 1##DEBUG
    ###
    if compareRotReflec(State, output):
        ###
        print("Safe" + str(x))##DEBUG output, this program takes a while so feedback is good
        ###
        output.append(State)
np.savez("GameStatesWOreflecrot", output)
print("Done")
