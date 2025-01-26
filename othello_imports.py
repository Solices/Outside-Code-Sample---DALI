def convert_board(board):
    top_bot = ["?"]*10
    listofeight = []
    spliceind = 0
    for i in range(8):
        listofeight.append(board[spliceind:spliceind+8])
        spliceind += 8
    retstr = ""
    retstr += "".join(top_bot)
    for i in range(8):
        retstr += "?"
        retstr += listofeight[i]
        retstr += "?"
    retstr += "".join(top_bot)
    return retstr

def convert_10i_to_8i(i):
    row = i//10
    col = i%10
    return 8*row + col - 9
    
def possible_moves(board, token):
    board = convert_board(board)
    #print(board)
    directions = [-11,-10,-9,-1,1,9,10,11]
    allmoves = set()
    op = "xo"["ox".index(token)]
    for i in range(8):
        for j in range(8):
            var = i * 10 + j + 11
            if board[var] == token:
                for direction in directions:
                    mvar = var + direction
                    if board[mvar] == op:
                        while board[mvar] == op:
                            mvar += direction
                        if board[mvar] == ".":
                            allmoves.add(mvar)
    retset = set()
    for i in allmoves:
        retset.add(convert_10i_to_8i(i))
    return list(retset)

def to_eight_by_eight(board):
    retstr = ""
    for i in range(10):
        if i == 0 or i == 9:
            continue
        else:
            retstr += board[i*10 + 1:i*10 + 9]
    return retstr
def fliptoken(board, index):
    if board[index] == "x":
        board[index] = "o"
    else:
        board[index] = "x"
    return board

def make_move(board, token, index):
    #print(1)
    op = "xo"["ox".index(token)]
    board = convert_board(board)
    #print(board)
    board = list(board)

    board[10 * (index//8) + (index%8) + 11] = token
    index = 10 * (index//8) + (index%8) + 11
    directions = [-11,-10,-9,-1,1,9,10,11]
    
    for dire in directions:
        var = index + dire
        tmpset = set()
        if board[var] == op:
            while board[var] == op:
                tmpset.add(var)
                var += dire
           # print(var, token)
            if board[var] == token:
                #print(tmpset)
                for i in tmpset:
                    board = fliptoken(board, i)
    board = "".join(board)
    return to_eight_by_eight(board)
