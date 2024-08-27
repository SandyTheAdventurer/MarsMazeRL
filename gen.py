import pygame
import random
import numpy as np
import sys

sys.setrecursionlimit(10**6)
def maze_modify(a):
    cs = random.randint(5, 15)
    rs = random.randint(10, 20)
    
    for _ in range(cs):
        j = random.randint(0, len(a) - 1)
        k = random.randint(0, len(a[0]) - 1)
        if a[j][k] == 0:
            a[j][k] = 2
        else:
            cs -= 1
    
    for _ in range(rs):
        j = random.randint(0, len(a) - 1)
        k = random.randint(0, len(a[0]) - 1)
        if a[j][k] == 0:
            a[j][k] = 3
        else:
            rs -= 1
    
    return a

def generate_maze(height, breadth):
    def in_bounds(x, y):
        return 0 <= x < height and 0 <= y < breadth

    def get_neighbors(x, y):
        neighbors = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
        return [(nx, ny) for nx, ny in neighbors if in_bounds(nx, ny)]

    def dfs(x, y):
        maze[x, y] = 0
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if in_bounds(nx, ny) and maze[nx, ny] == 1:
                maze[x + dx, y + dy] = 0
                dfs(nx, ny)

    maze = np.ones((height, breadth), dtype=int)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    start_x, start_y = 1, 1
    maze[start_x, start_y] = 0
    dfs(start_x, start_y)

    end_x, end_y = height - 2, breadth - 2
    maze[end_x, end_y] = 0

    return maze, (start_x, start_y), (end_x, end_y)



def find_paths(maze, start, end):
    def dfs(x, y, path):
        if (x, y) == end:
            paths.append(path[:])
            return
        if (x, y) in visited:
            return
        visited.add((x, y))
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and maze[nx, ny] == 0:
                dfs(nx, ny, path + [(nx, ny)])
        visited.remove((x, y))

    paths = []
    visited = set()
    dfs(start[0], start[1], [start])
    return paths

def draw_maze(maze, start, end, cell_size=20, paths=[]):
    pygame.init()
    height, width = maze.shape
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    pygame.display.set_caption("Maze Visualization")
    clock = pygame.time.Clock()

    colors = {
        'wall': (0, 0, 0),
        'path': (255, 255, 255),
        'start': (0, 255, 0),
        'end': (255, 0, 0),
        'route': (0, 0, 255), 
        'extra_2': (255, 0, 255),
        'extra_3': (0, 255, 255)
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(colors['wall'])
        for y in range(height):
            for x in range(width):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                # Determine color based on cell value
                if maze[y, x] == 0:
                    color = colors['path']
                elif maze[y, x] == 1:
                    color = colors['wall']
                elif maze[y, x] == 2:
                    color = colors['extra_2']
                elif maze[y, x] == 3:
                    color = colors['extra_3']
                pygame.draw.rect(screen, color, rect)

        # Draw start and end positions
        for (sx, sy) in [start, end]:
            rect = pygame.Rect(sy * cell_size, sx * cell_size, cell_size, cell_size)
            color = colors['start'] if (sx, sy) == start else colors['end']
            pygame.draw.rect(screen, color, rect)

        # Draw all paths
        for path in paths:
            for (px, py) in path:
                rect = pygame.Rect(py * cell_size, px * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, colors['route'], rect)

        pygame.display.flip()
        clock.tick(10)

if __name__ == '__main__':
    height, breadth = 8, 8
    maze, start, end = generate_maze(height, breadth)
    paths = find_paths(maze, start, end)
    print(len(paths))
    draw_maze(maze, start, end, cell_size=20)