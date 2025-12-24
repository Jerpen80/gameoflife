import pygame
import sys
import random

cell_size = 5      
grid_width = 200
grid_height = 200

# RNG Density, float between 0 and 1
density = 0.09

alive_color = (255, 255, 255)  # white
dead_color = (0, 0, 0)         # black

# Reduce game speed
clock = pygame.time.Clock()
fps = 10

# 2D grid 
def make_grid(width, height):
    return [[0 for x in range(width)] for y in range(height)]

# Random start
def populate_grid_random(grid, density):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if random.random() < density:
                grid[y][x] = 1

# TODO: Allow user to determine startinmg position

def count_live_neighbor_cells(grid, x, y):
    count = 0
    # delta (changing) x and y
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue  # skip the cell itself
            # neighbors
            nx = x + dx
            ny = y + dy

            if 0 <= nx < grid_width and 0 <= ny < grid_height:
                count += grid[ny][nx]

    return count

# Apply the game of life logic:
def step(grid):
    new_grid = make_grid(grid_width, grid_height)

    for y in range(grid_height):
        for x in range(grid_width):
            neighbors = count_live_neighbor_cells(grid, x, y)

            if grid[y][x] == 1:
                # survival
                if neighbors == 2 or neighbors == 3:
                    new_grid[y][x] = 1
            else:
                # birth
                if neighbors == 3:
                    new_grid[y][x] = 1

    return new_grid


grid = make_grid(grid_width, grid_height)
populate_grid_random(grid, density)
pygame.init()

window_width = grid_width * cell_size
window_height = grid_height * cell_size

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Game of Life")

# start:
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    grid = step(grid)

    screen.fill(dead_color)

    # draw grid
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] == 1:
                rect = pygame.Rect(
                    x * cell_size,
                    y * cell_size,
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(screen, alive_color, rect)

    pygame.display.flip()
    clock.tick(fps)


pygame.quit()
sys.exit()
