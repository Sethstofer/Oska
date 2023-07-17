from subprocess import call
import os
from time import sleep
from copy import deepcopy
from oska import oska_play, display, movegen, listsToStrs, strsToLists

def clear():
    _ = call('clear' if os.name == 'posix' else 'cls')


def display_title():
    clear()
    print("______________________")
    print("----  ----  |  /  /--\\")
    print("|  |  |     | /   |  |")
    print("|  |  ----  |(    |--|")
    print("|  |     |  | \   |  |")
    print("----  ----  |  \  |  |")
    print("______________________")
    return


def title_screen():
    while True:
        display_title()
        print("START GAME <S>")
        print("HOW TO PLAY <H>")
        print ("QUIT <Q>")
        user_input = input("> ").lower()
        if user_input == "s":
            clear()
            break
        if user_input == "h":
            clear()
            how_to_play_screen()
            continue
        if user_input == "q":
            clear()
            exit()
        clear()
    return


def move_example():
    print("1. PIECES MOVE DIAGONALLY:")
    print("HERE, WHITE HAS MOVED THEIR PIECE")
    print("2ND FROM THE TOP TO THE AVAILABLE")
    print("RIGHTWARD SPOT\n")
    ex_board = ['w-ww','-w-','--','---','bbbb']
    display(ex_board)
    return


def capture_example():
    print("2. PIECES CAPTURE BY LEAP:")
    print("BY LEAPING OVER A WHITE PIECE IN")
    print("THE SAME DIRECTION AS IF TO MOVE,")
    print("BLACK HAS CAPTURED A WHITE PIECE\n")
    # boards used
    # ex_board_1 = ['w-w-','---','--','-w-','bb--']
    # ex_board_2 = ['w-w-','---','-b','---','b---']
    print("w - w -       w - w -")
    print(" - - -         - - - ")
    print("  - -     ->    - b  ")
    print(" - w -         - - - ")
    print("b b - -       b - - -\n")
    return


def endgame_example():
    print("3. VICTORY OR DEFEAT:")
    print("A VICTOR HAS ENSURED ONE OF THE THREE\n")
    print("-> ALL OPPONENT'S PIECES ARE CAPTURED")
    print("-> ALL PIECES HAVE REACHED OTHER SIDE")
    print("-> OPPONENT CAN NO LONGER MOVE\n")
    print("KEEP THESE IN MIND.\n")
    return


def how_to_play_screen():
    option = 0
    while True:
        if option == 0:
            move_example()
        elif option == 1:
            capture_example()
        else:
            endgame_example()
        print("CONTINUE <C>")
        print("MAIN MENU <M>")
        user_input = input("> ").lower()
        if user_input == "c":
            option = (option + 1) % 3
        if user_input == "m":
            clear()
            display_title()
            break
        clear()
    return


def display_win():
    clear()
    print("_______________________________________________")
    print("\   /  ----  |   |     |      |  -----  |\    |")
    print(" \ /   |  |  |   |     |      |    |    | \   |")
    print("  |    |  |  |   |     \      /    |    |  \  |")
    print("  |    |  |  \   /      | /\ |     |    |   \ |")
    print("  |    ----   ---       |/  \|   -----  |    \|")
    print("_______________________________________________")
    return


def display_game_over():
    clear()
    print("__________________________________________________________")
    print("----  /--\  |\  /|  ----      ----  |      |  ----  ----  ")
    print("|     |  |  | \/ |  |         |  |  \      /  |     |   \\")
    print("| --  |--|  |    |  |---      |  |   |    |   |---  |___/ ")
    print("|  |  |  |  |    |  |         |  |    \  /    |     |   \ ")
    print("----  |  |  |    |  ----      ----     \/     ----  |    \\")
    print("__________________________________________________________")
    return


def display_tie():
    clear()
    print("__________________")
    print("-----  -----  ----")
    print("  |      |    |   ")
    print("  |      |    |---")
    print("  |      |    |   ")
    print("  |    -----  ----")
    print("__________________")
    return


def game_over_screen(result):
    sleep(2.0)
    while True:
        if result == 1:
            display_win()
        elif result == 2:
            display_game_over()
        else:
            display_tie()
        print("RETURN TO MAIN MENU <R>")
        print ("QUIT <Q>")
        user_input = input("> ").lower()
        if user_input == "r":
            clear()
            break
        if user_input == "q":
            clear()
            exit()
        clear()
    return


