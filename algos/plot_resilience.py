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
import dpa_plot as DPA
import upa as UPA
import timeit

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

def make_complete_graph(num_nodes):
    '''make fully populated graph'''
    edges = dict()
    for start_node in range(0,num_nodes):
        edges[start_node] = set()
        for end_node in range(0,num_nodes):
            if start_node != end_node:
                edges[start_node].add(end_node)
    return edges

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
            #print new_graph[neighbor]
            #print "Neighbor: " , neighbor
            #print "Max degree node: " , max_degree_node
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

def remove_node(ugraph, node):
    '''Remove node from the graph. This also includes removal of the node
    from its neighbors.'''
    for neighbor in ugraph[node]:
        ugraph[neighbor].remove(node)
    del ugraph[node]

def fast_targeted_order(ugraph):
    new_graph = copy_graph(ugraph)
    degree_sets = [set()] * len(new_graph)
    for node, neighbors in new_graph.iteritems():
        degree = len(neighbors)
        degree_sets[degree].add(node)
    order = []

    for k in range(len(new_graph) - 1, -1, -1):
        while degree_sets[k]:
            u = degree_sets[k].pop()
            for neighbor in new_graph[u]:
                d = len(new_graph[neighbor])
                degree_sets[d].remove(neighbor)
                degree_sets[d - 1].add(neighbor)

            order.append(u)
            remove_node(new_graph, u)
    return order

def measure_targeted_order(n, m, func):
    graph = make_upa_graph(n, m)
    return timeit.timeit(lambda: func(graph), number=1)

def make_er_graph(n, p):
    """input: number of nodes n, probability p
    """
    graph = {x: set() for x in range(n)}
    for node in range(n):
      for edge in range(n):
        a = random.random()
        if a < p and node != edge:
            graph[node].add(edge)
            graph[edge].add(node)
    return graph

def compute_in_degrees(digraph):
    '''compute in_degrees of a given graph'''
    # need to add handling for zero!
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

def make_upa_graph(num_nodes, connections):
    ugraph = make_complete_graph(connections)
    upa = UPA.UPATrial(connections)
    for i in range(connections, num_nodes):
      edges = upa.run_trial(connections)
      ugraph[i] = edges
      for edge in edges:
        ugraph[edge].add(i)
    return ugraph
    
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

def generate_plots(order,title):
  ag_1 = load_graph(NETWORK_URL)
  ag_2 = make_er_graph(1239,.002)
  ag_3 = make_upa_graph(1239,2)
  random_nodes1 = order(ag_1)
  random_nodes2 = order(ag_2)
  random_nodes3 = order(ag_3)
  
  x1 = []
  x2 = []
  x3 = []
  y1 =  compute_resilience(ag_1,random_nodes1)
  y2 =  compute_resilience(ag_2,random_nodes2)
  y3 =  compute_resilience(ag_3,random_nodes3)
  for i in range(len(ag_1)+1):
    x1.append(i)
  for i in range(len(ag_2)+1):
    x2.append(i)
  for i in range(len(ag_3)+1):
    x3.append(i)
  plt.xlabel("Nodes Removed")
  plt.ylabel("Largest Connected Component")
  plt.title(title)
  plt.plot(x1, y1, label="network")
  plt.plot(x2, y2,label="ER (p=0.005)")
  plt.plot(x3, y3, label="UPA (m=5)")
  plt.legend(loc='upper right')
  plt.axis([0,1400,0,1400])
  plt.show() 

def plot_performance():
    xs = range(10, 1000, 10)
    m = 5
    ys_targeted = [measure_targeted_order(n, m, targeted_order) for n in xs]
    ys_fast_targeted = [measure_targeted_order(n, m, fast_targeted_order) for n in xs]

    plt.plot(xs, ys_targeted, '-r', label='targeted_order')
    plt.plot(xs, ys_fast_targeted, '-b', label='fast_targeted_order')
    plt.title('Targeted order functions performance (desktop Python)')
    plt.xlabel('Number of nodes in the graph')
    plt.ylabel('Execution time')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()
#legend_example()
#generate_plots(random_order,"Random Attack Order Resilience")
generate_plots(targeted_order,"Targeted Attack Order Resilience")
#generate_plots(fast_targeted_order, "Fast Targeted)
#question3() 
