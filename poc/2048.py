"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    new_line = line
    #sort zeroes by selecting non zeroes then appending zeroes
    new_line = [i for i in line if i !=0]
    new_line.extend(i for i in line if i == 0)
    line = new_line
    print new_line
    for tile_index in range(0,len(line)-1):
        if new_line[tile_index] == new_line[tile_index+1]:
            new_line[tile_index] += new_line[tile_index+1]
            new_line[tile_index+1] = 0
            line = new_line
    new_line = [i for i in line if i !=0]
    new_line.extend(i for i in line if i == 0)
    line = new_line
    return line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles. 4x3 grid should be [[0,0,0,0],[0,0,0,0],[0,0,0,0]].
        Populate with two new tiles by calling new_tile twice.
        """
        # create HxW dictionary
        self._grid_list = []
        for _ in range(0,self._grid_width):
            row_list = []
            for _ in range(0,self._grid_height):
                row_list.append(0)
            self._grid_list.append(row_list)
        # populate with two new tiles
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._grid_list)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        pass

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        tile_chance = random.randint(0,9)
        if tile_chance == 9:
            tile_value = 4
        else:
            tile_value = 2
        # add tile to grid
        column = random.randrange(0,self._grid_width)
        row = random.randrange(0,self._grid_height)
        if self._grid_list[column][row] == 0:
            self._grid_list[column][row] = tile_value
        else:
            self.new_tile()

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid_list[col][row] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid_list[col][row]


poc_2048_gui.run_gui(TwentyFortyEight(3,3))
