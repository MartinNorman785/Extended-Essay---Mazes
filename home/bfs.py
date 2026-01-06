from collections import deque
import colours as c

def bfs(grid):
    explored = set()
    frontier = deque([grid.start])

    explored.add(grid.start)

    while frontier:
        current = frontier.popleft()

        if current == grid.end:
            path = []
            while current is not None:
                path.append(current)
                current.colour = c.MAGENTA
                current = current.prev
            path[-1].colour = c.GREEN
            return path[::-1]

        for neighbor in grid.get_next(grid.get_tile_loc(current)):
            n = grid.tiles[neighbor[0]][neighbor[1]]

            if n not in explored:
                explored.add(n)
                n.prev = current
                frontier.append(n)

    return None