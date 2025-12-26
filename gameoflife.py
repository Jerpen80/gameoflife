import pygame
import sys
import random
import argparse, textwrap

alive_color = (255, 255, 255)  # white
dead_color = (0, 0, 0)         # black
grid_color = (40, 40, 40)      # grey grid during editing

# 2D grid of zeroes
def make_grid(width, height):
    return [[0 for x in range(width)] for y in range(height)]

# Random start
def populate_grid_random(grid, density):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if random.random() < density:
                grid[y][x] = 1

# Count neighbouring alive cells
def count_live_neighbor_cells(grid, x, y, grid_width, grid_height):
    count = 0
    # Count how many of its 8 surrounding neighbors are alive where (0,0) is the cell itself:
    # (-1,-1) (0,-1) (1,-1)
    # (-1, 0) (0, 0) (1, 0)
    # (-1, 1) (0, 1) (1, 1)

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            # skip the cell itself
            if dx == 0 and dy == 0:
                continue
            # convert relative offsets into absolute grid positions
            nx = x + dx
            ny = y + dy
            # prevent accessing invalid positions (beyond grid edges)
            if 0 <= nx < grid_width and 0 <= ny < grid_height:
                # Add all alive neighbours (dead = 0, alive = 1)
                count += grid[ny][nx]
    return count

