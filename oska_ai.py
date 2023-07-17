from copy import deepcopy
from random import choice
import sys


"""
oskaplayer(board, player, limit)
[Explanation:]
Using a form of minimax algorithm, takes a `board`, the MAX `player`, and the
depth (`limit`) of search allowed and outputs best move available to the player
[returns:]
A list of strings representing next move to make
"""
def oska_play(board, player, limit):
    # uses minimax to search for best option for given player
    # *with the assumption opponent will always choose the best move available*
    # recursive minimax algorithm
    if player == 'w':
        nextmove = max(board, player, limit)[0]
    else:
        nextmove = min(board, player, limit)[0]
    # return next best move (the board part of the returned pair (board, value))
    return nextmove


"""
display(board)
[Explanation:]
Displays the `board` in an intuitive manner
[returns:]
A string representing the board
"""
def display(board):
    display = ''
    buffer = ''
    n = len(board[0])
    halfway = (int)((2 * n - 3) / 2)

    for i in range((int)(2 * n - 3)):
        display = display + buffer
        for j in range(len(board[i])):
            display = display + board[i][j] + ' '
        display = display + '\n'
        if i < halfway:
            buffer = buffer + ' '
        else:
            buffer = (len(buffer) - 1) * ' '
    
    print(display)
    curr_state = eval(board)
    if (curr_state == sys.maxsize):
        print("WHITE WINS")
        return 1
    if (curr_state == -sys.maxsize):
        print("BLACK WINS")
        return 2
    if (curr_state == 3.14):
        # tie
        return 3
    return 0


"""
max(board, player, limit)
[Explanation:]
Max function of the minimax algorithm; generates moves from a board,
evaluates it if it's a leaf node or a winning move, and then returns
a pair of the board and its value that was the most among them
[returns:]
A list comprised of the board (list of strings) of the best move and
its evaluation value
"""
def max(board, player, limit):
    if player == 'w':
        opponent = 'b'
    else:
        opponent = 'w'
    # placeholder w/ overwrittable eval num
    # NOTICE it will keep track of the move board in bestoption[0]
    bestoption = [['placeholder'], -sys.maxsize]
    option = [board, -sys.maxsize]
    moves = movegen(board, player)
    moves = jumble(moves)
    # go through each move, calling min if not a leaf node
    for elem in moves:
        result = eval(elem)
        # stop at limit == 1 for limit levels of branching
        # if find win for MAX or reach limit, propogate up; ignore loss moves
        if result == sys.maxsize:
            bestoption = [elem, result]
            break
        if (result == -sys.maxsize) or (limit == 1):
            option = [elem, result]
        # otherwise, continue downward to propogate up later
        else:
            option = [elem, (min(elem, opponent, limit - 1))[1]]
        # choose the maximum value amongst all generated moves' values
        # NOTICE that this will only run once MINIMAX has (likely recursively)
        # returned to this point after getting to a leaf node
        if option[1] > bestoption[1]:
            bestoption = option
    # bestoption is always a real option
    if bestoption[0] == ['placeholder']:
        bestoption = option
    return bestoption


"""
min(board, opponent, limit)
[Explanation:]
Min function of the minimax algorithm; generates moves from a board,
evaluates it if it's a leaf node or a winning move, and then returns
a pair of the board and its value that was the least among them
[returns:]
A list comprised of the board (list of strings) of the best move and
its evaluation value
"""
def min(board, opponent, limit):
    if opponent == 'w':
        player = 'b'
    else:
        player = 'w'
    # placeholder w/ overwrittable eval num
    # NOTICE it will keep track of the move board in bestoption[0]
    bestoption = [['placeholder'], sys.maxsize]
    option = [board, sys.maxsize]
    moves = movegen(board, opponent)
    moves = jumble(moves)
    # go through each move, calling max if not a leaf node
    for elem in moves:
        result = eval(elem)
        # stop at limit == 1 for limit levels of branching
        # if find win for MIN or reach limit, propogate up; ignore loss moves
        if result == -sys.maxsize:
            bestoption = [elem, result]
            break
        if (result == sys.maxsize) or (limit == 1):
            option = [elem, result]
        else:
            option = [elem, (max(elem, player, limit - 1))[1]]
        # choose the minimum value amongst all generated moves' values
        # NOTICE that this will only run once MINIMAX has (likely recursively)
        # returned to this point after getting to a leaf node
        if option[1] < bestoption[1]:
            bestoption = option
    # bestoption is always a real option
    if bestoption[0] == ['placeholder']:
        bestoption = option
    return bestoption


