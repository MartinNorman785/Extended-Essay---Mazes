import heapq
import colours as c

def bfs(grid):
    explored = set()
    frontier = [grid.start]

    while frontier:
        f = frontier[:]
        frontier = []

        for current in f:
            if current == grid.end:

                path = []
                while current.prev is not None:
                    path.append(current)
                    current = current.prev
                    current.colour = c.MAGENTA

                path.append(current)
                current.colour = c.GREEN
                return path

            
            explored.add(current)

            for neighbor in grid.get_next(grid.get_tile_loc(current)):
                n = grid.tiles[neighbor[0]][neighbor[1]]
                

                if n not in explored and n not in frontier:
                    frontier.append(n)
                    n.prev = current