def choose_side():
    player = ''
    opponent = ''
    while True:
        print("PLAY AS WHITE OR BLACK?")
        print ("WHITE <W>    BLACK <B>")
        user_input = input("> ").lower()
        if user_input == "w":
            player = 'w'
            opponent = 'b'
            clear()
            break
        if user_input == "b":
            player = 'b'
            opponent = 'w'
            clear()
            break
        clear()
    return player, opponent


def choice_confirmation(player, choice, board):
    list_board = strsToLists(board)
    n = len(board[0])
    temp_board = []
    # save iterators
    i = 0
    j = 0

    for i in range((int)(2 * n - 3)):
        if choice == 0:
            i -= 1
            break

        for j in range(len(board[i])):
            if board[i][j] == player:
                choice -= 1
            if choice == 0:
                temp_board = deepcopy(list_board)
                temp_board[i][j] = '!'
                break
    
    temp_board = listsToStrs(temp_board)
    while True:
        print("DID YOU MEAN THIS PIECE (!)?")
        print("YES <Y>    NO <N>")
        display(temp_board)
        user_input = input("> ").lower()
        if user_input == "y":
            clear()
            return 0, i, j
        if user_input == "n":
            clear()
            return 1, 0, 0
        clear()
        print("PLEASE CONFIRM")


def choose_move(moves):
    while True:
        for k in range(len(moves)):
            while True:
                print("POSSIBLE MOVES:")
                print("CHOICE " + str(k + 1))
                display(moves[k])

                print("ACCEPT MOVE OR NEXT?")
                print("ACCEPT <A>   NEXT <N>")
                user_input = input("> ").lower()
                if user_input == "a":
                    clear()
                    return moves[k]
                if user_input == "n":
                    clear()
                    break
                clear()


def player_move(player, board):
    # board should be displayed from prior move
    # determine how many options player has
    n = len(board[0])
    options = 0
    for i in range((int)(2 * n - 3)):
        for j in range(len(board[i])):
            if board[i][j] == player:
                options += 1

    possible_moves = movegen(board, player)
    if options > 1:
        while True:
            if possible_moves == []:
                return board

            print("PICK WHICH OF YOUR PIECES TO MOVE")
            print ("FIRST <1>    SECOND <2>...")

            try:
                user_input = int(input("> "), 10)
            except ValueError:
                clear()
                display(board)
                continue

            if (user_input <= options) and (user_input > 0):
                clear()
                ret, i, j = choice_confirmation(player, user_input, board)
                # if you want to go back, restart loop
                if ret == 1:
                    display(board)
                    continue
                moves = [x for x in possible_moves if x[i][j] == '-']
                if moves == []:
                    print("NO MOVES AVAILABLE FOR THAT PIECE")
                    display(board)
                    continue
                return choose_move(moves)
            clear()
            display(board)
    else:
        clear()
        if possible_moves == []:
            return board
        return choose_move(possible_moves)


def play_oska():
    title_screen()
    player, opponent = choose_side()
    difficulty = 5  # static depth search
    ret = 0

    start_board = ['wwww','---','--','---','bbbb']
    display(start_board)

    board = start_board
    white_move = []
    black_move = []

    # determine game flow by who goes first
    if player == 'w':
        while True:
            # white goes
            white_move = player_move(player, board)
            # check for cannot move; black wins
            if white_move == board:
                ret = 2
                break
            #
            clear()
            ret = display(white_move)
            board = white_move
            if ret != 0:
                break

            # black goes
            sleep(1.0)
            black_move = oska_play(board, opponent, difficulty)
            # check for cannot move; white wins
            if black_move == board:
                ret = 1
                break
            #
            clear()
            ret = display(black_move)
            board = black_move
            if ret != 0:
                break

    else:
        while True:
        # white goes
            sleep(1.0)
            white_move = oska_play(board, opponent, difficulty)
            # check for cannot move; black wins
            if white_move == board:
                ret = 2
                break
            #
            clear()
            ret = display(white_move)
            board = white_move
            if ret != 0:
                break

            # black goes
            black_move = player_move(player, board)
            # check for cannot move; white wins
            if black_move == board:
                ret = 1
                break
            #
            clear()
            ret = display(black_move)
            board = black_move
            if ret != 0:
                break

    # game finished
    result = 1
    if ((ret == 1) and (player == 'b')) or ((ret == 2) and (player == 'w')):
        result = 2
    if (ret == 3):
        result = 3
    
    game_over_screen(result)
    title_screen()
    play_oska()


if __name__ == "__main__":
    play_oska()