"""
eval(board)
[Explanation:]
Evaluates given board based on rules of game & decided heuristics
[returns:]
Integer value representing evaluation of board
"""
def eval(board):
    wleft = 0
    bleft = 0
    value = 0

    n = len(board[0])
    maxNdx = len(board) - 1
    midNdx = (int)((2 * n - 3) / 2)

    wPassedMid = False
    bPassedMid = True

    # `i` is top to bottom location of piece; row
    # `j` is left to right location of piece; spot in row
    for i in range(len(board)):
        for j in range(len(board[i])):
            # player's pieces on their first row favors opponent
            # player's pieces on their opponent's first row favors player
            # NOTICE this heuristic instigates forward movement of pieces
            # results in any piece in top row meaning -1 and +1 for bottom row
            #
            # pts are added/subtracted dependent on how close each piece is
            # to the opp side
            if i == 0 and board[i][j].isalpha():
                value = value - 1
            if i == maxNdx and board[i][j].isalpha():
                value = value + 1
            # count number of each player's pieces
            if board[i][j] == 'w':
                wleft = wleft + 1
                value = value + i
                # if first white piece found is passed mid, all are passed mid
                if wleft == 1 and i > midNdx:
                    wPassedMid = True
            if board[i][j] == 'b':
                bleft = bleft + 1
                value = value + (i - maxNdx)
                # if last black piece found is before mid, all are before mid
                if i >= midNdx:
                    bPassedMid = False
                else:
                    bPassedMid = True
    
    # win states are defined by maximum and minimum integers possible
    # check for total capture win
    if wleft == 0:
        return -sys.maxsize
    if bleft == 0:
        return sys.maxsize
    
    # check for all pieces at end win
    w_end = 0
    b_end = 0
    for j in range(n):
        if board[0][j] == 'b':
            b_end = b_end + 1
        if board[maxNdx][j] == 'w':
            w_end = w_end + 1
    if bleft == b_end and wleft == w_end:
        # final move causes both parties to be at end of board
        if bleft > wleft:
            return -sys.maxsize
        elif wleft > bleft:
            return sys.maxsize
        else:
            # tie; only possible fraction return
            return 3.14
    if bleft == b_end:
        return -sys.maxsize
    if wleft == w_end:
        return sys.maxsize
    
    # advantageous for a player to be passed mid w/ less pieces than opponent
    if wPassedMid == True and bPassedMid == True:
        value = value + (bleft - wleft)
    elif wPassedMid == True:
        value = value + bleft
    elif bPassedMid == True:
        value = value - wleft
    
    return value + (wleft - bleft)


