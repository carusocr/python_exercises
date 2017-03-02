#import poc_queue
import random

GRAPH0 = {0: set([1]),
          1: set([0, 2]),
          2: set([1, 3]),
          3: set([2])}

GRAPH1 = {0: set([1, 2, 3, 4]),
          1: set([0, 2, 3, 4]),
          2: set([0, 1, 3, 4]),
          3: set([0, 1, 2, 4]),
          4: set([0, 1, 2, 3])}

GRAPH2 = {1: set([2, 4, 6, 8]),
          2: set([1, 3, 5, 7]),
          3: set([2, 4, 6, 8]),
          4: set([1, 3, 5, 7]),
          5: set([2, 4, 6, 8]),
          6: set([1, 3, 5, 7]),
          7: set([2, 4, 6, 8]),
          8: set([1, 3, 5, 7])}

GRAPH3 = {0: set([]),
          1: set([2]),
          2: set([1]),
          3: set([4]),
          4: set([3])}

GRAPH4 = {0: set([1, 2, 3, 4]),
          1: set([0]),
          2: set([0]),
          3: set([0]),
          4: set([0]),
          5: set([6, 7]),
          6: set([5]),
          7: set([5])}

GRAPH5 = {"dog": set(["cat"]),
          "cat": set(["dog"]),
          "monkey": set(["banana"]),
          "banana": set(["monkey", "ape"]),
          "ape": set(["banana"])}

def bfs_visited(ugraph, start):
    '''
    Returns all nodes visited by bfs
    '''
    q = poc_queue.Queue()
    q.enqueue(start)
    visited = set([start])
    while not q.__len__() == 0:
        node = q.dequeue()
        #visited.add(node)
        for j in ugraph[node]:
            if j not in visited:
                visited.add(j)
                q.enqueue(j)
    return visited

def cc_visited(ugraph):
    '''
    Takes the undirected graph ugraph and returns a list
    of sets, where each set consists of all the nodes
    (and nothing else) in a connected component, and there
    is exactly one set in the list for each connected 
    component in ugraph and nothing else.
    RemainingNodes = V(# nodes)
    CC = 0
    while RemainingNodes != 0:
      Let i = arbitrary node in RemainingNodes
      W = bfs_visited(ugraph, i?)
      CC = ?
      RemainingNodes = RemainingNodes - i
    return CC
    '''
    # CC is the list of sets
    CC = []
    remaining_nodes = ugraph.keys()
    while remaining_nodes != []:
        node = remaining_nodes[random.randint(0,len(remaining_nodes)-1)]
        edges = bfs_visited(ugraph,node)
        CC.append(edges)
        # finds anything that isn't in the set yet and sets remaining_nodes to those values
        remaining_nodes = [i for i in remaining_nodes if i not in edges]
    return CC

def largest_cc_size(ugraph):
    '''
    Takes the undirected graph ugraph and returns the 
    size of the largest connected component in ugraph.
    '''
    CC = []
    remaining_nodes = ugraph.keys()
    for i in range(len(remaining_nodes)):
        node = remaining_nodes[i]
        edges = bfs_visited(ugraph,node)
        CC.append(edges)
    return len(max(CC))

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
    pass
#cc_visited(alg_module2_graphs.GRAPH0) expected [set([0, 1, 2, 3])]
#largest_cc_size(alg_module2_graphs.GRAPH0) expected 4
#print bfs_visited(GRAPH1,0)
print cc_visited(GRAPH0)
#print largest_cc_size(GRAPH3)
#
