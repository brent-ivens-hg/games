import re


# ------------------------------------------------------ start ------------------------------------------------------ #


def tic_tac_toe():
    board = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
    indices = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    player = 1
    symbol = " "
    player1_score = 0
    player2_score = 0
    ins = input(format_list(board) + "Where do you want to place, player " + str(player) + "? [1-9] ").lower()
    # PLACING "X" FOR PLAYER 1 AND "O" FOR PLAYER 2
    while True:  # Runs until stopped to allow rematches
        while True:  # Runs for a single round
            if ins == "stop":
                print("\nGame was stopped.")
                break
            elif ins in indices:  # Number must be between 1 and 9
                if player == 1:
                    symbol = "X"
                else:
                    symbol = "O"
                if board[int(ins) - 1] == "_":
                    board[int(ins) - 1] = symbol
                    player = 3 - player  # Switches players after turn if placement is available
                else:
                    print("ERROR: Place already taken.")
            else:
                print("ERROR: Placement must be a number between 1 and 9.")
            if board.count("_") == 0:
                print(format_list(board) + "Stalemate.")
                break
            elif is_finished(board, symbol):
                player = 3 - player  # Previous player/turn won the round so player gets reversed
                print(format_list(board) + "Round finished. Player " + str(player) + " won!")
                if player == 1:
                    player1_score += 1
                else:
                    player2_score += 1
                break
            else:
                ins = input(
                    format_list(board) + "Where do you want to place, player " + str(player) + "? [1-9] ").lower()
        if ins == "stop":
            break
        else:
            print("Score: {}-{}.".format(player1_score, player2_score))
            ins = input("Rematch? (y/n) ").lower()
            while ins != "stop":
                if ins in "yes":
                    board = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
                    ins = input(
                        format_list(board) + "Where do you want to place, player " + str(player) + "? [1-9] ").lower()
                elif ins in "no":
                    ins = "stop"
                else:
                    ins = input("Rematch? (y/n) ").lower()


def format_list(input_list):
    string = ""
    for i, item in enumerate(input_list):
        if (i + 1) % 3 == 0:
            string += item + "\n"
        else:
            string += item + "  "
    string += "\n"
    return string


def is_finished(board, symbol):
    board = "".join(board).replace(symbol, "#")
    finished = True
    # regular expressions
    if re.match("^###......$", board) or re.match("^...###...$", board) or re.match("^......###$", board):
        print("[Horizontal match for '" + symbol + "']")
    elif re.match("^#..#..#..$", board) or re.match("^.#..#..#.$", board) or re.match("^..#..#..S$", board):
        print("[Vertical match for '" + symbol + "']")
    elif re.match("^#...#...S$", board) or re.match("^..#.#.#..$", board):
        print("[Diagonal match for '" + symbol + "']")
    else:
        print("[No matches for '" + symbol + "']")
        finished = False
    return finished


tic_tac_toe()


# ------------------------------------------------------- end ------------------------------------------------------- #


def test_finished_board():
    # TEST BOARDS
    boards = [
        ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
        ['X', 'X', 'X', '_', 'O', '_', 'O', '_', '_'],
        ['_', '_', 'O', 'X', 'X', 'X', 'O', '_', '_'],
        ['_', '_', 'O', '_', 'O', '_', 'X', 'X', 'X'],
        ['X', '_', 'O', 'X', 'O', '_', 'X', '_', '_'],
        ['_', 'X', 'O', '_', 'X', '_', 'O', 'X', '_'],
        ['_', '_', 'X', '_', 'O', 'X', 'O', '_', 'X'],
        ['X', '_', 'O', '_', 'X', '_', 'O', '_', 'X'],
        ['O', '_', 'X', '_', 'X', '_', 'X', '_', 'O']
    ]
    for board in boards:
        is_finished(board, "X")
        is_finished(board, "O")
