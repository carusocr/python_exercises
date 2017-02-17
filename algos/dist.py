EX_GRAPH1 = { 0: set([1,4,5]), 1: set([2,6]), 2: set([3]),
             3: set([0]), 4: set([1]), 5: set([2]), 6: set([]) }
test_graph = {0: 1, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1}

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
  degree_dist = dict()
  for i in digraph:
    if degree_dist.get(digraph[i]) == None:
      degree_dist[digraph[i]] = 1
    else:
      degree_dist[digraph[i]] += 1
  return degree_dist

in_degs = compute_in_degrees(EX_GRAPH1)

print in_degree_distribution(test_graph)
