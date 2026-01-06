from grid import Grid

import random

total = 0
created = 0

for size in [(10, 10), (20, 10), (30, 10), (40, 20), (50, 30), (100, 50)]:
    '''
    BASIC MAZES: All Random x 300
    '''

    total += 300


    while created < total:
        noise = max(int(random.gauss(mu=1.5*size[0], sigma=0.2*size[0])), 1)
        chunks = max(int(random.gauss(mu=0.4*size[0], sigma=0.1*size[0])), 1)
        walls = max(int(random.gauss(mu=0.1*size[0], sigma=0.02*size[0])), 0)
        try:
            grid = Grid(size[0], size[1], noise, 0, 0)
            grid.save("mazes/" + str(created) + ".txt")
            print("saved")
            created += 1
        except Exception as e:
            print(f"An error occurred: {e}") 
            print("No Path Found", created)


    '''
    JUST NOISE: Only the random noise x 100
    '''

    total += 100

    while created < total:
        noise = max(int(random.gauss(mu=2.5*size[0], sigma=0.2*size[0])), 1)
        try:
            grid = Grid(size[0], size[1], noise, 0, 0)
            grid.save("mazes/" + str(created) + ".txt")
            print("saved")
            created += 1
        except Exception as e:
            print(f"An error occurred: {e}") 
            print("No Path Found", created)


    '''
    CHUNKS AND NOISE: Noise and CHUNKS x 400
    '''

    total += 400

    while created < total:
        noise = max(int(random.gauss(mu=1.5*size[0], sigma=0.2*size[0])), 1)
        chunks = max(int(random.gauss(mu=0.6*size[0], sigma=0.1*size[0])), 1)
        try:
            grid = Grid(size[0], size[1], noise, chunks, 0)
            grid.save("mazes/" + str(created) + ".txt")
            print("saved")
            created += 1
        except Exception as e:
            print(f"An error occurred: {e}") 
            print("No Path Found", created)


    '''
    WALLS AND NOISE: Walls with Noise added x 200
    '''

    total += 200

    while created < total:
        noise = max(int(random.gauss(mu=1.5*size[0], sigma=0.2*size[0])), 1)
        walls = max(int(random.gauss(mu=0.15*size[0], sigma=0.03*size[0])), 0)
        try:
            grid = Grid(size[0], size[1], noise, 0, walls)
            grid.save("mazes/" + str(created) + ".txt")
            print("saved")
            created += 1
        except Exception as e:
            print(f"An error occurred: {e}") 
            print("No Path Found", created)

