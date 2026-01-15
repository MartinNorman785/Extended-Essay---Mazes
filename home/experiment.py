from grid import Grid
from astar import *

import pickle
import time

WEIGHTS = [x/10 for x in range(1, 20, 1)] + [x/100 for x in range(200, 501, 25)]

class Trial():
    def __init__(self, size, best_path_len):
        self.size = size
        self.best_path_len = best_path_len
        
        self.path_distances_man = {}
        self.nodes_exploreds_man = {}
        self.time_takens_man = {}
        
        self.path_distances_euc = {}
        self.nodes_exploreds_euc = {}
        self.time_takens_euc = {}

class Data():
    def __init__(self):
        self.trials = {
            "10x10": [],
            "20x10": [],
            "30x10": [],
            "40x20": [],
            "50x30": [],
            "100x50": [],
            "1000x500": [],
        }

    def add_trial(self, trial, size):
        self.trials[size].append(trial)
    


def conduct_trial(filename):
    grid = Grid(10, 10, check_path=False)
    grid.load(filename)

    size = str(grid.LENGTH) + "x" + str(grid.HEIGHT)

    trial = Trial(size, len(grid.best_path))

    for weight in WEIGHTS:
        start_time = time.perf_counter()
        man, explored = astar(grid, manhattan, weight, explored_count=True)
        end_time = time.perf_counter()

        trial.path_distances_man[weight] = len(man)
        trial.time_takens_man[weight] = end_time - start_time
        trial.nodes_exploreds_man[weight] = explored
        grid.reset_costs()
    return trial, size

def conduct_trials(numbertrials, filepath):
    data = Data()
    for x in range(numbertrials):
        print(x)
        filename = filepath + "/" + str(x) + ".txt"
        trial, size = conduct_trial(filename)

        data.add_trial(trial, size)
    return data

if __name__ == "__main__":

    data = conduct_trials(4000, "mazes")

    with open('data.pkl', 'wb') as file:
        pickle.dump(data, file)