# detect if chunks contain live cells, or we can skip them
def active_chunks_from_grid(grid, grid_width, grid_height, chunk_size):
    active = set()
    for y in range(grid_height):
        row = grid[y]
        for x in range(grid_width):
            if row[x] == 1:
                active.add((x // chunk_size, y // chunk_size))
    return active

def expand_active_chunks(active):
    # active: set of (chunk_x, chunk_y)
    expanded = set()
    for chunk_x, chunk_y in active:
        for offset_x in (-1, 0, 1):
            for offset_y in (-1, 0, 1):
                expanded.add((chunk_x + offset_x, chunk_y + offset_y))
    return expanded


def iterate_chunk_cells(chunk_x, chunk_y, chunk_size, grid_width, grid_height):
    x0 = chunk_x * chunk_size
    y0 = chunk_y * chunk_size

    # keep within grid bounds (also handles negative chunk coords safely)
    x_start = max(0, x0)
    y_start = max(0, y0)
    x_end = min(grid_width,  x0 + chunk_size)
    y_end = min(grid_height, y0 + chunk_size)

    # if chunk is outside grid, yield nothing
    if x_start >= x_end or y_start >= y_end:
        return

    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            # return one coordinate at a time
            yield x, y

# Apply the game of life logic:
def step(grid, grid_width, grid_height, active, chunk_size):
    active = active_chunks_from_grid(grid, grid_width, grid_height, chunk_size)
    new_grid = make_grid(grid_width, grid_height)

    # evaluate also neighbors of active chunks
    expanded = expand_active_chunks(active)

    # 2) Evaluate only those cells
    for chunk_x, chunk_y in expanded:
        for x, y in iterate_chunk_cells(chunk_x, chunk_y, chunk_size, grid_width, grid_height):

            neighbors = count_live_neighbor_cells(grid, x, y, grid_width, grid_height)

            if grid[y][x] == 1:
                if neighbors in (2, 3):
                    new_grid[y][x] = 1
            else:
                if neighbors == 3:
                    new_grid[y][x] = 1

    # 3) Rebuild active chunks for next frame (correct + simple)
    new_active = active_chunks_from_grid(new_grid, grid_width, grid_height, chunk_size)
    return new_grid, new_active


def main(grid_width, grid_height, cell_size, fps, mode, density):
    
    offset_x = 0
    offset_y = 0
    # SCROLL_SPEED: ammount of pixels to shift with arrow key presses
    SCROLL_SPEED = 40

    chunk_size = 32

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
    window_width, window_height = screen.get_size()
    
    # Fullscreen if x and y are 0 or less
    if grid_width <= 0 or grid_height <= 0:
        grid_width = window_width // cell_size
        grid_height = window_height // cell_size

    grid = make_grid(grid_width, grid_height)

    if density is not None:
        populate_grid_random(grid, density)

    # create set of active chunks, chunks with alive cells
    active = active_chunks_from_grid(grid, grid_width, grid_height, chunk_size)

    # Init pygame
    pygame.init()

    # start:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # keyboard controls (always)
            if event.type == pygame.KEYDOWN:
                
                # Escape to quit
                if event.key == pygame.K_ESCAPE:
                    running = False

                # shifting pixels with arrow keys relative to current position
                elif event.key == pygame.K_LEFT:
                    offset_x -= SCROLL_SPEED
                elif event.key == pygame.K_RIGHT:
                    offset_x += SCROLL_SPEED
                elif event.key == pygame.K_UP:
                    offset_y -= SCROLL_SPEED
                elif event.key == pygame.K_DOWN:
                     offset_y += SCROLL_SPEED

                elif event.key == pygame.K_SPACE:
                    if mode == "EDIT":
                        mode = "RUN"
                    elif mode == "RUN":
                        mode = "PAUSE"
                    elif mode == "PAUSE":
                        mode = "RUN"

                elif event.key == pygame.K_n:
                    if mode == "EDIT":
                        mode = "PAUSE"

                    grid, active = step(grid, grid_width, grid_height, active, chunk_size)

                max_offset_x = grid_width * cell_size - window_width
                max_offset_y = grid_height * cell_size - window_height

                # Prevent camera from scrolling past edge of the grid
                offset_x = max(0, min(max_offset_x, offset_x))
                offset_y = max(0, min(max_offset_y, offset_y))

            # Mouse controls (EDIT only)
            if mode == "EDIT" and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                x = (mouse_x + offset_x) // cell_size
                y = (mouse_y + offset_y) // cell_size

                if 0 <= x < grid_width and 0 <= y < grid_height:
                    grid[y][x] = 0 if grid[y][x] == 1 else 1

                active = active_chunks_from_grid(grid, grid_width, grid_height, chunk_size)

        # Update simulation once per frame (RUN only)
        if mode == "RUN":
            grid, active = step(grid, grid_width, grid_height, active, chunk_size)

        # Start with empty screen (dead cells)
        screen.fill(dead_color)

        if mode == "EDIT":
            for x in range(0, window_width, cell_size):
                pygame.draw.line(screen, grid_color, (x, 0), (x, window_height))
            for y in range(0, window_height, cell_size):
                pygame.draw.line(screen, grid_color, (0, y), (window_width, y))

        for y in range(grid_height):
            for x in range(grid_width):
                if grid[y][x] == 1:
                    pygame.draw.rect(
                        screen,
                        alive_color,
                        (
                            # prevent mouse offset caused by scrolling with arrow keys
                            x * cell_size - offset_x,
                            y * cell_size - offset_y,
                            cell_size,
                            cell_size
                        )
                    )

        pygame.display.flip()
        # untie gamespeed and editing speed
        clock.tick(fps if mode == "RUN" else 30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="How to use The Game Of Life",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
        python3 gameoflife.py -x 600 -y 350 -c 20 -s 10
        ''')
    )

    parser.add_argument('-x', '--width', type=int, default=0, help="Number of cells x axis, 0 for full screen")
    parser.add_argument('-y', '--height', type=int, default=0, help="Number of cells y axis, 0 for full screen")
    parser.add_argument('-r', '--random', type=float, help="Fill starting grid randomly with a density between 0 and 1")
    parser.add_argument('-s', '--speed', type=int, default=10, help="Iterations per second")
    parser.add_argument('-c', '--cellsize', type=int, default=8, help="Cell size in pixels")

    args = parser.parse_args()

    # determine starting mode
    if args.random is None:
        mode = "EDIT"
        density = None
    else:
        mode = "PAUSE"
        density = args.random

    main(
        grid_width=args.width,
        grid_height=args.height,
        cell_size=args.cellsize,
        fps=args.speed,
        mode=mode,
        density=density
    )
