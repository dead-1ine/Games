import sys
import pygame
import random


pygame.init()

WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# TODO: Rename above vars to upper case
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_dir = (0, -1)
apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    flash = False

    while True:
        handle_events()
        move_snake()

        if snake[0] == apple:
            grow_snake()
            move_apple()
        elif check_collision():
            break

        draw(screen, flash)
        clock.tick(10)  # 게임 속도 조절 (10 FPS)

        # 몸통 또는 벽에 충돌 시 뱀의 색상을 변경하고 잠시 멈춤
        if check_collision() or is_wall_collision():
            flash = True
            draw(screen, flash)
            pygame.display.flip()
            pygame.time.delay(500)
            flash = False

    pygame.quit()
    sys.exit()


def move_snake():
    global snake, snake_dir

    head_x, head_y = snake[0]
    dir_x, dir_y = snake_dir
    new_head = (head_x + dir_x, head_y + dir_y)
    snake.insert(0, new_head)
    snake.pop()


def grow_snake():
    global snake, snake_dir

    head_x, head_y = snake[0]
    dir_x, dir_y = snake_dir
    new_head = (head_x + dir_x, head_y + dir_y)
    snake.insert(0, new_head)


def move_apple():
    global apple

    apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))


def check_collision():
    global snake

    snake_head = snake[0]
    # 몸통과의 충돌 여부 확인
    if snake_head in snake[1:]:
        return True

    return is_wall_collision(snake_head)


def is_wall_collision(snake_head):
    x, y = snake_head

    # 벽과의 충돌 여부 확인
    if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
        return True

    return False


def draw(screen, flash=False):
    screen.fill(WHITE)

    for segment in snake:
        x, y = segment
        if flash:
            color = RED
        else:
            color = GREEN
        pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    ax, ay = apple
    pygame.draw.rect(screen, RED, pygame.Rect(ax * GRID_SIZE, ay * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()


def handle_events():
    global snake_dir

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, 1):
                snake_dir = (0, -1)
            if event.key == pygame.K_DOWN and snake_dir != (0, -1):
                snake_dir = (0, 1)
            if event.key == pygame.K_LEFT and snake_dir != (1, 0):
                snake_dir = (-1, 0)
            if event.key == pygame.K_RIGHT and snake_dir != (-1, 0):
                snake_dir = (1, 0)


if __name__ == '__main__':
    main()
