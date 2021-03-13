import numpy as np

from readNPYorZ import readNPYorZ
from ifWin import ifWin
from ifDraw import ifDraw

print("Reading File")
ListOfGS = readNPYorZ("GameStatesWOreflecrot.npz")
GSvalue = []
for State in ListOfGS:#P1=AI
    if ifWin(State, 1):#Target to maximise, P1 winning
       GSvalue.append(1.0)
    elif ifDraw(State):#No benefit
        GSvalue.append(0.0)
    elif ifWin(State, 2):#Avoid at all cost, P2 winning
        GSvalue.append(-1.0)#The book says 0.0 for this!! but other sources say -1, the idea for 0 is that P1 can't win (so not necessarily bad in the authors perspective) from this state but we want to include punishment as reward
    else:
        GSvalue.append(0.5)#All other States start at 0.5
np.savez("StateValuesP1", GSvalue)

#Now do the same but from P2 perspective
###################################
GSvalue = []
for State in ListOfGS:#P1=AI
    if ifWin(State, 2):#Target to maximise, P2 winning
       GSvalue.append(1.0)
    elif ifDraw(State):#No benefit
        GSvalue.append(0.0)
    elif ifWin(State, 1):#Avoid at all cost, P1 winning
        GSvalue.append(-1.0)#The book says 0.0 for this!! but other sources say -1, the idea for 0 is that P1 can't win (so not necessarily bad in the authors perspective) from this state but we want to include punishment as reward
    else:
        GSvalue.append(0.5)#All other States start at 0.5
np.savez("StateValuesP2", GSvalue)
print("Done")
