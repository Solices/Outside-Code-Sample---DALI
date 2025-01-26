lis = []
sett = set()
import sys
def checkstate(state):
    board = list(state)
    winner = "null"
    for i in range(3):
        if board[i*3] == board[(i*3) + 1] == board[(i*3) + 2] and board[(i*3)] != ".":
            winner = board[i*3]
    if winner == "null":
        for j in range(3):
            if board[j] == board[3 + j] == board[6 + j] and board[j] != ".":
                winner = board[j]
    if winner == "null":
        if board[0] == board[4] == board[8] and board[0] != ".":
            winner = board[0]
    if winner == "null":
        if board[2] == board[4] == board[6] and board[2] != ".":
            winner = board[2]
    return winner
def x_recur(state, path):
    if(path == 9 or checkstate(state) == "X" or checkstate(state) == "O"):
        lis.append(state)
        sett.add(state)
    else:
        board = list(state)
        for i in range(9):
            if board[i] == ".":
                tmp = board.copy()
                tmp[i] = "X"
                tmp1 = "".join(tmp)
                o_recur(tmp1, path + 1)
def o_recur(state, path):
    if(path == 9 or checkstate(state) == "X" or checkstate(state) == "O"):
        lis.append(state)
        sett.add(state)
    else:
        board = list(state)
        for i in range(9):
            if board[i] == ".":
                tmp = board.copy()
                tmp[i] = "O"
                tmp1 = "".join(tmp)
                x_recur(tmp1, path+1)
def possible_next_boards(state, current_player):
    board = list(state)
    retlis = []
    for i in range(9):
        if board[i] == ".":
            tmp = board.copy()
            if current_player == "X":
                tmp[i] = "X"
            else:
                tmp[i] = "O"
            tmp1 = "".join(tmp)
            retlis.append(tmp1)
    return retlis
def max_step(state):
    plis = ["."]
    if checkstate(state) == "X":
        return 1
    elif checkstate(state) == "O":
        return -1
    elif all(x not in plis for x in state):
        return 0
    results = []
    for next_board in possible_next_boards(state, "X"):
        results.append(min_step(next_board))
    return max(results)
def min_step(state):
    plis = ["."]
    if checkstate(state) == "X":
        return 1
    elif checkstate(state) == "O":
        return -1
    elif all(x not in plis for x in state):
        return 0
    results = []
    for next_board in possible_next_boards(state, "O"):
        results.append(max_step(next_board))
    return min(results)
def human_move(state, x_or_o):
    board = list(state)
    ipt = int(input("Place your piece (0-8)"))
    while True:
        if board[ipt] == "O" or board[ipt] == "X":
            print("Invalid Move!!!")
            ipt = int(input("Try Again. Place your piece (0-8)"))
        else:
            board[ipt] = x_or_o
            break
    return "".join(board)
def ai_move(state, x_or_o):
    boardlist = []
    if x_or_o == "X":
        for next_board in possible_next_boards(state, x_or_o):
            boardlist.append((min_step(next_board), next_board))
    elif x_or_o == "O":
        for next_board in possible_next_boards(state, x_or_o):
            boardlist.append((max_step(next_board), next_board))
    for i in boardlist:
        if x_or_o == "X":
            if i[0] == 0:
                print("Tie", i[1])
            elif i[0] == 1:
                print("Win", i[1])
            elif i[0] == -1:
                print("Lose", i[1])
        else:
            if i[0] == 0:
                print("Tie", i[1])
            elif i[0] == 1:
                print("Lose", i[1])
            elif i[0] == -1:
                print("Win", i[1])

    if x_or_o == "X":
        for i in boardlist:
            if i[0] == 1:
                return i[1]
        for i in boardlist:
            if i[0] == 0:
                return i[1]
        return boardlist[0][1]
    if x_or_o == "O":
        for i in boardlist:
            if i[0] == -1:
                return i[1]
        for i in boardlist:
            if i[0] == 0:
                return i[1]
        return boardlist[0][1]
def display_board(board):
    board1 = list(board)     
    print(board1[0], board1[1], board1[2])
    print(board1[3], board1[4], board1[5])
    print(board1[6], board1[7], board1[8])

    
#print(max_step("........."))
#print(max_step(".OXOX...."))
#print(min_step("XO.XOX..."))
startboard = sys.argv[1]
plis = ["."]

if all(x in plis for x in startboard):
    ipt = input("Who Goes First? (Type AI or Human)")
    if ipt == "Human":
        count = 0
        while True:
            display_board(startboard)
            w = checkstate(startboard)
            if w == "X" or w == "O" or count == 9:
                print("Game End.")
                break
            else:
                startboard = human_move(startboard, "X")
                count += 1
            display_board(startboard)
            w = checkstate(startboard)
            if w == "X" or w == "O" or count == 9:
                print("Game End.")
                break
            else:
                startboard = ai_move(startboard, "O")
                count += 1
    elif ipt == "AI":
        count = 0
        while True:
            display_board(startboard)
            w = checkstate(startboard)
            if w == "X" or w == "O" or count == 9:
                print("Game End.")
                break
            else:
                startboard = ai_move(startboard, "X")
                count += 1
            display_board(startboard)
            w = checkstate(startboard)
            if w == "X" or w == "O" or count == 9:
                print("Game End.")
                break
            else:
                startboard = human_move(startboard, "O")
                count += 1
    else:
        print("Invalid entry")
else:
    lisboard = list(startboard)
    xcount = 0
    ocount = 0
    for i in lisboard:
        if i == "O":
            ocount+=1
        if i == "X":
            xcount+=1
    if ocount == xcount: #computer plays X next
        count = xcount+ocount
        #print(count)
        while True:
            display_board(startboard)
            w = checkstate(startboard)
            if w == "X" or w == "O" or count == 9:
                print("Game End.")
                break
            else:
                startboard = ai_move(startboard, "X")
                count += 1
            display_board(startboard)
            w = checkstate(startboard)
            if w == "X" or w == "O" or count == 9:
                print("Game End.")
                break
            else:
                startboard = human_move(startboard, "O")
                count += 1
    else: #computer plays O next
        count = xcount+ocount
        while True:
            display_board(startboard)
            w = checkstate(startboard)
            if w == "X" or w == "O" or count == 9:
                print("Game End.")
                break
            else:
                startboard = ai_move(startboard, "O")
                count += 1
            display_board(startboard)
            w = checkstate(startboard)
            if w == "X" or w == "O" or count == 9:
                print("Game End.")
                break
            else:
                startboard = human_move(startboard, "X")
                count += 1
'''    
x_recur(".........", 0)

print(len(lis))
print(sett)

count5=0
count7=0
count9=0
count6=0
count8=0
ties = 0
for i in sett:
    count = 0
    tmp = list(i)
    if(checkstate(i)) == "X":
        for j in tmp:
            if j == ".":
                count+=1
        if count == 4:
            count5+=1
        elif count == 2:
            count7+=1
        elif count == 0:
            count9+=1
    if checkstate((i)) == "O":
        for j in tmp:
            if j == ".":
                count+=1
        if count == 3:
            count6+=1
        elif count == 1:
            count8+=1
    if checkstate((i)) == "null":
        ties+=1
print(count5, count6, count7, count8, count9)
print(ties)
'''        
