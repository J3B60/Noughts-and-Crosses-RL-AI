# Noughts and Crosses with AI (Tic-Tac-Toe)
## How To Run
Requires PyQt5 ver 5.13.0, numpy ver 1.17.2, joblib ver 0.14.1 and spyder ver 3.3.6. These can be installed by running "pip install -r requirements.txt".

To run the Tic-Tac-Toe Game, run Tic-Tac-Toe-GUI2.py for the GUI version or Tic-Tac-Toe.py for console. Once the game is run, the player has the option to choose the settings whether to play Human Vs Human, AI Vs Human or Human Vs AI and the option to change the Learning Rate and Epsilon values of the AI.

## Game Tree Generation for Reinforcement Learning AI

GameTreeGen.py, UniqueGameStateGen.py, UniqueGSwRotReflecGen.py, GSvalueGen.py

In brief, GameTreeGen.py generates all legal game states for Tic-Tac-Toe (aka. Game tree) using the recursive MinimaxGen(), then it outputs the list of game states to the file “GameTree.npz”. The next focus is to remove all the duplicate game states.

UniqueGameStateGen.py generates a set of all board symbol combinations O(3\^9) (including illeagal board states) which is generated using the itertools library. When comparing the game tree and the symbol combinations it takes O(3\^9x9!), speeding up the process by x18.5 compared to checking the game tree against itself O(9!\^2). 

This program takes the intersection of the game tree set and symbol combination set to output the set of unique legal game states to a file called “GameStates.npz”. This program runs MMGenParallelBlock.py in parallel using the Joblib library, this is to reduce execution time. The files generated were done on a personal home server which completed the program in 10 hours using 8 logic processors at 4.0GHz hence necessary use of parallel programming to increase speed.

UniqueGSwRotReflecGen.py reduces the game state set to an even smaller 765 by removing all duplicate boards that are symmetrical or rotations of each other, using the compareRotReflec.py function. The output is saved to the file “gameStatesWOreflectrot.npz”
GSvalueGen.py generates the game state values for the learning. Wins =1, Lose = -1, Draw = 0 and all other boards begin with 0.5 [3]. Each game state value corresponds to the game state in the unique game state file.
