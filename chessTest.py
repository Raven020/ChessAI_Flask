from cmath import exp
import chess
import random
def main():
    board = chess.Board()
    move = None
    board.push(chess.Move.from_uci('a2a4'))
    #print(board.legal_moves)
    print("Initial evaluation - ",evaluateBoard(board))
    for i in range(100):
        #move = randomMove(board)
        #board.push_san(move)
        #move = randMove2(board)
        #moveInUCI = chess.Move.from_uci(move)
        move = pickBestInitialMove(board)
        #move = findMoveMinimax(3, board, False)
        board.push(move)

    print(board)
    print(evaluateBoard(board))
    print(True == board.is_checkmate)

    
def randomMove(board):
    move = None
    while(True):
    #
        pieces = ['P','R','N','B','Q','K']
        square =['a','b','c','d','e','f','g','h']
        number =['1','2','3','4','5','6','7','8']
        num1 = random.randrange(0,8)
        num2 = random.randrange(0,8)
        num3 = random.randrange(0,6)
        if(pieces[num3] == 'P'):
            move = square[num1] + number[num2]
            #print(move)
            
        else:
            move = pieces[num3] + square[num1] + number[num2]
        
        try:
            if(board.parse_san(move)):
                return move;
        except ValueError:
            #print("invalid san")
            pass

def randMove2(board):
    
    list_of_moves = list(board.legal_moves)
    num1 = random.randrange(board.legal_moves.count())
    return list_of_moves[num1]


def pickBestInitialMove(board):
    list_of_moves = list(board.legal_moves)
    best_value = 9999
    best_move = None
    for move in list_of_moves:
        move_eval = evaluateMove(move, board)

        if( move_eval < best_value):
            best_value =  move_eval
            best_move = move

    return best_move
        


def evaluateMove(move, board):
    #create a new board add move evaluate board
    test_board = board.copy()
    test_board.push(move)
    return evaluateBoard(test_board)


def evaluateBoard(board):
    dict_pieces = board.piece_map()
    all_pieces = list(dict_pieces.values())
    #print(all_pieces[0].symbol())
   # print('r' == all_pieces[0].symbol())
    total_eval = 0
    for i in all_pieces:
        piece = i.symbol()
        match piece:
            case "K": 
                total_eval += 900
            case "Q": 
                total_eval += 90
            case "R": 
                total_eval += 50
            case "B": 
                total_eval += 30
            case "N": 
                total_eval += 30
            case "P": 
                total_eval += 10

            case "k": 
                total_eval += -900
            case "q": 
                total_eval += -90
            case "r": 
                total_eval += -50
            case "b": 
                total_eval += -30
            case "n": 
                total_eval += -30
            case "p": 
                total_eval += -10
    return total_eval


def findMoveMinimax(depth, board, maximising_player):
    
    # for each move get minimax value
    best_value = 9999
    best_move = None
    for move in board.legal_moves:
        board.push(move)
        value = minimax(depth -1, board, (not maximising_player))
        board.pop()
        if(value <= best_value):
            best_move = move
            best_value = value
                # return best move
    return best_move

def minimax(depth, board, maximising_player):
    if(depth == 0):
        print(-(evaluateBoard(board)))
        return (evaluateBoard(board))
    
    if(maximising_player):
        best_value = 9999

        for move in board.legal_moves:
            board.push(move)
            move_eval = minimax(depth - 1, board, (not maximising_player))
            board.pop()
        best_value = max(best_value, move_eval)
        return best_value
    
    else:
        best_value = -9999

        for move in board.legal_moves:
            board.push(move)
            move_eval = minimax(depth - 1, board, (not maximising_player))
            board.pop()
        best_value = min(best_value, move_eval)
        return best_value



if __name__ =="__main__":
    main()