'''

1. Initialize queue to empty.
2. for each node j do
3.   initialize dj to infinity
4. di = 0 (first node)
5. enqueue (Q,i)
6. while Q is not empty do
7.    j = dequeue(Q)
8. foreach neighbor h of j do
9.    if dh = infinity do
10.     di = dh+1
11.     enqueue (Q,h)
12. return dj

Instead of setting node distance to infinity, in the case of when we're considering all distances
to be 1, you can just use a set containing visited nodes and check that when traversing graph.

'''


import Queue

graph = {0: [1,3,4], 1: [0,2,3], 2: [1,4], 3: [0,1], 4: [0,2,5], 5: [4]}
 
def bfs(graph, start):
  q = Queue.Queue()
  q.put(start)
  visited = set([start])
  while not q.empty():
    node = q.get()
    #visited.add(node)
    for j in graph[node]:
      if j not in visited:
        visited.add(j)
        q.put(j)
  return visited

def cc_visited(graph):
  pass
      
      
    

print bfs(graph,0)