"""
movegen(str_board, next_player)
[Explanation:]
Generates possible moves (slides and captures) for the given next player
with the given current board
[returns:]
A list of lists of strings
"""
def movegen(str_board, next_player):
    n = len(str_board[0])
    boardLen = (int)(2 * n - 3)
    halfway = (int)((2 * n - 3) / 2)
    generated = []

    if next_player == 'w':
        otherplayer = 'b'
        board = strsToLists(str_board)
    else:
        otherplayer = 'w'
        board = strsToLists(reverse(str_board))
    
    ### main computations
    # i := row
    # j := spot in row
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == next_player:
                ### SLIDES
                # above halfway
                if i < halfway:
                    # check for right move
                    if (j < len(board[i]) - 1) and (board[i+1][j] == '-'):
                        curr_board = deepcopy(board)
                        curr_board[i][j] = '-'
                        curr_board[i+1][j] = next_player
                        generated = generated + [curr_board]
                    # check for left move
                    if (j > 0) and (board[i+1][j-1] == '-'):
                        curr_board = deepcopy(board)
                        curr_board[i][j] = '-'
                        curr_board[i+1][j-1] = next_player
                        generated = generated + [curr_board]
                # below halfway
                else:
                    if i + 1 < boardLen:
                        # check for right move
                        if board[i+1][j+1] == '-':
                            curr_board = deepcopy(board)
                            curr_board[i][j] = '-'
                            curr_board[i+1][j+1] = next_player
                            generated = generated + [curr_board]
                        # check for left move
                        if board[i+1][j] == '-':
                            curr_board = deepcopy(board)
                            curr_board[i][j] = '-'
                            curr_board[i+1][j] = next_player
                            generated = generated + [curr_board]
                        
                ### CAPTURES
                # above halfway
                if i < halfway - 1:
                    # check for right capture
                    if (j < len(board[i]) - 2) and (board[i+1][j] == otherplayer):
                        if board[i+2][j] == '-':
                            curr_board = deepcopy(board)
                            curr_board[i][j] = '-'
                            curr_board[i+1][j] = '-'
                            curr_board[i+2][j] = next_player
                            generated = generated + [curr_board]
                    # check for left capture
                    if (j - 2 >= 0) and (board[i+1][j-1] == otherplayer):
                        if board[i+2][j-2] == '-':
                            curr_board = deepcopy(board)
                            curr_board[i][j] = '-'
                            curr_board[i+1][j-1] = '-'
                            curr_board[i+2][j-2] = next_player
                            generated = generated + [curr_board]
                # midsection
                elif i == halfway - 1:
                    # check for right capture
                    if (j < 2) and (board[i+1][j] == otherplayer):
                        if board[i+2][j+1] == '-':
                            curr_board = deepcopy(board)
                            curr_board[i][j] = '-'
                            curr_board[i+1][j] = '-'
                            curr_board[i+2][j+1] = next_player
                            generated = generated + [curr_board]
                    # check for left capture
                    if (j > 0) and (board[i+1][j-1] == otherplayer):
                        if board[i+2][j-1] == '-':
                            curr_board = deepcopy(board)
                            curr_board[i][j] = '-'
                            curr_board[i+1][j-1] = '-'
                            curr_board[i+2][j-1] = next_player
                            generated = generated + [curr_board]
                # below halfway
                else:
                    if i + 2 < boardLen:
                        # check for right capture
                        if board[i+1][j+1] == otherplayer:
                            if board[i+2][j+2] == '-':
                                curr_board = deepcopy(board)
                                curr_board[i][j] = '-'
                                curr_board[i+1][j+1] = '-'
                                curr_board[i+2][j+2] = next_player
                                generated = generated + [curr_board]
                        # check for left capture
                        if board[i+1][j] == otherplayer:
                            if board[i+2][j] == '-':
                                curr_board = deepcopy(board)
                                curr_board[i][j] = '-'
                                curr_board[i+1][j] = '-'
                                curr_board[i+2][j] = next_player
                                generated = generated + [curr_board]
    # turn generated lists of lists back into lists of strings
    temp = []
    for elem in generated:
        temp = temp + [listsToStrs(elem)]
    generated = temp
    # flip the generated boards back to proper orientation if playing black
    if otherplayer == 'w':
        generated = []
        for each in temp:
            generated = generated + [reverse(each)]
    return generated


"""
jumble(moves)
[Explanation:]
Takes moves and places them in arbitrary locations in list to give equal
evals a chance to be picked
[returns:]
A list representing possible moves
"""
def jumble(moves):
    moves_left = deepcopy(moves)
    jumbled_moves = []

    while moves_left != []:
        move = choice(moves_left)
        jumbled_moves = jumbled_moves + [move]
        moves_left = [x for x in moves_left if x != move]
    
    return jumbled_moves


"""
strsToLists(board)
[Explanation:]
Takes original board representation and changes it to a list of lists
[returns:]
List of lists
"""
def strsToLists(board):
    listboard = []
    for elem in board:
        listboard = listboard + [list(elem)]
    return listboard


"""
listsToStrs(listboard)
[Explanation:]
Takes lists of lists representation and changes it back to
original string representation
[returns:]
List of strings
"""
def listsToStrs(listboard):
    board = []
    for elem in listboard:
        string = ''
        for each in elem:
            string = string + each
        board = board + [string]
    return board


"""
reverse(st)
[Explanation:]
Simple function that reverses the items in something
[returns:]
The reverse of what was passed
"""
def reverse(st):
  return st[::-1]