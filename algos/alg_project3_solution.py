import random
import urllib2
import matplotlib.pyplot as plt
import time
import timeit

from alg_proj3 import *

def gen_random_clusters(num_clusters):
  """
  creates a list of clusters where each cluster in this list corresponds to one randomly generated point in the square with corners (+/-1,+/-1).
  """
  return [alg_cluster.Cluster(set([]),random.uniform(-1,1),random.uniform(-1,1),0,0) for x in range(num_clusters)]

def measure_performance(n, func):
  ran_clus = gen_random_clusters(n)
  func(ran_clus)

def plot_performance():
  xs = range(2, 200)
  scp = [timeit.timeit(lambda: measure_performance(n, slow_closest_pair),number=1) for n in xs]
  fcp = [timeit.Timer(lambda: measure_performance(n, fast_closest_pair)).timeit(number=1) for n in xs]
  plt.plot(xs, scp, '-r', label='Slow Closest Pair')
  plt.plot(xs, fcp, '-b', label='Fast Closest Pair')
  plt.xlabel('Number of Clusters')
  plt.ylabel('Execution time')
  plt.legend(loc='upper left')
  plt.title('Comparison of execution time for fast vs. slow closest pair (desktop Python)')
  plt.tight_layout()
  plt.show()
  
#plot_performance()
