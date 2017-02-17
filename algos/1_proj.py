'''
Testing graph functions
'''

EX_GRAPH0 = { 0: set([1,2]), 1: set([]), 2: set([]) }
EX_GRAPH1 = { 0: set([1,4,5]), 1: set([2,6]), 2: set([3]),
             3: set([0]), 4: set([1]), 5: set([2]), 6: set([]) }
EX_GRAPH2 = { 0: set([1,4,5]), 1: set([2,6]), 2: set([3,7]),
             3: set([7]), 4: set([1]), 5: set([2]), 6: set([]),
              7: set([3]), 8: set([1,2]), 9: set([0,3,4,5,6,7]) }
GRAPH0 = {0: set([1]),
          1: set([2]),
          2: set([3]),
          3: set([0])}

def make_complete_graph(num_nodes):
    '''make fully populated graph'''
    edges = dict()
    for start_node in range(0,num_nodes):
        edges[start_node] = set()
        for end_node in range(0,num_nodes):
            if start_node != end_node:
                edges[start_node].add(end_node)
    return edges

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

def in_degree_distribution(digraph):
    '''Takes digraph dict and returns a dictionary
    whose keys correspond to in-degrees of nodes 
    in the graph.'''
    in_degrees = compute_in_degrees(digraph)
    degree_dist = dict()
    for start_node in in_degrees:
        if degree_dist.get(in_degrees[start_node]) == None:
            degree_dist[in_degrees[start_node]] = 1
        else:
            degree_dist[in_degrees[start_node]] += 1
    return degree_dist
            

#print compute_in_degrees(EX_GRAPH1)

#print in_degree_distribution(GRAPH0)