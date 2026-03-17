import pickle

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
    

def load_and_collate():
    data = Data()
    for x in range(6):
        print(f"data{x if x != 0 else ''}.pkl")
        with open(f"data{x if x != 0 else ''}.pkl", 'rb') as f:
            data_file = pickle.load(f)
            for trial in data_file.trials["100x50"]:
                data.add_trial(trial, "100x50")
    print(data.trials)

    with open('data_large.pkl', 'wb') as file:
        pickle.dump(data, file)

def load_and_collate2():
    with open("data7.pkl", 'rb') as f:
        data = pickle.load(f)

    with open(f"data_large.pkl", 'rb') as f:
        data_file = pickle.load(f)
        for trial in data_file.trials["100x50"]:
            data.add_trial(trial, "100x50")

    with open('data_final.pkl', 'wb') as file:
        pickle.dump(data, file)


if __name__ == '__main__':
    load_and_collate2()