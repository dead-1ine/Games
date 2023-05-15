import pygame
import random


# Set window size
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 700
PLAY_WIDTH, PLAY_HEIGHT = 300, 600

TOP_LEFT_X = (WINDOW_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = WINDOW_HEIGHT - PLAY_HEIGHT - 50

# Set blocks
BLOCK_SIZE = 30
SHAPES = [
    [[1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 0], [0, 1, 1]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [0, 1, 0], [1, 1, 1]],  # +
    [[1, 1, 0], [1, 1, 1]],  # L
    [[0, 1, 1], [1, 1, 0], [0, 1, 1]],  # X
]

SHAPES_COLOR = [
    (0, 255, 255),  # I
    (255, 255, 0),  # O
    (255, 0, 0),  # Z
    (0, 255, 0),  # S
    (128, 0, 128),  # T
    (255, 165, 0),  # +
    (0, 0, 255),  # L
    (128, 128, 128),  # X
]


def main():
    pygame.font.init()
    pygame.display.set_caption('Tetris')
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        fall_speed = 0.27
        grid = create_grid(locked_positions)

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1  # TODO
                    current_piece.shape = rotate(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1  # TODO
                        current_piece.shape = rotate(current_piece.shape)
                        current_piece.shape = rotate(current_piece.shape)
                        current_piece.shape = rotate(current_piece.shape)

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            clear_rows(grid, locked_positions)

        draw_window(window, grid)

    pygame.quit()


class Piece(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = SHAPES_COLOR[SHAPES.index(shape)]
        self.rotation = 0  # TODO


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color

    return grid


def rotate(shape):
    return [list(x) for x in zip(*shape[::-1])]


def get_shape():
    return Piece(5, 0, random.choice(SHAPES))


def draw_window(surface, grid):
    surface.fill((0, 0, 0))

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (TOP_LEFT_X + x*BLOCK_SIZE, TOP_LEFT_Y + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)
    pygame.display.update()


def clear_rows(grid, locked):
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
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < min(full_rows):
                new_key = (x, y + len(full_rows))
                locked[new_key] = locked.pop(key)


def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(10) if grid[y][x] == (0, 0, 0)] for y in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape

    for y, line in enumerate(shape_format):
        row = list(line)
        for x, column in enumerate(row):
            if column == 1:
                positions.append((piece.x + x, piece.y + y))

    return positions


if __name__ == '__main__':
    main()