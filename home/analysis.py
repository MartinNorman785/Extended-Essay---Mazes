import pickle
import matplotlib.pyplot as plt
import numpy as np

# Re-defining skeletons for Pickle to map the data correctly
class Trial:
    def __init__(self, size, best_path_len):
        self.size = size
        self.best_path_len = best_path_len
        self.path_distances_man = {}
        self.nodes_exploreds_man = {}
        self.time_takens_man = {}
        self.path_distances_euc = {}
        self.nodes_exploreds_euc = {}
        self.time_takens_euc = {}

class Data:
    def __init__(self):
        self.trials = {}

def load_and_plot(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f)

    # 1. Prepare to aggregate data
    # We want to see how Weight affects performance across all trials of a specific size
    sizes = [s for s in data.trials.keys() if data.trials[s]]

    nodes_all = []
    opt_all = []
    time_all = []
    
    for size_label in sizes:
        trials = data.trials[size_label]
        if not trials: continue

        # Extract weights from the first trial
        weights = sorted(trials[0].path_distances_man.keys())
        
        # Aggregators for means
        nodes_man = []
        opt_man = [] # Path length / Best Path Length
        time_man = []

        nodes_all.append(nodes_man)
        opt_all.append(opt_man)
        time_all.append(time_man)



        for w in weights:
            # Average nodes explored at this weight
            n_m = np.mean([t.nodes_exploreds_man[w] for t in trials])
            nodes_man.append(n_m)

            # Average optimality ratio (1.0 is perfect)
            o_m = np.mean([t.path_distances_man[w] / t.best_path_len for t in trials])
            opt_man.append(o_m)

            t_m = np.mean([t.time_takens_man[w] for t in trials])
            time_man.append(t_m)

        # 2. Create the Plots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(f"Weighted A* Performance: Grid Size {size_label}", fontsize=16)

        # Plot Efficiency (Nodes Explored)
        ax1.plot(weights, nodes_man, label='Manhattan', marker='o', markersize=4)
        ax1.set_title("Search Efficiency (Lower is Better)")
        ax1.set_xlabel("Weight")
        ax1.set_ylabel("Avg Nodes Explored")
        ax1.grid(True, linestyle='--', alpha=0.6)

        # Plot Optimality (Path Length Ratio)
        ax2.plot(weights, opt_man, label='A*', marker='o', markersize=4)
        ax2.axhline(y=1.0, color='r', linestyle='--', label='Optimal')
        ax2.set_title("Path Optimality (1.0 is Optimal)")
        ax2.set_xlabel("Weight")
        ax2.set_ylabel("Path Length / Best Path")
        ax2.legend()
        ax2.grid(True, linestyle='--', alpha=0.6)

        # Plot Time taken
        ax3.plot(weights, time_man, label='Manhattan', marker='o', markersize=4)
        ax3.set_title("Average time taken")
        ax3.set_xlabel("Weight")
        ax3.set_ylabel("Time Taken")
        ax3.grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        file_name = f"astar_performance_{size_label}.png"
        plt.savefig(file_name, dpi=300)

        plt.show()
    

    # 2. Create the Plots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"Weighted A* Performance: All Sizes", fontsize=16)
    

    for i, size_label in enumerate(sizes):
        ax1.plot(weights, nodes_all[i], label=size_label, marker='o', markersize=4)
        ax2.plot(weights, opt_all[i], label=size_label, marker='o', markersize=4)
        ax3.plot(weights, time_all[i], label=size_label, marker='o', markersize=4)
    
    # Plot Efficiency (Nodes Explored)
    ax1.set_title("Search Efficiency (Lower is Better)")
    ax1.set_xlabel("Weight")
    ax1.set_ylabel("Avg Nodes Explored")
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Plot Optimality (Path Length Ratio)
    ax2.axhline(y=1.0, color='r', linestyle='--', label='Optimal')
    ax2.set_title("Path Optimality (1.0 is Optimal)")
    ax2.set_xlabel("Weight")
    ax2.set_ylabel("Path Length / Best Path")
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)

    # Plot Time taken
    ax3.set_title("Average time taken")
    ax3.set_xlabel("Weight")
    ax3.set_ylabel("Time Taken")
    ax3.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    file_name = f"astar_performance_all.png"
    plt.savefig(file_name, dpi=300)

    plt.show()



if __name__ == "__main__":
    # Ensure 'data.pkl' is in the same directory
    try:
        load_and_plot('data.pkl')
    except FileNotFoundError:
        print("Error: data.pkl not found. Please run experiment.py first.")