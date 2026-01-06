from display import main
from grid import Grid

import random

total = 0

for size in [(10, 10), (20, 10), (30, 10), (40, 20), (50, 30), (100, 50), (1000, 500)]:
    '''
    BASIC MAZES: All Random x 300
    '''

    total += 300
    created = 0

    while created < total:
        noise = max(int(random.gauss(mu=20, sigma=5)), 1)
        chunks = max(int(random.gauss(mu=6, sigma=3)), 1)
        walls = max(int(random.gauss(mu=1, sigma=1)), 0)
        try:
            grid = Grid(20, 10, noise, chunks, walls)
            grid.save("TWENTYxTEN/" + str(created) + ".txt")
            print("saved")
            created += 1
        except Exception as e:
            print(f"An error occurred: {e}") 
            print("No Path Found")


    '''
    JUST NOISE: Only the random noise x 100
    '''

    total += 100

    while created < total:
        noise = max(int(random.gauss(mu=40, sigma=10)), 1)
        try:
            grid = Grid(20, 10, noise, 0, 0)
            grid.save("TWENTYxTEN/" + str(created) + ".txt")
            print("saved")
            created += 1
        except Exception as e:
            print(f"An error occurred: {e}") 
            print("No Path Found")


    '''
    CHUNKS AND NOISE: Noise and CHUNKS x 400
    '''

    total += 400

    while created < total:
        noise = max(int(random.gauss(mu=25, sigma=5)), 1)
        chunks = max(int(random.gauss(mu=8, sigma=3)), 1)
        try:
            grid = Grid(20, 10, noise, chunks, walls)
            grid.save("TWENTYxTEN/" + str(created) + ".txt")
            print("saved")
            created += 1
        except Exception as e:
            print(f"An error occurred: {e}") 
            print("No Path Found")


    '''
    WALLS AND NOISE: Walls with Noise added x 200
    '''

    total += 200

    while created < total:
        noise = max(int(random.gauss(mu=25, sigma=5)), 1)
        walls = max(int(random.gauss(mu=2, sigma=1)), 0)
        try:
            grid = Grid(20, 10, noise, chunks, walls)
            grid.save("TWENTYxTEN/" + str(created) + ".txt")
            print("saved")
            created += 1
        except Exception as e:
            print(f"An error occurred: {e}") 
            print("No Path Found")

