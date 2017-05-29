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
    """
    dist = float("inf")
    idx1 = -1
    idx2 = -1
    for dummy_u in range(0,len(cluster_list)):
        for dummy_v in range(0,len(cluster_list)):
            if dummy_u == dummy_v:
                continue
            tmpdist = cluster_list[dummy_u].distance(cluster_list[dummy_v])
            (dist, idx1, idx2) = min((dist, idx1, idx2),(tmpdist, dummy_u, dummy_v))
    
    return (dist, idx1, idx2)



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    dummy_n = len(cluster_list)
    if dummy_n <= 3:
        (dist, idx1, idx2) = slow_closest_pair(cluster_list)
    else:
        m_half = math.floor(dummy_n/2)
        #initialize left and right side lists
        l_cluster, r_cluster = cluster_list[:dummy_n/2], cluster_list[dummy_n/2:] 
        (rdist, ridx1, ridx2) = fast_closest_pair(r_cluster)
        (ldist, lidx1, lidx2) = fast_closest_pair(l_cluster)
        (dist, idx1, idx2) = min((ldist, lidx1, lidx2),(rdist, ridx1+m_half, ridx2+m_half))
        mid = (1/2.0) * (cluster_list[dummy_n/2-1].horiz_center() + cluster_list[dummy_n/2].horiz_center())
        (dist, idx1, idx2) = min((dist, idx1, idx2), (closest_pair_strip(cluster_list,mid,dist)))
    return (dist, int(idx1), int(idx2))


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    cluster_s = []
    dist = float('inf')
    idx1 = -1
    idx2 = -1
    # need to add return if empty set
    for cluster_i in range(len(cluster_list)):
        if abs(cluster_list[cluster_i].horiz_center() - horiz_center) < half_width:
            cluster_s.append(cluster_i)
    cluster_s.sort(key = lambda cluster_s: cluster_list[cluster_s].vert_center())
    for dummy_u in range(len(cluster_s)-1):
        temp_bound = min(dummy_u+3, len(cluster_s)-1)
        for dummy_v in range(dummy_u+1, temp_bound+1):
            tmpdist = cluster_list[cluster_s[dummy_u]].distance(cluster_list[cluster_s[dummy_v]])
            if tmpdist < dist and dist > 0:
                dist = tmpdist
                idx1 = cluster_s[dummy_u]
                idx2 = cluster_s[dummy_v]
    if dist == float("inf"):
        return (dist, idx1, idx2)
    else:
        return pair_distance(cluster_list, idx1, idx2)
            
 
    
######################################################################
# Code for hierarchical clustering
"""
For the second part of the Project, your task is to implement hierarchical clustering and k-means clustering. In particular, you should implement the following two functions:

𝚑𝚒𝚎𝚛𝚊𝚛𝚌𝚑𝚒𝚌𝚊𝚕_𝚌𝚕𝚞𝚜𝚝𝚎𝚛𝚒𝚗𝚐(𝚌𝚕𝚞𝚜𝚝𝚎𝚛_𝚕𝚒𝚜𝚝, 𝚗𝚞𝚖_𝚌𝚕𝚞𝚜𝚝𝚎𝚛𝚜) - Takes a list of 𝙲𝚕𝚞𝚜𝚝𝚎𝚛 objects and applies hierarchical clustering as described in the pseudo-code HierarchicalClustering from Homework 3 to this list of clusters. This clustering process should proceed until 𝚗𝚞𝚖_𝚌𝚕𝚞𝚜𝚝𝚎𝚛𝚜 clusters remain. The function then returns this list of clusters.
Note that your implementation of lines 5-6 in the pseudo-code need not match the pseudo-code verbatim. In particular, merging one cluster into the other using 𝚖𝚎𝚛𝚐𝚎_𝚌𝚕𝚞𝚜𝚝𝚎𝚛𝚜 and then removing the other cluster is fine. Note that, for this function, mutating 𝚌𝚕𝚞𝚜𝚝𝚎𝚛_𝚕𝚒𝚜𝚝 is allowed to improve performance.

