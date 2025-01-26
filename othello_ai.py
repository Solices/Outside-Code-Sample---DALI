import sys
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

def score_move(board, token):
    op = "xo"["ox".index(token)]
    score = 0
    w1 = possible_moves(board, token)
    w2 = possible_moves(board, op)
    if len(w1) == 0 and len(w2) == 0:
        score += (board.count("x") - board.count("o"))
        if score > 0:
            score += 10000000
        elif score < 0:
            score -= 10000000
    else:
        score += (len(w1) - len(w2))
    board = list(board)
    if board[0] == "x":
        score += 10000
    elif board[0] == "o":
        score -= 10000
    if board[7] == "x":
        score += 10000
    elif board[7] == "o":
        score -= 10000
    if board[56] == "x":
        score += 10000
    elif board[56] == "o":
        score -= 10000
    if board[63] == "x":
        score += 10000
    elif board[63] == "o":
        score -= 10000
    
    if board[1] == "x":
        score -= 1000
    elif board[1] == "o":
        score += 1000
    if board[8] == "x":
        score -= 1000
    elif board[8] == "o":
        score += 1000
    if board[9] == "x":
        score -= 1000
    elif board[9] == "o":
        score += 1000


    if board[6] == "x":
        score -= 1000
    elif board[6] == "o":
        score += 1000
    if board[14] == "x":
        score -= 1000
    elif board[14] == "o":
        score += 1000
    if board[15] == "x":
        score -= 1000
    elif board[15] == "o":
        score += 1000


    if board[48] == "x":
        score -= 1000
    elif board[48] == "o":
        score += 1000
    if board[49] == "x":
        score -= 1000
    elif board[49] == "o":
        score += 1000
    if board[57] == "x":
        score -= 1000
    elif board[57] == "o":
        score += 1000


    if board[54] == "x":
        score -= 1000
    elif board[54] == "o":
        score += 1000
    if board[55] == "x":
        score -= 1000
    elif board[55] == "o":
        score += 1000
    if board[62] == "x":
        score -= 1000
    elif board[62] == "o":
        score += 1000
    return score

def max_step(board, player, depth):
    op = "xo"["ox".index(player)]
    if depth == 0 or (len((w := (possible_moves(board, player)))) == 0 and len(possible_moves(board, op)) == 0):
        return score_move(board, player)
    elif len(w) == 0:
        return min_step(board, op, depth-1)
    results = []
    for move in w:
        new_board = make_move(board, player, move)
        results.append(min_step(new_board, op, depth-1))
    return max(results)

def min_step(board, player, depth):
    op = "xo"["ox".index(player)]
    if depth == 0 or (len((w := (possible_moves(board, player)))) == 0 and len(possible_moves(board, op)) == 0):
        return score_move(board, player)
    elif len(w) == 0:
        return max_step(board, op, depth-1)
    results = []
    for move in w:
        new_board = make_move(board, player, move)
        results.append(max_step(new_board, op, depth-1))
    return min(results)



def find_next_move(board, player, depth):
    op = "xo"["ox".index(player)]
    all_moves_values_with_moves = []
    for move in possible_moves(board, player):
        new_board = make_move(board, player, move)
        if player == "x":
            all_moves_values_with_moves.append((move, min_step(new_board, op, depth-1)))
        else:
            all_moves_values_with_moves.append((move, max_step(new_board, op, depth-1)))
    bestmove = all_moves_values_with_moves[0][1]
    if player == "x":
        bestmove = max(all_moves_values_with_moves,key=lambda item:item[1])[0]
    else:
        bestmove = min(all_moves_values_with_moves,key=lambda item:item[1])[0] 
    return bestmove


board = sys.argv[1]

player = sys.argv[2]

depth = 1

for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
    print(find_next_move(board, player, depth))

    depth += 1
