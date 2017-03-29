"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)
import random

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    max_score = 0
    for i in hand:
      score = len([x for x in hand if x == i])*i
      if score >= max_score:
        max_score = score
    return max_score

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    total = 0.0
    outcomes = [dummy_idx for dummy_idx in range(1,num_die_sides+1)]
    possible_sequence = gen_all_sequences(outcomes, num_free_dice)
    for combo in possible_sequence:
        total += score((held_dice+combo))
    return total/len(possible_sequence)

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    handset = [()]
    for elem in hand:  
        for partial_sequence in handset:
          #construct sets of tuples
          #print tuple(partial_sequence)+(elem,)
          handset = handset + [tuple(partial_sequence)+(elem,)]
    return set(handset)

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    held_hand = ()
    best_score = 0.0
    possible_holds = gen_all_holds(hand)
    for i in possible_holds:
      roll = expected_value(i, num_die_sides, (len(hand)-len(i)))
      if roll > best_score: 
        best_score = roll
        held_hand = i
    return (best_score, (held_hand))

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand = (4, 4, 4, 3, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
#run_example()
#hand = [random.randrange(1,7) for i in range(5)]
#print "Your roll: " + str(hand)
#print "Best score: " + str(score(hand))
print expected_value((3, 3), 8, 5)

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
#print expected_value((4,4),6,4)
#gen_all_holds((2,2,3,4,6))
#strategy((2,2,3,4,6),6)
