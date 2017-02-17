"""
Merge function for 2048 game.
"""
# Iterate over the input and create an output list 
# that has all of the non-zero tiles slid over to the
# beginning of the list with the appropriate number of
# zeroes at the end of the list.

# Iterate over the list created in the previous step and 
# create another new list in which pairs of tiles in the
# first list are replaced with a tile of twice the value
# and a zero tile. 

# Repeat step one using the list created 
# in step two to slide the tiles to the beginning of the 
# list again.

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    new_line = line
    #sort zeroes by selecting non zeroes then appending zeroes
    new_line = [i for i in line if i !=0]
    new_line.extend(i for i in line if i == 0)
    line = new_line
    print new_line
    for i in range(0,len(line)-1):
        if new_line[i] == new_line[i+1]:
            new_line[i] += new_line[i+1]
            new_line[i+1] = 0
            line = new_line
    new_line = [i for i in line if i !=0]
    new_line.extend(i for i in line if i == 0)
    line = new_line
    return line

#tests
print merge([4,4,8])
print merge([2,2,0,2,0,4])
print merge([2,0,2,4])
print merge([0,0,2,2])
print merge([2,2,0,0])
print merge([2,2,2,2,2])
print merge([8,16,16,8])

