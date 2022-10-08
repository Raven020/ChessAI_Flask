from math import inf
import random
from flask import Flask, render_template, request,Response, make_response, jsonify
import chess

app = Flask(__name__)

board = chess.Board()
depth = 3
@app.route("/chess", methods=['POST','GET'])
@app.route("/", methods=['POST','GET'])
def chessServer():
    #if we have recieved a post request it means client is sending a new position
    if request.method == 'POST':
        print("REQUEST RECIEVED!");
        #print(request.form['position'])
        # get attempted move in correct format
        attemptedMove = chess.Move.from_uci(request.form['position'])
        returnDict = {'valid': 'invalid'}
        
        # if move is valid set return map valid to valid and make move on board
        if(attemptedMove in board.legal_moves):
            # if it is valid set it to valid
            print("valid move")
            returnDict['valid'] = 'valid'
            board.push(attemptedMove)
            print(board)
        # else if move is valid set return map valid to invalid and do not make move on board
        else:
            print("invalid move")
            returnDict['valid'] = 'invalid'

        if(board.is_check()):
            returnDict['check']= 'true'
        
        # return json of valid dict
        if(board.is_checkmate()):
            print("CheckMate!!")
            returnDict = returnWin(returnDict)

        return returnDict

    else:
        board.reset()
        print(board)
        return render_template('index.html', static_url_path='')

@app.route("/ai", methods=['GET'])
def getAImove():
   # ai_move = randomAI(board)
   # ai_move = pickBestInitialMove(board)
    #print("Number of Positions Evaluated - ", positions_evaluated)
    
    ai_move = getMoveMinimax(depth,board, False)
    returnDict = {}
    #move = {}
    returnDict['move'] = str(ai_move)
    board.push(ai_move)
    #responseMap['legalMoves'] = list(board.legal_moves)
    if(board.is_check()):
        returnDict['check']= 'true'
    
    if(board.is_checkmate()):
        print("CheckMate!!")
        returnDict = returnWin(returnDict)

    return returnDict

def returnWin(returnDict):
    """ Alters return dict in case of a win, adds win value to return map, and which color won

    Args:
        returnDict (dict): map of data to be returned to client

    Returns:
        dict: altered map
    """
    winner = board.outcome().winner
    if(winner == False):
        winner = "Black"
    else:
       winner = "White"
    returnDict['winner'] = winner
    returnDict['win']= 'true'
    return returnDict

def getLegalMoves(board):
    """ Returns a list of strings for all current legal moves 
    """
    list_of_moves = []
    for move in board.legal_moves:
        # make move a string
        pass
        # add string to list
    pass



def randomAI(board):
    """
    Returns a random move, stupid AI
    """
    list_of_moves = list(board.legal_moves)
    num1 = random.randrange(board.legal_moves.count())
    return list_of_moves[num1]

if __name__ == "__main__":
    app.run(debug=True)


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
        


def evaluateMove(move, given_board):
    """Evaluates the given move for the given board, creates a copy of the board, makes the move
        then evaluates the board

    Args:
        move (_type_): given move to evaluate
        board (_type_): given board to evaluate move on

    Returns:
        the evaluation of the move on the board
    """
    #create a new board add move evaluate board
    test_board = given_board.copy()
    test_board.push(move)
    return evaluateBoard(test_board)


def evaluateBoard(given_board):
    """ Evaluates a board, white is positive integers, black is negative integers

    Args:
        given_board (chess.Board): The board that is to be evaluated
    """
    dict_pieces = given_board.piece_map()
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


def getMoveMinimax(depth, board, maximising_player):
    """ Gets the best move out of all possible legal moves, calls the minimax function

    Args:
        depth (int): desired depth for minimax function
        board (chess.Board): game board
        maximising_player (bool): is the ai maximising?

    Returns:
        chess.Move: the best move found
    """
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
    #positions_evaluated += 1
    if(depth == 0):
       # print(-(evaluateBoard(board)))
        return (evaluateBoard(board))
    
    if(maximising_player):
        best_value = -inf

        for move in board.legal_moves:
            board.push(move)
            move_eval = minimax(depth - 1, board, (not maximising_player))
            board.pop()
            best_value = max(best_value, move_eval)
        return best_value
    
    else:
        best_value = inf

        for move in board.legal_moves:
            board.push(move)
            move_eval = minimax(depth - 1, board, (not maximising_player))
            board.pop()
            best_value = min(best_value, move_eval)
        return best_value