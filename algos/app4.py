"""
Questions for Project 4
"""

import math
import random
import matplotlib.pyplot as plt
import app4_provided as ap
import proj4

def question_one():
  human_eyeless = ap.read_protein(ap.HUMAN_EYELESS_URL)
  fly_eyeless = ap.read_protein(ap.FRUITFLY_EYELESS_URL)
  smx = ap.read_scoring_matrix(ap.PAM50_URL)
  amx = proj4.compute_alignment_matrix(human_eyeless, fly_eyeless, smx, False)
  score, h_align, f_align = proj4.compute_local_alignment(human_eyeless, fly_eyeless, smx, amx)
  return score, h_align, f_align

def question_two():
  """

  compare each of the two sequences of the local alignment computed in Question 1 to this
  consensus sequence to determine whether they correspond to the PAX domain.

  Load the file ConsensusPAXDomain. For each of the two sequences of the local alignment
  computed in Question 1, do the following:

  1. Delete the dashes in the sequence.
  2. Compute the global alignment of this dashless sequence with the ConsensusPAXDomain
  sequence.
  3. Compare corresponding elements of these two globally-aligned sequence 
  (local vs. consensus) and compute the percentage of elements in these two sequences
   that agree.
  """

  score, h_align, f_align = question_one()

  h_stripped = h_align.replace('-','')
  f_stripped = f_align.replace('-','')
  smx = ap.read_scoring_matrix(ap.PAM50_URL)
  pax = ap.read_protein(ap.CONSENSUS_PAX_URL)
  amx = proj4.compute_alignment_matrix(h_stripped, pax, smx, True)
  score, h_align, f_align = proj4.compute_global_alignment(h_stripped, pax, smx, amx)
  print  "human: "
  print score, h_align, f_align
  # iterate over len of sequences, check index mat of both h_align and f_align, 
  # add 1 point per match, finish and divide points by len(h_align) to get pct.
  score = 0
  for i in range(len(h_align)):
    if h_align[i] == f_align[i]:
      score += 1
  print "human similarity score is" , float(score)/float(len(h_align))
  amx = proj4.compute_alignment_matrix(f_stripped, pax, smx, True)
  score, h_align, f_align = proj4.compute_global_alignment(f_stripped, pax, smx, amx)
  score = 0
  for i in range(len(h_align)):
    if h_align[i] == f_align[i]:
      score += 1
  print "fly similarity score is" , float(score)/float(len(h_align))
  

# question_one()
#(875, 'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ', 'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ')
question_two()
#human similarity score is 0.729323308271
#fly similarity score is 0.701492537313
