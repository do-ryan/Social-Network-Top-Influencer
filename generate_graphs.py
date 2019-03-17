import numpy as np
import random

# this script generates a graph that is a subset (size num_nodes) of a larger graph in text format
# the input graph is of format: node1 node2 weight

def generate_graph(master_graph_path, num_nodes, num_edges):
    # takes in a large graph file, desired number of nodes and number of edges
    # generates a text file with a subset of the large graph with the specified number of nodes and number of edges

    master_graph = np.genfromtxt(master_graph_path)
    output_graph = []
    node_list = []

    random_edge = master_graph[random.randint(0, master_graph.shape[0] - 1)]
    while True:
        if len(set(node_list) | set([random_edge[0], random_edge[1]])) <= num_nodes and len(output_graph)+1 <= num_edges: # if both output size conditions have not yet been met
            node_list = list(set(node_list) | set([random_edge[0], random_edge[1]])) # union of nodes in current edge and output node list
            output_graph.append(random_edge)
            if len(output_graph) == num_edges and len(node_list) == num_nodes: # if output size conditions are met
                break
        random_edge = master_graph[random.randint(0, master_graph.shape[0] - 1)]


    with open("{}nodes{}edges.txt".format(num_nodes, num_edges, master_graph_path), 'w') as f:
        for edge in output_graph:
            f.write("{} {} {}\n".format(int(edge[0]), int(edge[1]), edge[2]))
        print "New graph generated: ", f

    return
