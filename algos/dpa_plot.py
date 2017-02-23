"""
Provided code for application portion of module 1

Helper class for implementing efficient version
of DPA algorithm
"""

# general imports
import random
import matplotlib.pyplot as plt

num_nodes = 10000
m = 13

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def make_complete_graph(num_nodes):
    '''make fully populated graph'''
    edges = dict()
    for start_node in range(0,num_nodes):
        edges[start_node] = set()
        for end_node in range(0,num_nodes):
            if start_node != end_node:
                edges[start_node].add(end_node)
    return edges

def make_dpa_graph(m,n):
  graph = make_complete_graph(m)
  new_node = DPATrial(m)
  for i in range(m, n):
    graph[i] = new_node.run_trial(m)
  return graph

def make_plot(degree_dist):
  x,y = zip(*degree_dist.items())
  plt.xscale('log')
  plt.yscale('log')
  plt.plot(x,y,'bo')
  plt.title('Log/log distribution of DPA in_degrees')
  plt.ylabel('Fraction of Nodes')
  plt.xlabel('Number of in_degrees')
  plt.axis([0,10000,0.00001,1])
  plt.show()

def compute_in_degrees(digraph):
    '''compute in_degrees of a given graph'''
    in_degrees = dict()
    for start_node in digraph:
        for end_node in digraph[start_node]:
            if end_node in in_degrees:
                in_degrees[end_node] += 1
            else:
                in_degrees[end_node] = 1
        if start_node not in in_degrees:
            in_degrees[start_node] = 0
    return in_degrees

def in_degree_distribution(digraph):
  # added normalization
  total_nodes = len(digraph)
  degree_dist = dict()
  for i in digraph:
    if degree_dist.get(digraph[i]) == None:
      degree_dist[digraph[i]] = 1
    else:
      degree_dist[digraph[i]] += 1
  for i in degree_dist:
    degree_dist[i] = float(degree_dist[i]) / float(total_nodes)
  return degree_dist

digraph = make_dpa_graph(m,num_nodes)
in_degs = compute_in_degrees(digraph)
degree_dist = in_degree_distribution(in_degs)
make_plot(degree_dist)
