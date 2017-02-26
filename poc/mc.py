"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 30         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
# Add your functions here.
    
def mc_update_scores(scores, board, player):
    '''
    Update the scores grid by iterating
    over each square and assigning points:
    If winning board, each player-picked
    square gets +1, opponent-picked -1,
    empty 0. Switches to -1, +1 for loss.
    Draw means all squares = 0...just return 
    unchanged scores list!
    '''
    winner = board.check_win()
    if winner == provided.DRAW:
        return
    elif winner == provided.PLAYERX:
        mod = 1
    else:
        mod = -1
    dim = board.get_dim()
    for row in range(dim):
        for col in range(dim):
            square = board.square(row,col)
            if square == provided.PLAYERX:
                scores[row][col] += SCORE_CURRENT*mod
            elif square == provided.PLAYERO:
                scores[row][col] += -SCORE_OTHER*mod
    #print scores

def mc_trial(mc_board, player):
    '''
    1. Trial needs to play game until check_win != None
    2. Once game is over, check status
    3. If tie, all scores for grid = 0
    4. If x win, x tiles +1 and y tiles -1
    5. If y win, x tiles -1 and y tiles +1
    * for games that get won faster, weight scores?
    * what happens if cpu plays symmetric choices?
    '''
    while mc_board.check_win() == None:
        empties = mc_board.get_empty_squares()
        row,col = empties[random.randrange(len(empties))]
        mc_board.move(row,col,player)
        if player == provided.PLAYERO:
            player = provided.switch_player(provided.PLAYERO)
        else:
            player = provided.switch_player(provided.PLAYERX)
    
def get_best_move(board, scores):
    '''
    Takes current board and grid of scores,
    returns best move. For all empty squares,
    pick one with highest score. If more than
    one, pick randomly among those. If board
    has no empty spaces, this function shouldn't
    even be getting called!
    '''
    score_coords = 0
    max_score = -9999 # sloppy
    for row,col in board.get_empty_squares():
        if max_score <= scores[row][col]:
            score_coords = (row,col)
            max_score = scores[row][col]
    return score_coords

def mc_move(board, player, ntrials):
    '''
    Zug.
    '''
    #global scores
    dim = board.get_dim()
    scores = [[0 for dummy_row in range(dim)] for dummy_col in range(dim)]
    for _ in range(ntrials):
        mc_board = board.clone()
        mc_trial(mc_board, player)
        mc_update_scores(scores, mc_board, player)
    best_move = get_best_move(board, scores)
    return best_move

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.
#print get_best_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY]]), [[1, 2, 3], [7, 8, 9], [4, 5, 6]]) 
#print get_best_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.EMPTY, provided.EMPTY]]), [[-3, 6, -2], [8, 0, -3], [3, -2, -4]]) 
provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
#b = provided.TTTBoard(3)
#b.move(2,2,provided.PLAYERX)
#es = b.get_empty_squares()
