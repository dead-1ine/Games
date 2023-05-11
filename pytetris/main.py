import pygame
import random

pygame.font.init()

# Set window size
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 700
PLAY_WIDTH, PLAY_HEIGHT = 300, 600

TOP_LEFT_X = (WINDOW_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = WINDOW_HEIGHT - PLAY_HEIGHT - 50

# Set blocks
BLOCK_SIZE = 30
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 0], [0, 1, 1]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [1, 1, 1, 1, 1]],  # +
    [[1, 1, 0], [1, 1, 1]],  # L
    [[0, 1, 1], [1, 1, 0], [0, 1, 1]],  # X
]

# 색상 설정
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

# index 0 - 7 represent shape
class Piece(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = SHAPES_COLOR[SHAPES.index(shape)]