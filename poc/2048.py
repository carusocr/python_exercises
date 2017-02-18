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
    for tile_index in range(len(line)-1):
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
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._initial = {
            UP : [[0,width] for width in range(self._grid_width)],
            DOWN : [[self._grid_height-1,width] for width in range(self._grid_width)],
            LEFT : [[height, 0] for height in range(self._grid_height)],
            RIGHT : [[height, self._grid_width-1] for height in range (self._grid_height)]
        }
        
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles. 4x3 grid should be [[0,0,0,0],[0,0,0,0],[0,0,0,0]].
        Populate with two new tiles by calling new_tile twice.
        """
        # create HxW dictionary
        self._grid_list = []
        self._grid_list = [[0 for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]
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
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        if direction == UP or direction == DOWN:
            # note: what's the point of using the get_grid_height() function if
            # I can just reference self._grid_height?
            num_steps = self.get_grid_height()
        else:
            num_steps = self.get_grid_width()
        orig_grid = str(self._grid_list)
        for start_cell in self._initial[direction]:
            temp_list = []
            for step in range(num_steps):
                row = start_cell[0] + step * OFFSETS[direction][0]
                col = start_cell[1] + step * OFFSETS[direction][1]
                temp_list.append(self._grid_list[row][col])
            temp_list = merge(temp_list)
            for step in range(num_steps):
                row = start_cell[0] + step * OFFSETS[direction][0]
                col = start_cell[1] + step * OFFSETS[direction][1]
                self._grid_list[row][col] = temp_list[step]
                
        if str(orig_grid) != str(self._grid_list):
            self.new_tile()
       
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        available_positions = []
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self._grid_list[row][col] == 0:
                    available_positions.append([row, col])
        tile_chance = random.randint(0,9)
        if tile_chance == 9:
            tile_value = 4
        else:
            tile_value = 2
        # add tile to grid
        if available_positions:
            tile_location = random.choice(available_positions)
            self.set_tile(tile_location[0],tile_location[1],tile_value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid_list[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid_list[row][col]


#poc_2048_gui.run_gui(TwentyFortyEight(3,3))

#TwentyFortyEight(5,4)
