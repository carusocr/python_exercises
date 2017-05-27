"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster



######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       


    Pseudo-code:

    dist = float("inf")
    idx1 = -1
    idx2 = -1
    for i in cluster_list:
      for j in cluster_list:
        # next if i == j
        # tmpdist =  dist between cluster_list[i] and cluster_list[j]
        # (dist, idx1, idx2) = min{(dist, idx1, idx2,),(tmpdist, i, j)} # min compares first element of each tuple

    return (dist, idx1, idx2)
    """

    
    
    return ()



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       

    ***NOTE*** To sort clusters by vert/hori positions of cluster centers:
    cluster_list.sort(key = lambda cluster: cluster.vert_center())

    n = len(cluster_list)
    if n <= 3:
      (dist, idx1, idx2) = slow_closest_pair(cluster_list)
    else:
      m = math.floor(n/2)
      #populate left and right lists with halves of cluster_list
      (ldist, lidx1, lidx2) = fast_closest_pair(left_cluster_list)
      (rdist, ridx1, ridx2) = fast_closest_pair(right_cluster_list)
      (dist, idx1, idx2) = min((ldist,lidx1,lidx2),(rdist,ridx1+m,ridx2+m))
      mid = (xm-1 + xm)/2
      (dist, idx1, idx2) = min(dist, idx1, idx2), closest_pair_strip(cluster_list, mid, dist)
    return (dist, idx1, idx2)
      
    """
    
    return ()


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       


    Let S be a list of the set {i: |xi - mid| < w}
    Sort the indices in S in nondecreasing order of the vertical (y) coordinates of their associated points.
    k = |S|  <-- || means number of elements in item, not absolute value!
    dist = float("inf")
    idx1 = -1
    idx2 = -1
    for i in range(0,k-2):
      for j in range (i+1,min(i+3,k-1)):
        tmpdist = dist between S[i] and S[p]
        (dist, idx1, idx2) = min{(dist, idx1, idx2),(tmpdist, S[i], S[j])}

    return (dist, idx1, idx2)
    """

    return ()
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    return []


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
            
    return []


