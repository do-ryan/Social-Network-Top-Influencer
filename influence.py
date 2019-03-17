import numpy as np
import datetime as dt
import heapq
import sys

#!/usr/bin/env python3.6.5

def build_adj_list(node_node_weight):
    # argument: numpy array edge description (row-wise: node1 node2 edge_weight)
    # return: adjacency list represented as a nested dictionary
    graph = {}
    for edge in node_node_weight:
        if graph.get(edge[0]) == None:
            graph[edge[0]] = {}
            graph[edge[0]][edge[1]] = edge[2]
        else:
            graph[edge[0]][edge[1]] = edge[2]
    return graph

def dijkstra(adj_list, source):
    # argument: nested dictionary adjacency list graph, source key
    # return: dictionary of shortest path time to each node from source
    shortest_paths = {}

    # initialize shortest path distances to all nodes that can possibly be reached
    for node in adj_list.keys():
        for target in adj_list[node]:
            shortest_paths[target] = float("inf")
    shortest_paths[source] = 0

    dist_node_list = []
    # construct 2d list (distances, nodes). This stores the unexplored nodes.
    for item in shortest_paths.items():
        dist_node_list.append([item[1], item[0]])

    # explore all the nodes and update shortest paths of adjacent nodes with each exploration
    while dist_node_list:
        heapq.heapify(dist_node_list) # construct heap list of distance keys
        explored_node = dist_node_list.pop(0)[1]

        if explored_node in adj_list: # check if the current node actually has influencees
            for adj_node in adj_list[explored_node]:  # relax the adjacent nodes
                if shortest_paths[explored_node] + adj_list[explored_node][adj_node] < shortest_paths[adj_node]: # if newly found path shorter
                    shortest_paths[adj_node] = shortest_paths[explored_node] + adj_list[explored_node][adj_node] # update shortest path dist
                    for dist_node in dist_node_list: # search through this list to see if the updated influencee is unexplored
                        if int(dist_node[1]) == adj_node:
                            dist_node[0] = shortest_paths[adj_node]  # if so, update unexplored node distances as well

    return shortest_paths

def compute_top_one_influencer(adj_list, T):
    # argument: nested dictionary adjacency list directed graph with weights representing time to influence, deadline T (float)
    # return: top 1 influencer node num (int), spread (int), runtime (float), influencees (list). In the case of a tie, the smaller influencer node number is returned.

    start_time = dt.datetime.now()

    influence_dict = compute_influencees(adj_list, T) # dict stores influencer: [influencees]

    # determine top 1 influencer from dictionary of influencer: [influencees]
    max_spread = 0
    top_1_influencer = None
    for influencer, influencees in influence_dict.items():
        if len(influencees) > max_spread:
            max_spread = len(influencees)
            top_1_influencer = influencer

    return top_1_influencer, max_spread, dt.datetime.now() - start_time, influence_dict[top_1_influencer]

def compute_top_two_influencer(adj_list, T, top_1_influencees):
    # argument: nested dictionary adjacency list directed graph with weights representing time to influence, deadline T (float), list of nodes influenced by top 1
    # return:  node with max marginal spread gain (int), marginal spread (int), spread (int), runtime (float), influencees (list), marginal_influencees (list)
    # In the case of a tie, the smaller influencer node number is returned.

    start_time = dt.datetime.now()

    influence_dict = compute_influencees(adj_list, T)  # dict stores influencer: [influencees]

    # determine top 2 influencer (max marginal spread gain) from influence_dict.
    max_marginal_spread = 0
    top_2_influencer = None
    for influencer, influencees in influence_dict.items():
        marginal_influencees = list(set(influencees) - set(top_1_influencees))
        if len(marginal_influencees) > max_marginal_spread:
            max_marginal_spread = len(marginal_influencees)
            top_2_influencer = influencer

    return top_2_influencer, max_marginal_spread, len(influence_dict[top_2_influencer]), dt.datetime.now() - start_time, influence_dict[top_2_influencer], list(set(influence_dict[top_2_influencer]) - set(top_1_influencees))

def compute_influencees(adj_list, T):
    # return: influencees of every influencer in directed nested dictionary adjacency list graph adj_list (within deadline T)

    spreads = {}

    # construct dictionary of influencer: [influencees]
    for influencer in adj_list.keys():  # iterate through all entities
        shortest_paths = dijkstra(adj_list, influencer)  # get time to influence all others for current entity
        for influencee, time in shortest_paths.items():
            if time <= T:
                if spreads.get(influencer) == None:
                    spreads[influencer] = []
                    spreads[influencer].append(influencee)
                else:
                    spreads[influencer].append(influencee)

    return spreads

def main(argv):
    if argv:
        graph_path = argv[0]
        deadline = float(argv[1])
    else:
        graph_path = "facebook_small.txt"
        deadline = 5

    graph = np.genfromtxt(graph_path)
    adj_list = build_adj_list(graph)
    top_one_influencer, top_one_spread, top_one_runtime, top_one_influencees = compute_top_one_influencer(adj_list, deadline)
    top_two_influencer, top_two_marginalspread, top_two_spread, top_two_runtime, top_two_influencees, top_two_marginalinfluencees = compute_top_two_influencer(adj_list, deadline, top_one_influencees)

    print("For graph '{}'".format(graph_path))
    print("TOP-1 INFLUENCER: {}, SPREAD: {}, TIME: {} h/min/s".format(int(top_one_influencer), top_one_spread, top_one_runtime))
    print("TOP-2 INFLUENCER: {}, MARGINAL SPREAD: {}, TIME: {} h/min/s".format(int(top_two_influencer), top_two_marginalspread, top_two_runtime))

    return top_one_runtime + top_two_runtime

if __name__ == "__main__":
    main(sys.argv[1:])
