import sys
cornerlis = [0, 7, 56, 63]
diagadj = [9, 14, 49, 54]
acrossadj = [1,8,6, 12,15,48, 57,55,62]
edges =[2,3,4,5, 61,60,59,58, 16,24,32,40 ,47,39,31,23]
before_edges = [10,11,12,13, 17,25,33,41, 50,51,52,53, 22,30,38,46]
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
        return score
    else:
        score += 15*(len(w1) - len(w2))
    if len(w1) == 0:
        if op == "o":
            score -= 750
        else:
            score += 750
    elif len(w2) == 0:
        if op == "o":
            score += 750
        else:
            score -= 750
    board = list(board)


    for i in cornerlis:
        if board[i] == "x":
            score += 1500
        elif board[i] == "o":
            score -= 1500
    for i in diagadj:
        if board[i] == "x":
            score -= 150
        elif board[i] == "o":
            score += 150
    for i in acrossadj:
        if board[i] == "x":
            score -= 120
        elif board[i] == "o":
            score += 120
    for i in edges:
        if board[i] == "x":
            score += 15
        elif board[i] == "o":
            score -= 15
    '''
    for i in before_edges:
        if board[i] == "x":
            score -= 2
        elif board[i] == "o":
            score += 2
    '''
    return score

def max_step(board, player, depth, alpha, beta):
    op = "xo"["ox".index(player)]
    if depth == 0 or (len((w := (possible_moves(board, player)))) == 0 and len(possible_moves(board, op)) == 0):
        return score_move(board, player)
    elif len(w) == 0:
        return min_step(board, op, depth-1, alpha, beta)
    results = []
    for move in w:
        new_board = make_move(board, player, move)
        results.append(w1:=min_step(new_board, op, depth-1, alpha, beta))
        alpha = max(w1, alpha) #ALPHA BETA HERE
        if alpha >= beta: 
            break
    return max(results)

def min_step(board, player, depth, alpha, beta):
    op = "xo"["ox".index(player)]
    if depth == 0 or (len((w := (possible_moves(board, player)))) == 0 and len(possible_moves(board, op)) == 0):
        return score_move(board, player)
    elif len(w) == 0:
        return max_step(board, op, depth-1, alpha, beta)
    results = []
    for move in w:
        new_board = make_move(board, player, move)
        results.append(w1:=max_step(new_board, op, depth-1, alpha, beta))
        beta = min(beta, w1)  #ALPHA BETA HERE
        if alpha >= beta:
            break
    return min(results)

def find_next_move(board, player, depth):
    alpha = -99999999999999999
    beta = 99999999999999999
    op = "xo"["ox".index(player)]
    all_moves_values_with_moves = []
    for move in possible_moves(board, player):
        new_board = make_move(board, player, move)
        if player == "x":
            all_moves_values_with_moves.append((move, w1:=min_step(new_board, op, depth-1, alpha, beta)))
            #ALPHA BETA HERE
            alpha = max(w1, alpha)
            if alpha >= beta:
                break
        else:
            all_moves_values_with_moves.append((move, w1:=max_step(new_board, op, depth-1, alpha, beta)))
            beta = min(beta, w1)
            #ALPHA BETA HERE
            if alpha >= beta:
                break
    bestmove = all_moves_values_with_moves[0][1]
    if player == "x":
        bestmove = max(all_moves_values_with_moves,key=lambda item:item[1])[0]
    else:
        bestmove = min(all_moves_values_with_moves,key=lambda item:item[1])[0] 
    return bestmove


board = sys.argv[1]
player = sys.argv[2]
depth = 4
for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
    print(find_next_move(board, player, depth))

    depth += 1
