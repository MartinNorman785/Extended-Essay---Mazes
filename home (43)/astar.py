import heapq
import colours as c

def manhattan(loc, end):
    return abs(loc[0]-end[0]) + abs(loc[1]-end[1])

def euclidean(loc, end):
    return ((loc[0]-end[0])**2 + (loc[1]-end[1])**2)**(1/2)

def astar(grid, heuristic, weight=1, explored_count=False):
    explored = set()
    frontier = []

    if explored_count:
        count = 0
    
    heapq.heappush(frontier, (weight*heuristic(grid.get_tile_loc(grid.start), grid.get_tile_loc(grid.end)), grid.start))

    while frontier:
        if explored_count:
            count += 1
    
        cf, current = heapq.heappop(frontier)



        if current == grid.end:

            path = []
            while current.prev is not None:
                path.append(current)
                
                current = current.prev
                current.colour = c.YELLOW

            path.append(current)
            current.colour = c.GREEN
            if explored_count:
                return path, count
            else:
                return path

        if current not in explored:
            explored.add(current)

            for neighbor in grid.get_next(grid.get_tile_loc(current)):
                n = grid.tiles[neighbor[0]][neighbor[1]]
                
                if n.distance > current.distance + 1:
                    n.distance = current.distance + 1
                    n.prev = current


                n.heuristic = heuristic(neighbor, grid.get_tile_loc(grid.end))
                n.cost = round((n.distance + weight*n.heuristic)/(weight + 1), 1)

                heapq.heappush(frontier, (n.cost, n))



