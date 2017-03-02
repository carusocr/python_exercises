"""
Provided code for Application portion of Module 2
"""

# general imports
import Queue
import urllib2
import random
import time
import math
import matplotlib.pyplot as plt

GRAPH1 = {0: set([1, 2, 3, 4]),
          1: set([0, 2, 3, 4]),
          2: set([0, 1, 3, 4]),
          3: set([0, 1, 2, 4]),
          4: set([0, 1, 2, 3])}


def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)

def random_order(ugraph):
    """
    Return a list of nodes in a graph in random order.
    """
    node_list = ugraph.keys()
    random.shuffle(node_list)
    return node_list

def bfs_visited(ugraph, start):
    '''
    Returns all nodes visited by bfs
    '''
    bfsq = Queue.Queue()
    bfsq.put(start)
    visited = set([start])
    while not bfsq.empty():
        node = bfsq.get()
        #visited.add(node)
        for newnode in ugraph[node]:
            if newnode not in visited:
                visited.add(newnode)
                bfsq.put(newnode)
    return visited

def cc_visited(ugraph):
    '''
    Takes the undirected graph ugraph and returns a list
    of sets, where each set consists of all the nodes
    (and nothing else) in a connected component, and there
    is exactly one set in the list for each connected 
    component in ugraph and nothing else.
    '''
    # CC is the list of sets
    c_c = []
    remaining_nodes = ugraph.keys()
    while remaining_nodes != []:
        node = remaining_nodes[random.randint(0,len(remaining_nodes)-1)]
        edges = bfs_visited(ugraph,node)
        c_c.append(edges)
        # finds anything that isn't in the set yet and sets remaining_nodes to those values
        remaining_nodes = [i for i in remaining_nodes if i not in edges]
    return c_c

def largest_cc_size(ugraph):
    '''
    Takes the undirected graph ugraph and returns the 
    size of the largest connected component in ugraph.
    '''
    max_size = 0
    c_c = cc_visited(ugraph)
    for component in c_c:
        if len(component) >= max_size:
            max_size = len(component)
    return max_size

def compute_resilience(ugraph, attack_order):
    '''
    Takes ugraph, list of nodes attack_order, and iterates
    through in attack_order. For each node in the list,
    removes the given node and its edges from the graph and
    computes the size of the largest connected component for
    the resulting graph. Function should return a list whose 
    k+1th entry is the size of the largest connected component
    in the graph after the removal of the first k nodes in
    attack_order. The first entry (indexed by zero) is the size
    of the largest connected component in the original graph.
    '''
    size_list = [largest_cc_size(ugraph)]
    victim_graph = dict(ugraph)
    for node in attack_order:
        victim_graph.pop(node)
        for i in victim_graph:
            victim_graph[i].discard(node)
        size_list.append(largest_cc_size(victim_graph))
    return size_list
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    
def legend_example():
    """
    Plot an example with two curves with legends
    """
    xvals = [1, 2, 3, 4, 5]
    yvals1 = [1, 2, 3, 4, 5]
    yvals2 = [1, 4, 9, 16, 25]

    plt.plot(xvals, yvals1, '-b', label='linear')
    plt.plot(xvals, yvals2, '-r', label='quadratic')
    plt.legend(loc='upper right')
    plt.show()



##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

answer_graph = load_graph(NETWORK_URL)
random_nodes = random_order(answer_graph)
x = []
y =  compute_resilience(answer_graph,random_nodes)
for i in range(len(random_nodes)+1):
  x.append(i)
print len(x)
print len(y)
plt.plot(x, y)
plt.show() 
#legend_example()
