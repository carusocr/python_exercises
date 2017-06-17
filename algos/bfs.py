'''
traversal:

start with empty list

- add starting node
- get neighbors
- add neighbors to end of list in order visited
- visit first neighbor, add their neighbors to end of list, repeat until all have been processed

Queue object:

enqueue(Q, x)
dequeue(Q) <- queue always returns first value

easy to simulate queue with an array, obviously...

For every node in list, initialize distance to infinity.
Then when we visit a neighbor, check if distance is still infinite.
For boundary cases, possible to have nodes that are connected to
each other but not to initial node.

'''

import Queue

graph = {'A': ['B', 'C'],
         'B': ['A', 'D', 'E'],
         'C': ['A', 'F'],
         'D': ['B'],
         'E': ['B', 'F'],
         'F': ['C', 'E']}

def bfs(graph, start, end):
  q = Queue.Queue()
  path = [start]
  q.put(path)
  visited = set([start])
  while not q.empty():
    path = q.get()
    last_node = path[-1]
    if last_node == end:
      return path 
    else:
      for node in graph[last_node]:
        if node not in visited:
          visited.add(node)
          q.put(path + [node])

#print bfs(graph, 'A', 'F')
