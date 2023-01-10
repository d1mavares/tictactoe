"""
Tic Tac Toe Player
"""
import math
import random
import copy

X = "X"
O = "O"
EMPTY = None
NotB = "NB" # Not to Play: mark the cell to tell minmax not to play here at the first move

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # board as a 1D list
    boardFlat = [j for sub in board for j in sub]
    
    # If the board isn't full
    if boardFlat.count(EMPTY) > 0:
        # If the board is empty
        if boardFlat.count(EMPTY) == 9:
            return X
        if boardFlat.count(O) < boardFlat.count(X):
            return O
        else: 
            return X
    else:
        return None
    #raise NotImplementedError

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    boardFlat = [j for sub in board for j in sub]
    Actions = set()
    act = [i for i, val in enumerate(boardFlat) if val == None]
    for i in act:
        Actions.add((i//3,i%3))
    return Actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    action is a list = [(coordinates,player)]. eg: [(0,1),'X']
    """
    try:
        # if action is an integer, there is not an specified player (i.e first move)
        if type(action[0]) == int:
            move = action
            playr = player(board)
        #action == None means the game is over, so do nothing
        elif action[0] is None:
            return board
        else:
            move = action[0]
            playr = action[1]
        if (move[0]<0) or (move[0]>2) or (move[1]<0) or (move[1]>2):
            raise InvalidMoveException
        else:
            board[move[0]][move[1]] = playr 
            return board
    except InvalidMoveException:
        print("Exception occurred: Invalid Move")

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    boardFlat = [j for sub in board for j in sub]
    Actions = set()
    act = [i for i, val in enumerate(boardFlat) if val == None]
    for i in act:
        Actions.add((i//3,i%3))
    return Actions

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if utility(board) == 1:
        return 'X'
    elif utility(board) == -1:
        return 'O'
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    boardFlat = [j for sub in board for j in sub]
    A = boardFlat.count(None)
    if (A == 0):
        return True
    if bool(checklines(board,3)):
        return True
    if bool(checklines(board,-3)):
        return True
    return False
#    return bool(sum(x.count('None') for x in board) == 0)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if (3 in countmarks(board)[0]):
        return 1
    elif (-3 in countmarks(board)[0]):
        return -1
    else:
        return 0

def checklines(board,val):
    X0 = countmarks(board)
    #print(f"marks: {X0[0]}")
    lines2check = X0[1]
    checkline = X0[0]
   
    if val in checkline:
        ind3 = checkline.index(val)
        j = lines2check[ind3]
        out = []
        for ind in j:
            out.append((ind//3,ind%3))
        return out   
    return None

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # board as a 1D list
    boardFlat = [j for sub in board for j in sub]

    # If the game is over, no need to lookfor anything
    if terminal(board):
        return None
#    # If there is only one play, always play at the one corner
#    if boardFlat.count(EMPTY) == 8:
#        possibleactions = actions(board)
#        recommactions = {(1,1),(0,0),(0,2),(2,0),(2,2)}
#        for act1 in possibleactions:
#            for act2 in recommactions:
#                if act1 == act2:
#                    return act1
    #If AI makes the first move, always play at the center
    if boardFlat.count(EMPTY) == 9:
        return (1,1)
    #If there is one single empty cell, there is no need to lookfor anything
    if boardFlat.count(EMPTY) == 1:
        ind = boardFlat.index(EMPTY)
        return (ind//3,ind%3)

    # minmax search
    while not terminal(board):
        P = player(board)
        possibleactions = actions(board)
        sgn = 1 if P == X else -1
        recommactions = checklines(board,2*sgn)
        if recommactions is not None:
            for act1 in possibleactions:
                for act2 in recommactions:
                    if act1 == act2:
                        return act1
            return possibleactions.pop()
        else:
            recommactions = checklines(board,-2*sgn)
            if recommactions is not None:
                for act1 in possibleactions:
                    for act2 in recommactions:
                        if act1 == act2:
                            return act1
                return possibleactions.pop()
            else:
                recommactions = checklines(board,sgn)
                if recommactions is not None:
                    for act1 in possibleactions:
                        for act2 in recommactions:
                            if act1 == act2:
                                return act1
                    return possibleactions.pop()
                else:
                    recommactions = checklines(board,-1*sgn)
                    if recommactions is not None:
                        for act1 in possibleactions:
                            for act2 in recommactions:
                                if act1 == act2:
                                    return act1
                        return possibleactions.pop()
    return None
    
def countmarks(board):
    # Counts the number of Xs and Os in the board

    # board as a 1D list
    boardFlat = [j for sub in board for j in sub]
    
    # list of coordinates to check (lines)
    LinesCoord = []
    LinesCoord.append((0,1,2))
    LinesCoord.append((3,4,5))
    LinesCoord.append((6,7,8))
    LinesCoord.append((0,3,6))
    LinesCoord.append((1,4,7))
    LinesCoord.append((2,5,8))
    LinesCoord.append((0,4,8))
    LinesCoord.append((2,4,6))
    # LinesCoord=[(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

    # lines contains the number of Xs or Os per line in LinesCoord
    # e.g. lines = [0, 0, 2, 1, 0, 1, 1, -1]
    #                        |                       
    ################## one more X than O in the first vertical line
    lines = []
    for item in LinesCoord:
        lines.append([boardFlat[i] for i in item].count(X)-[boardFlat[i] for i in item].count(O))
    return [lines,LinesCoord]

class InvalidMoveException(Exception):
    "Raised when the input value is not a valid move at the tictactoe game"
    pass

board = initial_state() #Original board
while not terminal(board): #while game isn't over
    P = player(board)
    counter = 0
    action = None
    # If the game is starting, always play at the center
    boardFlat = [j for sub in board for j in sub] #Flattening the board to count marks
    if boardFlat.count(EMPTY) == 9:
        action = (1,1)
    Newboard = copy.deepcopy(board) #base board to explore search tree
    while action is None: #action is None while minmax is still looking for a move (computer thinking)
        if counter == 0:#For the first move, we create another board
            Newitboard = copy.deepcopy(Newboard) #board used to explore each branch of the tree
        else: #If not the beginning of the branch, we should remove NotB from Newitboard
            #Remove NotB from Newitboard
            NewitboardFlat = [j for sub in Newitboard for j in sub]# Make board an 1D list
            if NotB in NewitboardFlat:
                i = NewitboardFlat.index(NotB)
                NewitboardFlat[i] = EMPTY #Remove NotB mark
                Newitboard = [[None for i in range(3)] for i in range(3)]#Make board a 2D list again
                for i in range(3):
                    Newitboard[i] = NewitboardFlat[3*i:3*i+3]

        if terminal(Newitboard):#if this action ends the game and P winned, this is the right action and the cycle ends
            W = winner(Newitboard)
            if W == P:
                action = candaction
            elif W is None:#if P doesn't win, but the result is a tie, we take it as a tentative action. We should continue checking for a winner action
                tempaction = candaction
                counter = 0
            else: #If P loses, end of the branch
                counter = 0

        else:
            NewP = player(Newitboard) #player looking ahead
            candaction = minimax(Newitboard) #possible action
            Newitboard = result(Newitboard,(candaction,NewP))

            if counter == 0:#if this candaction doesn't end the game and it is the root of the tree, we check the cell with NotB, for the minmax function doesn't play there
                Newboard = result(Newboard,(candaction,NotB))

            counter += 1# Number of plays while looking for moves using minmax
      
        #Newitboard = result(Newboard,(candaction,NewP)) #if it isn't the first move, we uncheck the cell, for the minmax function could play there  
        #Newboard = result(Newboard,(action,P))
#    action = minimax(board)
    board = result(board,(action,P))
winplayer = winner(board)
