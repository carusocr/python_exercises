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


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        # Muuuuuutation!!!!!!
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        dist, cluster_i, cluster_j = fast_closest_pair(cluster_list)
        cluster_list[cluster_i].merge_clusters(cluster_list[cluster_j])
        del cluster_list[cluster_j]
    return cluster_list



######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    Plain English version:
    
    1.Initialize old cluster using large population counties 
    2.For number of iterations 
      3.Initialize the new clusters to be empty 
      4.For each county 
          5.Find the old cluster center that is closest 
          6.Add the county to the corresponding new cluster 
      7.Set old clusters equal to new clusters 
    8.Return the new clusters
    """
    # Initialize old cluster using large population counties
    cluster = [dummy_cluster.copy() for dummy_cluster in cluster_list]
    cluster.sort(key = lambda cluster_list: cluster_list.total_population(), reverse = True)
    center = [dummy_cluster for dummy_cluster in cluster[:num_clusters]]
    for dummy_iter in range(num_iterations):
        # Initialize new clusters to be empty Cluster objects
        new_clusters = [alg_cluster.Cluster(set([]),0,0,0,0) for x in range(num_clusters)]
        # For each county
        for dummy_idx in range(len(cluster_list)):
            distance = float('inf')
            # Find the old cluster center that is closest
            for dummy_center in range(num_clusters):
                newdist = cluster_list[dummy_idx].distance(center[dummy_center])
                if newdist < distance:
                    distance = newdist
                    cluster_sel = dummy_center
            # Add county to corresponding new cluster
            #copy if empty, otherwise merge
            if new_clusters[cluster_sel] == []:
                new_clusters[cluster_sel] = cluster_list[dummy_idx].copy()
            else:
                new_clusters[cluster_sel].merge_clusters(cluster_list[dummy_idx])
        for dummy_center in range(num_clusters):
            # Set old clusters equal to new clusters
            center[dummy_center] = new_clusters[dummy_center].copy()

    return new_clusters