𝚔𝚖𝚎𝚊𝚗𝚜_𝚌𝚕𝚞𝚜𝚝𝚎𝚛𝚒𝚗𝚐(𝚌𝚕𝚞𝚜𝚝𝚎𝚛_𝚕𝚒𝚜𝚝, 𝚗𝚞𝚖_𝚌𝚕𝚞𝚜𝚝𝚎𝚛𝚜, 𝚗𝚞𝚖_𝚒𝚝𝚎𝚛𝚊𝚝𝚒𝚘𝚗𝚜) - Takes a list of 𝙲𝚕𝚞𝚜𝚝𝚎𝚛 objects and applies k-means clustering as described in the pseudo-code KMeansClustering from Homework 3 to this list of clusters. This function should compute an initial list of clusters (line 2 in the pseudo-code) with the property that each cluster consists of a single county chosen from the set of the 𝚗𝚞𝚖_𝚌𝚕𝚞𝚜𝚝𝚎𝚛 counties with the largest populations. The function should then compute 𝚗𝚞𝚖_𝚒𝚝𝚎𝚛𝚊𝚝𝚒𝚘𝚗𝚜 of k-means clustering and return this resulting list of clusters.
As you implement KMeansClustering, here are a several items to keep in mind. In line 4, you should represent an empty cluster as a 𝙲𝚕𝚞𝚜𝚝𝚎𝚛 object whose set of counties is empty and whose total population is zero. The cluster centers μf, computed by lines 2 and 8-9, should stay fixed as lines 5-7 are executed during one iteration of the outer loop. To avoid modifying these values during execution of lines 5-7, you should consider storing these cluster centers in a separate data structure. Line 7 should be implemented using the 𝚖𝚎𝚛𝚐𝚎_𝚌𝚕𝚞𝚜𝚝𝚎𝚛𝚜 method from the 𝙲𝚕𝚞𝚜𝚝𝚎𝚛 class. 𝚖𝚎𝚛𝚐𝚎_𝚌𝚕𝚞𝚜𝚝𝚎𝚛𝚜 will automatically update the cluster centers to their correct locations based on the relative populations of the merged clusters.
"""


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        _, cluster_i, cluster_j = fast_closest_pair(cluster_list)
        cluster_list[cluster_i].merge_clusters(cluster_list[cluster_j])
        del cluster_list[cluster_j]  
    return cluster_list
    
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

#print slow_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0)])
#print closest_pair_strip([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 0, 1, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 1, 1, 0)], 0.5, 1.0)
#print closest_pair_strip([alg_cluster.Cluster(set([]), 1.0, 1.0, 1, 0),alg_cluster.Cluster(set([]), 1.0, 5.0, 1, 0), alg_cluster.Cluster(set([]),1.0, 4.0, 1, 0), alg_cluster.Cluster(set([]), 1.0, 7.0, 1, 0)], 1.0, 3.0) 
#expected one of the tuples in set([(1.0, 1, 2)]) but received (1.0, 2, 1)
fast_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 2, 0, 1, 0), alg_cluster.Cluster(set([]), 3, 0, 1, 0)])
#expected one of the tuples in set([(0.089442719099999998, 1, 4)]) but received (0.18248287590894655, 1, 2)
print closest_pair_strip([alg_cluster.Cluster(set([]), 0.32, 0.16, 1, 0), alg_cluster.Cluster(set([]), 0.39, 0.4, 1, 0), alg_cluster.Cluster(set([]), 0.54, 0.8, 1, 0), alg_cluster.Cluster(set([]), 0.61, 0.8, 1, 0), alg_cluster.Cluster(set([]), 0.76, 0.94, 1, 0)], 0.46500000000000002, 0.070000000000000007)
print fast_closest_pair([alg_cluster.Cluster(set([]), 0.02, 0.39, 1, 0), alg_cluster.Cluster(set([]), 0.19, 0.75, 1, 0), alg_cluster.Cluster(set([]), 0.35, 0.03, 1, 0), alg_cluster.Cluster(set([]), 0.73, 0.81, 1, 0), alg_cluster.Cluster(set([]), 0.76, 0.88, 1, 0), alg_cluster.Cluster(set([]), 0.78, 0.11, 1, 0)])
#expected one of the tuples in set([(0.076157731058639044, 3, 4)]) 
#but received (0.076157731058639044, 3.0, 4.0) (Exception: Invalid Types)
#Incompatible types being compared.  Expected 3  <type 'int'> but received 3.0
#<type 'float'>
