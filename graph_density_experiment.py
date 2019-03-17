import generate_graphs
import matplotlib.pyplot as plt
import influence
import numpy as np
import datetime
plt.interactive(True)

def main():

    fixed_num_nodes = 100

    for i in np.arange(2, 10.25, 0.25):
         generate_graphs.generate_graph("facebook_large.txt", fixed_num_nodes, num_edges=fixed_num_nodes*i)

    density_time_data = []
    for i in np.arange(2, 10.25, 0.25):
        density_time_data.append([i, influence.main(["{}nodes{}edges.txt".format(fixed_num_nodes, fixed_num_nodes*i), 5]).total_seconds()])

    plot_data = zip(*density_time_data)
    plt.scatter(plot_data[0], plot_data[1])

    plt.xlabel("Graph density (# edges / # nodes)")
    plt.ylabel("Top 1 and 2 Influencer Computation Run-time (s)")
    plt.title("Top Influencer Computation (Dijkstra) Run-time vs. Graph Density")
    plt.grid(True)

    plt.savefig("runtime_v_density.png")


if __name__ == "__main__":
    main()