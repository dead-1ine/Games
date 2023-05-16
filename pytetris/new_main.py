import pygame
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 700
PLAY_WIDTH, PLAY_HEIGHT = 300, 600
TOP_LEFT_X = (WINDOW_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = WINDOW_HEIGHT - PLAY_HEIGHT - 50

BLOCK_SIZE = 30
BLOCK_SHAPES = [
    [[1, 1], [1, 1]],  # O
    [[1], [1], [1], [1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 0], [0, 1, 1]],  # S
    [[1, 0, 0], [1, 1, 1]],  # L
    [[1, 1, 1], [1, 0, 0]],  # J
]

BLOCK_COLORS = [
    (0, 255, 255),
    (255, 255, 0),
    (255, 0, 0),
    (0, 255, 0),
    (128, 0, 128),
    (255, 165, 0),
    (0, 0, 255),
]

score = 0

def main():
    pygame.font.init()
    pygame.display.set_caption('Tetris')
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    locked_positions = {}

    change_block = False
    run = True
    current_block = get_shape()
    next_block = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        fall_speed = 0.27
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_block.y += 1
            if not valid_space(current_block, grid) and current_block.y > 0:
                current_block.y -= 1
                change_block = True

        # keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_block.x -= 1
                    if not valid_space(current_block, grid):
                        current_block.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_block.x += 1
                    if not valid_space(current_block, grid):
                        current_block.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_block.y += 1
                    if not valid_space(current_block, grid):
                        current_block.y -= 1
                elif event.key == pygame.K_UP:
                    current_block.shape = rotate_block(current_block.shape)
                    if not valid_space(current_block, grid):
                        current_block.shape = rotate_block(current_block.shape)
                        current_block.shape = rotate_block(current_block.shape)
                        current_block.shape = rotate_block(current_block.shape)

        shape_pos = convert_shape_format(current_block)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_block.color

        if change_block:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_block.color
            current_block = next_block
            next_block = get_shape()
            change_block = False

            if check_lost(locked_positions):  # Check if player lost
                draw_text_middle(window, 'GAME OVER', 80, (255, 255, 255))
                pygame.display.update()
                pygame.time.delay(2000)
                run = False

            clear_rows(grid, locked_positions)

        draw_window(window, grid)

    pygame.quit()


class Block(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = BLOCK_COLORS[BLOCK_SHAPES.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid


def rotate_block(shape):
    return [list(x) for x in zip(*shape[::-1])]


def get_shape():
    return Block(5, 0, random.choice(BLOCK_SHAPES))


def draw_window(surface, grid):
    surface.fill((0, 0, 0))

    font = pygame.font.SysFont('comicsans', 50)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    surface.blit(label, (WINDOW_WIDTH - label.get_width() - 10, 10))

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (TOP_LEFT_X + x*BLOCK_SIZE, TOP_LEFT_Y + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)
    pygame.display.update()


def clear_rows(grid, locked):
    global score
    full_rows = []

    for y in range(len(grid)-1, -1, -1):
        full = True
        for x in range(len(grid[y])):
            if grid[y][x] == (0, 0, 0):
                full = False
                break

        if full:
            full_rows.append(y)
            for x in range(len(grid[y])):
                del locked[(x, y)]

    if full_rows:
        score += (len(full_rows) ** 2) * 10  # Increase score exponentially
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < min(full_rows):
                new_key = (x, y + len(full_rows))
                locked[new_key] = locked.pop(key)


def valid_space(block, grid):
    accepted_positions = [[(x, y) for x in range(10) if grid[y][x] == (0, 0, 0)] for y in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(block)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def convert_shape_format(block):
    positions = []
    shape_format = block.shape
    for y, line in enumerate(shape_format):
        row = list(line)
        for x, column in enumerate(row):
            if column == 1:
                positions.append((block.x + x, block.y + y))
    return positions


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (WINDOW_WIDTH/2 - (label.get_width()/2), WINDOW_HEIGHT/2 - label.get_height()/2))


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:  # If block reaches top
            return True
    return False


if __name__ == '__main__':
    main()
