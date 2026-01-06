import colours as c
import pygame
import random

from astar import *
from bfs import bfs

#font_for_cost = pygame.font.SysFont("dejavusans", 15, True)
#font_for_heuristic = pygame.font.SysFont("dejavusans", 10, True)
class Tile():
    def __init__(self, size, x, y, free=True, heuristic=None, distance=None):
        self.size = size
        self.free = free
        
        self.x = x
        self.y = y

        self.x1 = x + size
        self.y1 = y + size

        self.colour = c.WHITE if self.free else c.GREY

        self.heuristic = None
        self.distance = float('inf')
        
        self.start = False
        self.end = False

        if self.heuristic is None:
            self.cost = None
        else:
            self.cost = heuristic + distance

        self.prev = None

    def reset(self):
        self.free = True
        self.colour = c.WHITE if self.free else c.GREY

        self.heuristic = None
        self.distance = float('inf')
        
        self.start = False
        self.end = False

        if self.heuristic is None:
            self.cost = None
        else:
            self.cost = heuristic + distance

        self.prev = None

    def change_free(self, free=None):
        if free is None:
            self.free = True if not self.free else False
        else:
            self.free = free
        
        self.colour = c.BEIGE if self.free else c.GREY
    
    def make_end(self):
        self.end = True
        self.colour = c.RED

    def make_start(self):
        self.start = True
        self.colour = c.GREEN

    def __gt__(self, other):
        if self.heuristic is not None:
            if self.heuristic > other.heuristic:
                return True
            elif self.heuristic < other.heuristic:
                return False

        if self.x > other.x:
            return True
        elif self.x > other.x:
            return False

        if self.y > other.y:
            return True

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.size, self.size), 0)

        if self.cost is not None:
            text = font_for_cost.render(str(self.cost), True, c.BLACK)
            width = text.get_width()
            height = text.get_height()
            win.blit(text, (self.x+self.size//2-width//2, self.y+self.size*0.6-height//2))

            text = font_for_heuristic.render(str(self.distance) + " " + str(self.heuristic), True, c.BLACK)
            width = text.get_width()
            height = text.get_height()
            win.blit(text, (self.x+self.size//2-width//2, self.y+self.size*0.2-height//2))


class Grid():
    OFFSETX = 50
    OFFSETY = 30
    TILE_SIZE = 35

    BORDER_SIZE = 2

    def __init__(self, length, height, noise=20, chunks=8, walls=1, check_path=True):
        self.LENGTH = length
        self.HEIGHT = height

        self.tiles = [
            [
                Tile(self.TILE_SIZE, self.OFFSETX + x*self.TILE_SIZE + (x*2 + 5)*self.BORDER_SIZE, self.OFFSETY + y*self.TILE_SIZE + (y*2 + 5)*self.BORDER_SIZE)
                for x in range(self.LENGTH)
            ]
            for y in range(self.HEIGHT)
            ]

        self.MAX_X = self.OFFSETX + (self.LENGTH - 1)*self.TILE_SIZE + (self.LENGTH*2+1)*self.BORDER_SIZE
        self.MAX_Y = self.OFFSETY + (self.HEIGHT - 1)*self.TILE_SIZE + (self.HEIGHT*2 + 10)*self.BORDER_SIZE


        self.make_random_filled(noise)
        self.make_random_chunks(chunks)
        self.make_random_walls(walls)

        self.choose_end()
        self.choose_start()



        if check_path:
            self.best_path = bfs(self)

            self.reset_prevs()

            if self.best_path is None:
                raise NoPath()


        '''
        path = astar(self, manhattan, 10)

        print(best_path == path)
        print(len(best_path), len(path))

        self.save("save.txt")
        self.clear()
        self.load("save.txt")
        '''



        

    def draw_main(self, win):
        # Background recreation
        win.fill(c.BEIGE)

        # Drawing the main grid

        pygame.draw.rect(win, c.BLACK, (self.OFFSETX, self.OFFSETY, self.MAX_X, self.MAX_Y), 0)

        for row in self.tiles:
            for tile in row:
                tile.draw(win)
    
    def make_random_filled(self, n):
        l = random.sample(range(self.LENGTH*self.HEIGHT), n)
        for x in l:
            self.tiles[x % self.HEIGHT][x // self.HEIGHT].change_free()

    def make_random_chunks(self, n, size=4, sizeSTD=3):
        l = random.sample(range(self.LENGTH*self.HEIGHT), n)
        for x in l:
            random_size = max(int(random.gauss(mu=size, sigma=sizeSTD)), 1)
            self.make_random_chunk(random_size, (x % self.HEIGHT, x // self.HEIGHT))

    def make_random_walls(self, n):
        for x in range(n):
            if random.choice([True, True, True, False]): # Vertical Barrier
                random_gap = min(max(int(random.gauss(mu=self.LENGTH / 5, sigma=self.LENGTH / 5)), 1), self.LENGTH // 8)
                self.make_random_wall(random_gap, random.sample(range(self.LENGTH), 1)[0], True)
            else:
                random_gap = min(max(int(random.gauss(mu=self.HEIGHT / 5, sigma=self.HEIGHT / 5)), 1), self.HEIGHT // 8)
                self.make_random_wall(random_gap, random.sample(range(self.HEIGHT), 1)[0], False)

    def make_random_chunk(self, size, loc):
        blocks = set([loc])
        nearby = self.get_next(loc)
        try:
            for i in range(size - 1):
                x = random.choice(tuple(nearby))
                blocks.add(x)
                nearby = nearby.union(self.get_next(x))
                nearby.difference_update(blocks)
        except:
            pass
        finally:
            for x in blocks:
                self.tiles[x[0]][x[1]].change_free(False)
        
    def make_random_wall(self, gap, loc, vertical):
        if vertical:
            safe = random.sample(range(self.HEIGHT), gap)
            for i, tile in enumerate([x[loc] for x in self.tiles]): # Column
                if i not in safe:
                    tile.change_free(False)    
        else:
            safe = random.sample(range(self.LENGTH), gap)
            for i, tile in enumerate(self.tiles[loc]): # Column
                if i not in safe:
                    tile.change_free(False)

    def get_next(self, loc):
        nexts = set()
        for d in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            n = (loc[0] + d[0], loc[1] + d[1])
            if n[0] >= 0 and n[0] < self.HEIGHT and n[1] >= 0 and n[1] < self.LENGTH and self.tiles[n[0]][n[1]].free:
                nexts.add(n)
        return nexts

    def choose_start(self):
        x = self.LENGTH * 15 //100

        y = random.choice(list(range(self.HEIGHT)))

        self.tiles[y][x].make_start()
        self.tiles[y][x].free = True
        
        self.start = self.tiles[y][x]

        self.tiles[y][x].distance = 0

    def choose_end(self):
        x = self.LENGTH * 85 // 100

        y = random.choice(list(range(self.HEIGHT)))

        self.tiles[y][x].make_end()
        self.tiles[y][x].free = True

        self.end = self.tiles[y][x]

    def get_tile_loc(self, tile):
        for y, row in enumerate(self.tiles):
            for x, t in enumerate(row):
                if tile == t:
                    return (y, x)

    def reset_prevs(self):
        for y, row in enumerate(self.tiles):
            for x, t in enumerate(row):
                t.prev = None

    def reset_costs(self):
        for row in self.tiles:
            for t in row:
                t.distance = float('inf')
                t.cost = None
                t.heuritic = None
        self.start.distance = 0

    
    def clear(self):
        for row in self.tiles:
            for tile in row:
                tile.reset()
    
    def save(self, filename):
        raw_maze = [["0" if x.free else "1" for x in row] for row in self.tiles]
        raw_maze = [' '.join(row) for row in raw_maze]
        with open(filename, 'w') as file:
            data = '\n'.join(raw_maze)
            start = self.get_tile_loc(self.start)
            end = self.get_tile_loc(self.end)
            data = data + "\n" + str(start[0]) + " " + str(start[1]) + " " + str(end[0]) + " " + str(end[1]) + "\n"
            data = data + str(self.LENGTH) + " " + str(self.HEIGHT) + "\n"
            file.write(data)
        print(filename)



    
    def load(self, filename):
        with open(filename, 'r') as file:
            read_list = [line.strip().split(" ") for line in file.readlines()]

        self.LENGTH = int(read_list[-1][0])
        self.HEIGHT = int(read_list[-1][1])

        self.tiles = [
            [
                Tile(self.TILE_SIZE, self.OFFSETX + x*self.TILE_SIZE + (x*2 + 5)*self.BORDER_SIZE, self.OFFSETY + y*self.TILE_SIZE + (y*2 + 5)*self.BORDER_SIZE, read_list[y][x] == "0")
                for x in range(self.LENGTH)
            ]
            for y in range(self.HEIGHT)
            ]

        self.start = self.tiles[int(read_list[-2][0])][int(read_list[-2][1])]
        self.end = self.tiles[int(read_list[-2][2])][int(read_list[-2][3])]


        self.start.make_start()
        self.end.make_end()

        self.best_path = bfs(self)





class NoPath(Exception):
    def __init__(self):
        self.message = "No Path Found"
        super().__init__("No Path Found")




