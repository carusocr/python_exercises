"""
Function to generate permutations of outcomes
Repetition of outcomes not allowed
"""

def gen_permutations(outcomes, length):
    """
    Iterative function that generates set of permutations of
    outcomes of length num_trials
    No repeated outcomes allowed
    """
    
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                if item not in new_seq:
                    new_seq.append(item)
                    temp.add(tuple(new_seq))
        ans = temp    
    return ans
   
#
outcome = set(["a", "b", "c", "d", "e", "f"])
#
permutations = gen_permutations(outcome, 4)
permutation_list = list(permutations)
permutation_list.sort()

print "Answer is", permutation_list[100]

