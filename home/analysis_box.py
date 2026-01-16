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

def load_and_boxplot(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f)

    # Use all sizes present in the data
    sizes = [s for s in data.trials.keys() if data.trials[s]]

    for size_label in sizes:
        all_trials = data.trials[size_label]
        if not all_trials: continue

        # Extract and sort the weights used in this batch
        weights = sorted(all_trials[0].path_distances_man.keys())

        # Prepare lists to hold a list of values for EACH weight
        # e.g., efficiency_data = [[vals for w1], [vals for w2], ...]
        efficiency_data = []
        optimality_data = []
        time_data = []

        for weight in weights:
            nodes_at_w = []
            opt_at_w = []
            time_at_w = []

            for trial in all_trials:
                # 1. Parse size for normalization
                dims = trial.size.split('x')
                total_tiles = int(dims[0]) * int(dims[1])
                
                # 2. Get and Normalize data
                nodes = trial.nodes_exploreds_man.get(weight, 0)
                path_len = trial.path_distances_man.get(weight, 0)
                time_val = trial.time_takens_man.get(weight, 0)

                nodes_at_w.append(nodes / total_tiles)
                if trial.best_path_len > 0:
                    opt_at_w.append(path_len / trial.best_path_len)
                
                # Normalized time (ms per 1000 tiles)
                time_at_w.append((time_val / total_tiles) * 1000)

            efficiency_data.append(nodes_at_w)
            optimality_data.append(opt_at_w)
            time_data.append(time_at_w)

    # 4. Create the Plot
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle("Weighted A* Performance (Linear Weight Scaling)", fontsize=18, fontweight='bold')

    # Style: Purple palette to distinguish from previous "even" plots
    box_style = dict(patch_artist=True, 
                     boxprops=dict(facecolor='#F5EEF8', color='#8E44AD', alpha=0.7),
                     medianprops=dict(color='#5B2C6F', linewidth=2),
                     flierprops=dict(marker='o', markersize=2, alpha=0.2))

    # 1. Prepare the data (Assuming weights is your list of 0.1 ... 5.0)
    weights = sorted(all_trials[0].path_distances_man.keys()) 

    # 2. Create the Figure
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(22, 7))

    # 3. Plot using 'positions=weights'
    # This puts the box for weight 5.0 at coordinate 5.0 on the x-axis.
    # We set 'widths' small (0.07) so the 0.1-increment boxes don't touch.
    box_width = 0.07 
    style = dict(patch_artist=True, boxprops=dict(facecolor='#E8F8F5', color='#16A085'))

    ax1.boxplot(efficiency_data, positions=weights, widths=box_width, **style)
    ax2.boxplot(optimality_data, positions=weights, widths=box_width, **style)
    ax3.boxplot(time_data, positions=weights, widths=box_width, **style)

    # 4. Format the X-Axis to show the full 0.1 - 5.0 range
    for ax in [ax1, ax2, ax3]:
        # Set ticks every 0.5 so they don't overlap, but the boxes stay at their weights
        tick_values = np.arange(0, 5.5, 0.5)
        ax.set_xticks(tick_values)
        
        # Force the x-axis to show the whole range
        ax.set_xlim(0, 5.2) 
        
        ax.set_xlabel("Weight ($w$)")
        ax.grid(True, linestyle=':', alpha=0.6)

    ax1.set_ylabel("Nodes Explored / Total Tiles")
    ax2.set_ylabel("Path Length / Shortest Path")
    ax2.axhline(y=1.0, color='r', linestyle='--', label='Optimal')
    ax3.set_ylabel("Time (ms / 1k tiles)")
    ax3.set_yscale('log')


    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    file_name = f"astar_boxplot_{size_label}.png"
    plt.savefig(file_name, dpi=300)
    plt.show()

if __name__ == "__main__":
    try:
        load_and_boxplot('data.pkl')
    except FileNotFoundError:
        print("Error: data.pkl not found.")