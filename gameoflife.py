import pygame
import sys
import random
import argparse, textwrap

alive_color = (255, 255, 255)  # white
dead_color = (0, 0, 0)         # black
grid_color = (40, 40, 40)      # grey grid during editing

# 2D grid 
def make_grid(width, height):
    return [[0 for x in range(width)] for y in range(height)]

# Random start
def populate_grid_random(grid, density):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if random.random() < density:
                grid[y][x] = 1

def count_live_neighbor_cells(grid, x, y, grid_width, grid_height):
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
def step(grid, grid_width, grid_height):
    new_grid = make_grid(grid_width, grid_height)

    for y in range(grid_height):
        for x in range(grid_width):
            neighbors = count_live_neighbor_cells(grid, x, y, grid_width, grid_height)

            if grid[y][x] == 1:
                # survival
                if neighbors == 2 or neighbors == 3:
                    new_grid[y][x] = 1
            else:
                # birth
                if neighbors == 3:
                    new_grid[y][x] = 1

    return new_grid

def main(grid_width, grid_height, cell_size, fps, editing, density):
    
    clock = pygame.time.Clock()
    grid = make_grid(grid_width, grid_height)

    if not editing and density is not None:
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

            if editing:
                if event.type == pygame.MOUSEBUTTONDOWN: # Mouse button to toggle cells in editing phase
                    mouse_x, mouse_y = event.pos

                    x = mouse_x // cell_size
                    y = mouse_y // cell_size

                    if 0 <= x < grid_width and 0 <= y < grid_height:
                        grid[y][x] = 0 if grid[y][x] == 1 else 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        editing = False

        if not editing:
            grid = step(grid, grid_width, grid_height)

        screen.fill(dead_color)
        
        if editing: # Draw grid while editing
            # vertical lines
            for x in range(0, window_width, cell_size):
                pygame.draw.line(screen, grid_color, (x, 0), (x, window_height))

            # horizontal lines
            for y in range(0, window_height, cell_size):
                pygame.draw.line(screen, grid_color, (0, y), (window_width, y))

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

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="How to use The Game Of Life",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
        python3 gameoflife.py -W 600 -H 350 -s 10
        ''')
    )

    parser.add_argument('-W', '--width', type=int, default=300, help="Grid width")
    parser.add_argument('-H', '--height', type=int, default=300, help="Grid height")
    parser.add_argument('-r', '--random', type=float, help="Fill starting grid randomly with a density between 0 and 1")
    parser.add_argument('-s', '--speed', type=int, default=10, help="Iterations per second")
    parser.add_argument('-c', '--cellsize', type=int, default=8, help="Cell size in pixels")

    args = parser.parse_args()

    # determine starting mode
    if args.random is None:
        editing = True
        density = None
    else:
        editing = False
        density = args.random

    main(
        grid_width=args.width,
        grid_height=args.height,
        cell_size=args.cellsize,
        fps=args.speed,
        editing=editing,
        density=density
    )
