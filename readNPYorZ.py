import numpy as np

def readNPYorZ(filepath):
    with np.load(filepath) as data:
        return data["arr_0"]
    
if __name__ == '__main__':#Test to see if working as intended
    #print(readNPYorZ("GameTree.npz").shape)
    #print(readNPYorZ("GameTree.npz")[0:10])
    #print(readNPYorZ("GameStatesWOreflecrot.npz").size)#VERY IMPORTANT NOTE, THIS IS WRONG, USE .shape[0] for actual length
    print(readNPYorZ("GameStatesWOreflecrot.npz").shape)
    print(readNPYorZ("GameStatesWOreflecrot.npz")[0:10])
    #print(readNPYorZ("StateValuesP1.npz")[600:])
