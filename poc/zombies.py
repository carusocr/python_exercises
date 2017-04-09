"""
Student portion of Zombie Apocalypse mini-project
BFS:
while boundary is not empty:
    current_cell  <-  dequeue boundary
    for all neighbor_cell of current_cell:
        if neighbor_cell is not in visited:
            add neighbor_cell to visited
            enqueue neighbor_cell onto boundary
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._obstacle_list = obstacle_list
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                #print "setting ", cell, "to full"
                self.set_full(cell[0], cell[1])
        else:
            self._obstacle_list = []
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._obstacle_list = []
        self._zombie_list = []
        self._human_list = []
        poc_grid.Grid.clear(self)
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        return list(zombie for zombie in self._zombie_list)
        # replace with an actual generator

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))

       
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        return list(human for human in self._human_list)
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances

BFS:
while boundary is not empty:
    current_cell  <-  dequeue boundary
    for all neighbor_cell of current_cell:
        if neighbor_cell is not in visited:
            add neighbor_cell to visited
            enqueue neighbor_cell onto boundary
            This description can be modified to compute
            a distance field during breadth-first search as follows:
"""
#    Create a new grid visited of the same size as the original grid
#    and initialize its cells to be empty.
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        for obstacle in self._obstacle_list:
            visited.set_full(obstacle[0],obstacle[1])
        
#    Create a 2D list distance_field of the same size as the original
#    grid and initialize each of its entries to be the product
#    of the height times the width of the grid.
#    (This value is larger than any possible distance.)
        distance_field = [[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)]
                                for dummy_row in range(self._grid_height)]    
#    Create a queue boundary that is a copy of either the zombie list
#    or the human list. For cells in the queue, initialize visited
#    to be FULL and distance_field to be zero. We recommend that you
#    use our Queue class.
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            source_list = self._human_list
        else:
            source_list = self._zombie_list
        for cell in source_list:
            boundary.enqueue(cell)
            visited.set_full(cell[0],cell[1])
            distance_field[cell[0]][cell[1]] = 0

# Finally, implement a modified version of the BFS search described
#    above. For each neighbor_cell in the inner loop, check whether
#    the cell has not been visited and is passable. 
#    If so, update the visited grid and the boundary queue
#    as specified. In this case, also update the neighbor's distance
#    to be the distance to current_cell plus one 
#    (distance_field[current_cell[0]][current_cell[1]] + 1).
        while boundary:
            current_cell = boundary.dequeue()
            neighbors = visited.four_neighbors(current_cell[0],current_cell[1])
            for n_cell in neighbors:
                if visited.is_empty(n_cell[0],n_cell[1]):
                    visited.set_full(n_cell[0],n_cell[1])
                    boundary.enqueue(n_cell)
                    distance_field[n_cell[0]][n_cell[1]] = min(distance_field[n_cell[0]][n_cell[1]], distance_field[current_cell[0]][current_cell[1]]+1)
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        
        should use the eight_neighbors function
        """
        
        for human in self.humans():
            new_location = human
            distance = float("-inf")
            neighbors = self.eight_neighbors(human[0],human[1])
            distance = zombie_distance_field[human[0]][human[1]]
            # iterate over neighbors and set new dest if distance is greater
            for space in neighbors:
                if self.is_empty(space[0],space[1]):
                    new_dist = zombie_distance_field[space[0]][space[1]]
                    if new_dist > distance:
                        distance = new_dist
                        #print "found new dist of", new_dist
                        new_location = (space[0],space[1])
            #print self._human_list
            #print new_location
            self._human_list[self._human_list.index(human)]=new_location
            
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie in self.zombies():
            new_location = zombie
            distance = float("inf")
            neighbors = self.four_neighbors(zombie[0],zombie[1])
            distance = human_distance_field[zombie[0]][zombie[1]]
            # iterate, find closest human and stalk
            for space in neighbors:
                if self.is_empty(space[0],space[1]):
                    new_dist = human_distance_field[space[0]][space[1]]
                    if new_dist < distance:
                        distance = new_dist
                        new_location = (space[0],space[1])
            self._zombie_list[self._zombie_list.index(zombie)]=new_location
                        

# Start up gui for simulation - You will need to write some code above
# before this will work without errors
#apoc = Apocalypse(30,40)
#apoc.compute_distance_field([(0,1)])
#poc_zombie_gui.run_gui(Apocalypse(30, 40))
#obj = Apocalypse(3, 3, [], [(2, 2)], [(1, 1)])
#dist = [[4, 3, 2], [3, 2, 1], [2, 1, 0]]
#obj.move_humans(dist)
#print obj.humans()
#print obj._human_list
#print obj.compute_distance_field(ZOMBIE)
#obj = Apocalypse(3, 3, [(0, 0), (0, 1), (0, 2), (1, 0)], [(2, 1)], [(1, 1)])
#dist = [[9, 9, 9], [9, 1, 2], [1, 0, 1]]
#obj.move_humans(dist)
