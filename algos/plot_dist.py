"""
This unnormalized distribution is easier to compute and can later be
normalized to sum to one by dividing each value by the total number of nodes.
"""

# general imports
import urllib2
import matplotlib.pyplot as plt

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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

citation_graph = load_graph(CITATION_URL)

in_degs = compute_in_degrees(citation_graph)
degree_dist = in_degree_distribution(in_degs)
print degree_dist
filtered_dist = {x:y for x,y in degree_dist.items() if x != 0}
x,y = zip(*filtered_dist.items())
print (x,y)
plt.xscale('log')
plt.yscale('log')
plt.title('Log/log Distribution of Physics Paper Citation Frequency')
plt.plot(x, y, 'bo')
plt.xlabel('Number of Citations')
plt.ylabel('Fraction of Publications')
plt.axis([0,10000,0.00001,1])
plt.show()
