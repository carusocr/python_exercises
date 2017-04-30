"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        print move_string
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction
                
    def position_tile(self, target_row, target_col, dest_row, dest_col):
        """function to return move string
        """
        move_str = ""
        # Move 0 up first
        row_dist = target_row - dest_row
        col_dist = target_col - dest_col
        move_str += "u" * row_dist
        # if target tile is to the left of 0
        if col_dist > 0:
            move_str += "l" * col_dist
            # now 0 is on left, target is on right, need to move target right
            # one urrdl string per col_dist?
            if dest_row > 0: # stay above invariant values
                move_str += "urrdl" * (col_dist-1)
                move_str += "druld" * row_dist
            else: # need to use downmoves
                move_str += "drrul" * (col_dist-1)
                move_str += "druld" * row_dist
            #print "coldist > 0: " + move_str
        elif col_dist == 0:
            # if in same column (0 on top of target tile now), move 
            # 0 next to target tile with + ld
            move_str += "ld"
            move_str += "druld" * (row_dist-1)
            #print "coldist == 0: " + move_str
        elif col_dist < 0:
            col_dist = abs(col_dist)
            # if target tile is to the right of 0
            move_str += "r" * (col_dist-1)
            if dest_row > 0:
                move_str += "rulld" * col_dist
                move_str += "druld" * row_dist
            else: #same row, use downmove first
                move_str += "rdllu" * col_dist
                move_str += "druld" * row_dist
            # cycle to reposition, times col dist
            #print "coldist < 0: " + move_str
                
        return move_str

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(target_row, target_col) == 0:
            for cur_col in range(target_col+1, self.get_width()):
                if (target_row, cur_col) != self.current_position(target_row, cur_col):
                    return False
            if target_row+1 == self.get_height():
                return True
            for cur_row in range(target_row+1, self.get_height()):
                for cur_col in range(0,self.get_width()):
                    if (cur_row, cur_col) != self.current_position(cur_row, cur_col):
                        return False
            return True
            
        return False

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)
        # get destination
        dest_row, dest_col = self.current_position(target_row, target_col)
        # move zero tile to location of target tile
        print "targ row and col:"
        print (target_row, target_col)
        print "dest row and col:"
        print (dest_row, dest_col)
        move_str = self.position_tile(target_row, target_col, dest_row, dest_col)
        self.update_puzzle(move_str)
        assert self.lower_row_invariant(target_row, target_col-1)
        return move_str

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        # move 0 tile from (i,0) to (i-1,1) using "ur"
        move_str = "ur"
        self.update_puzzle(move_str)
        dest_row, dest_col = self.current_position(target_row, 0)
        # if target tile already at (i,0), move tile 0 to end of row i-1
        if dest_row == target_row and dest_col == 0:
            # need to use -2 since we already moved right once
            lateral_move = (self.get_width()-2) * "r"
            self.update_puzzle(lateral_move)
            move_str += lateral_move
        else:
            # reposition target tile to (i-1, 1) and the 0 tile
            # to (i-1, 0)
            reposition = self.position_tile(target_row-1, 1, dest_row, dest_col)
            #print reposition
            self.update_puzzle(reposition)
            move_str += reposition
            #print "move string after repo: " + move_str
            # apply move string for 3x2 puzzle to bring target tile into 
            # position (i,0) (string from problem 9)
            threebytwo = "ruldrdlurdluurddlu"
            # move tile 0 to right end of row i-1
            threebytwo += "r" * (self.get_width()-1)
            self.update_puzzle(threebytwo)
            move_str += threebytwo
            #print "move string after 3x2: " + move_str

        assert self.lower_row_invariant(target_row-1, self.get_width()-1)
        return move_str

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0, target_col) != 0:
            return False
        # walk through tiles and check target tiles for solved
        for column in range(self.get_width()):
            for row in range(self.get_height()):
                if (row == 0 and column > target_col) or (row == 1 and column >= target_col) or row > 1:
                    if (row, column) != self.current_position(row, column):
                        return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if not self.lower_row_invariant(1, target_col):
            return False
        for column in range(self.get_width()):
            for row in range(2, self.get_height()):
                if (row, column) != self.current_position(row, column):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        # start with "ld" move and check if target tile is in (0,j)
        move_str = "ld"
        self.update_puzzle(move_str)
        dest_row, dest_col = self.current_position(0, target_col)
        if dest_row == 0 and dest_col == target_col:
            return move_str
        # need to reposition target tile to (1, j-1) with
        # tile 0 at (1, j-2)       
        reposition = self.position_tile(1, target_col-1, dest_row, dest_col)
        self.update_puzzle(reposition)
        move_str += reposition
        # apply move string from problem 10
        twobythree = "urdlurrdluldrruld"
        self.update_puzzle(twobythree)
        move_str += twobythree
        #print move_str
        assert self.row1_invariant(target_col-1)
        return move_str

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """             
        assert self.row1_invariant(target_col)
        dest_row, dest_col = self.current_position(1, target_col)
        # failed owltest many times due to having 0 instead of 1 here!
        # stupid mistake          vvvvvvvv
        move_str = self.position_tile(1, target_col, dest_row, dest_col)
        move_str += "ur" # ur to move upper tile to correct position
        self.update_puzzle(move_str)
        assert self.row0_invariant(target_col)
        return move_str 

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_str = ""
        zero_str = ""
        # get zero to top left
        if self.get_number(0,1) == 0:
            zero_str += "l"
        elif self.get_number(1,0) == 0:
            zero_str += "u"
        elif self.get_number(1,1) == 0:
            zero_str += "ul"
        self.update_puzzle(zero_str)
        # now zero is top left, check values of others and generate
        # appropriate move_str
        # if solved, return immediately
        if self.current_position(0,1) == (0,1) and self.current_position(1,0) == (1,0) and self.current_position(1,1) == (1,1):
            return zero_str
        if self.get_number(1,0) > self.get_number(1,1):
            move_str += "rdlu"        
        else:
            move_str += "drul"
        self.update_puzzle(move_str)
        return zero_str + move_str


    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        # steps:
        # 1. move zero tile to bottom right
        move_str = ""
        row = self.get_height()-1
        column = self.get_width()-1
        zero_row, zero_col = self.current_position(0,0)
        width = column - zero_col
        height = row - zero_row
        #print (width, height)
        zero_move = ("r" * width) + ("d" * height)
        move_str += zero_move
        #print move_str
        self.update_puzzle(move_str)
        # 2. solve bottom m-2 rows with solve_interior_tile, bottom to top
        for cur_row in range(row, 1, -1):
            for cur_col in range(column, 0, -1):
                #print "solving interior for: "
                #print cur_row, cur_col
                move_str += self.solve_interior_tile(cur_row, cur_col)
            #have to treat col0 with solve_col0
            move_str += self.solve_col0_tile(cur_row)
        # 3. solve rightmost n-2 cols to reduce to 2x2 grid
        for cur_col in range(column, 1, -1):
            move_str += self.solve_row1_tile(cur_col)
            move_str += self.solve_row0_tile(cur_col)
        # 4. call 2x2 solver
        move_str += self.solve_2x2()
        print move_str
        return move_str

# Start interactive simulation
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#obj.lower_row_invariant(2, 2)
#obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [7, 0, 8]])
#print obj.lower_row_invariant(2, 1) #expected True but received False
#obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]])
#print obj.lower_row_invariant(2, 0)
#obj = Puzzle(4, 5, [[12, 11, 10, 9, 8], [7, 6, 5, 4, 3], [2, 1, 0, 13, 14], [15, 16, 17, 18, 19]])
#print obj.lower_row_invariant(2, 2)
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj.solve_interior_tile(2, 2)
#obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#print obj.row1_invariant(1)
#print obj.get_width()
#obj = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
#print obj.solve_col0_tile(3)
#obj = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
#obj.solve_row1_tile(2) 
#obj = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
#print obj
#obj.solve_row0_tile(2)
#print obj
#obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#print obj
#obj.solve_2x2()
#print obj
#poc_fifteen_gui.FifteenGUI(Puzzle(3,3))
obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
obj.solve_puzzle()
# not solving row 1 correctly?
print obj


