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

    sizes = [s for s in data.trials.keys() if data.trials[s]]

    for size_label in sizes:
        all_trials = data.trials[size_label]
        if not all_trials: continue

        # Extract weights (assuming all trials use the same WEIGHTS list)
        weights = sorted(all_trials[0].path_distances_man.keys())

        # Lists to store EVERY single data point for the scatter plot
        scatter_w = []
        scatter_nodes = []
        scatter_opt = []
        scatter_time = []

        # Lists for the "Mean" trend line
        nodes_means = []
        opt_means = []
        time_means = []

        for weight in weights:
            n_at_w = []
            o_at_w = []
            t_at_w = []

            for trial in all_trials:
                # 1. Parse size and normalize
                dims = trial.size.split('x')
                total_tiles = int(dims[0]) * int(dims[1])
                
                # 2. Get data
                nodes = trial.nodes_exploreds_man.get(weight, 0)
                path_len = trial.path_distances_man.get(weight, 0)
                time_val = trial.time_takens_man.get(weight, 0)

                # 3. Normalize
                node_ratio = nodes / total_tiles
                opt_ratio = path_len / trial.best_path_len if trial.best_path_len > 0 else 1
                # Time per 1000 tiles to make the number readable
                norm_time = (time_val / total_tiles) * 1000 

                # Add to scatter lists
                scatter_w.append(weight)
                scatter_nodes.append(node_ratio)
                scatter_opt.append(opt_ratio)
                scatter_time.append(norm_time)

                # Collect for mean calculation
                n_at_w.append(node_ratio)
                o_at_w.append(opt_ratio)
                t_at_w.append(norm_time)

            # Calculate means for the trend line
            nodes_means.append(np.mean(n_at_w))
            opt_means.append(np.mean(o_at_w))
            time_means.append(np.mean(t_at_w))

        # --- Plotting ---
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle("Weighted A* Performance Distribution (All Maze Sizes)", fontsize=16)

        # 1. Efficiency Scatter
        ax1.scatter(scatter_w, scatter_nodes, alpha=0.1, s=1, color='blue', label='Individual Trial')
        ax1.plot(weights, nodes_means, color='red', linewidth=2, label='Mean Trend')
        ax1.set_title("Search Efficiency")
        ax1.set_ylabel("Nodes Explored / Total Tiles")

        # 2. Optimality Scatter
        ax2.scatter(scatter_w, scatter_opt, alpha=0.1, s=1, color='green')
        ax2.plot(weights, opt_means, color='red', linewidth=2)
        ax2.axhline(y=1.0, color='black', linestyle='--', alpha=0.5)
        ax2.set_title("Path Optimality")
        ax2.set_ylabel("Found Path / Shortest Path")

        # 3. Time Scatter
        ax3.scatter(scatter_w, scatter_time, alpha=0.1, s=1, color='purple')
        ax3.plot(weights, time_means, color='red', linewidth=2)
        ax3.set_title("Normalized Execution Time")
        ax3.set_ylabel("Time per 1000 Tiles (ms)")
        ax3.set_yscale('log') # Log scale is still helpful for time variance

        for ax in [ax1, ax2, ax3]:
            ax.set_xlabel("Weight")
            ax.grid(True, alpha=0.3)
            # Optional: zoom in on the interesting part of the X axis
            # ax.set_xlim(0.8, 5.0) 

        ax1.legend(markerscale=10)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        file_name = f"astar_performance_scatter_{size_label}.png"
        plt.savefig(file_name, dpi=300)
        plt.show()


if __name__ == "__main__":
    # Ensure 'data.pkl' is in the same directory
    try:
        load_and_plot('data.pkl')
    except FileNotFoundError:
        print("Error: data.pkl not found. Please run experiment.py first.")