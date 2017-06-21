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
  print score, h_align, f_align

question_one()
