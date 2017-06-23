"""
Student template code for Project 4
Student will implement five functions:

"""

import math

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters (alphabet) and three scores: diag_score,
    off_diag_score, and dash_score. The function returns a dict of dicts whose 
    entries are indexes by pairs of characters in alphabet plus '-'. The score
    for any entry indexes by one or more dashes is dash_score. The score for
    the remaining off-diagonal entries is off_diag_score. 

    One final note for build_scoring_matrix is that, although an alignment with
    two matching dashes is not allowed, the scoring matrix should still include
    an entry for two dashes (which will never be used).
    """
    scoring_matrix = {}
    c_alpha = alphabet.copy()
    c_alpha.add('-')

    for dum_i in c_alpha:
        scoring_matrix[dum_i] = {}
        for dum_j in c_alpha:
            if dum_i == '-' or dum_j == '-':
                scoring_matrix[dum_i][dum_j] = dash_score
            elif dum_i == dum_j:
                scoring_matrix[dum_i][dum_j] = diag_score
            else:
                scoring_matrix[dum_i][dum_j] = off_diag_score
    return scoring_matrix

def compute_alignment_matrix(seq_x, seq_y, smx, global_flag):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common alphabet
    with the scoring matrix scoring_matrix. The function computes and returns the
    alignment matrix for seq_x and seq_y as described in the Homework. If global_flag
    is True, each entry of the alignment matrix is computed using the method described in
    Question 8 of the Homework. If global_flag is False, each entry is computed using
    the method described in Question 12 of the Homework.
    """
    m, n = len(seq_x), len(seq_y)
    score = [[0 for _x in range(n+1)] for _y in range(m+1)]
    if global_flag:
        for dum_i in range(1,m+1):
            score[dum_i][0] = score[dum_i-1][0] + smx[seq_x[dum_i-1]]['-']
        for dum_j in range(1,n+1):
                score[0][dum_j] = score[0][dum_j-1] + smx['-'][seq_y[dum_j-1]]
        for dum_i in range(1,m+1):
            for dum_j in range(1,n+1):
                score[dum_i][dum_j] = max(score[dum_i-1][dum_j-1] + smx[seq_x[dum_i-1]][seq_y[dum_j-1]],
                    score[dum_i-1][dum_j] + smx[seq_x[dum_i-1]]['-'],
                    score[dum_i][dum_j-1] + smx['-'][seq_y[dum_j-1]])
    else:
        score = [[0 for _x in range(n+1)] for _y in range(m+1)]
        for dum_i in range(1,m+1):
            for dum_j in range(1,n+1):
                score[dum_i][dum_j] = max(score[dum_i-1][dum_j-1] + smx[seq_x[dum_i-1]][seq_y[dum_j-1]],
                    score[dum_i-1][dum_j] + smx[seq_x[dum_i-1]]['-'],
                    score[dum_i][dum_j-1] + smx['-'][seq_y[dum_j-1]])       
                if score[dum_i][dum_j] < 0:
                    score[dum_i][dum_j] = 0
                
    return score
def compute_global_alignment(seq_x, seq_y, smx, amx):
    """
    Compute global alignment and return tuple of
    (score, align_x, align_y) where score is the score of the global
    alignment align_x and align_y.
    """
    dum_i, dum_j = len(seq_x), len(seq_y)
    x_align = ''
    y_align = ''
    score = amx[dum_i][dum_j]
    while dum_i > 0 and dum_j > 0:
        if amx[dum_i][dum_j] == amx[dum_i-1][dum_j-1] + smx[seq_x[dum_i-1]][seq_y[dum_j-1]]:
            x_align = seq_x[dum_i-1] + x_align
            y_align = seq_y[dum_j-1] + y_align
            dum_i -= 1
            dum_j -= 1
        else:
            if amx[dum_i][dum_j] == amx[dum_i-1][dum_j] + smx[seq_x[dum_i-1]]['-']:
                x_align = seq_x[dum_i-1] + x_align
                y_align = '-' + y_align
                dum_i -= 1
            else:
                x_align = '-' + x_align
                y_align = seq_y[dum_j-1] + y_align
                dum_j -= 1
    while dum_i > 0:
        x_align = seq_x[dum_i-1] + x_align
        y_align = '-' + y_align
        dum_i -= 1
    while dum_j > 0:
        x_align = '-' + x_align
        y_align = seq_y[dum_j-1] + y_align
        dum_j -= 1
    return (score, x_align, y_align)

def compute_local_alignment(seq_x, seq_y, smx, amx):
    """ Find highest val in alignment matrix, record i/j.
    Trace backwards using exact same technique as global.
    Stop when you find a 0.
    Any entry with a max value can be used.
    Return (score, x_align, y_align)
    Score should be optimal local alignment score (so amx[i_val][j_val]?)
    """
    x_align, y_align = '', ''
    maxscore, i_val, j_val = 0,0,0
    for row in range(len(amx)):
        for col in range(len(amx[0])):
            if amx[row][col] > maxscore:
                maxscore =  amx[row][col]
                i_val = row
                j_val = col
    
    while i_val > 0 and j_val > 0:
        if amx[i_val][j_val] == 0:
            break
        if amx[i_val][j_val] == amx[i_val-1][j_val-1] + smx[seq_x[i_val-1]][seq_y[j_val-1]]:
            x_align = seq_x[i_val-1] + x_align
            y_align = seq_y[j_val-1] + y_align
            i_val -= 1
            j_val -= 1
        else:
            if amx[i_val][j_val] == amx[i_val-1][j_val] + smx[seq_x[i_val-1]]['-']:
                x_align = seq_x[i_val-1] + x_align
                y_align = '-' + y_align
                i_val -= 1
            else:
                x_align = '-' + x_align
                y_align = seq_y[j_val-1] + y_align
                j_val -= 1
    return (maxscore, x_align, y_align)

def generate_null_distribution(seq_x, seq_y, smx, num_trials):
  """
  This functions should return a dictionary scoring_distribution that represents an unnormalized
  distribution generated by performing the following process num_trials times:
  1. Generate a random permutation rand_y of the sequence seq_y using random.shuffle().
  2. Compute the maximum value score for the local alignment of seq_x and rand_y using the
    score matrix smx.
  3. Increment the entry score in the dictionary scoring_distribution by one.
  Use the function generate_null_distribution to create a distribution with 1000 trials using
  the protein sequences HumanEyelessProtein and FruiflyEyelessProtein (with PAM50 smx). Important:
  use the HumanEyelessProtein as the first parameter seq_x (which stays fixed) and 
  FruitflyEyelessProtein as the second parameter seq_y (which is randomly shuffled) when calling 
  generate_null_distribution. Switching the order of these two parameters will lead to 
  slightly different answers for Q5 that may fuck your shit up!
  """
  pass
