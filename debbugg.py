import math
import random
import copy
import tictactoe as ttt

X = "X"
O = "O"
EMPTY = None

U = [[EMPTY,  X, EMPTY],[  O,    O,     X],[X, EMPTY, EMPTY]]
action = ttt.minimax(U)
print(action)