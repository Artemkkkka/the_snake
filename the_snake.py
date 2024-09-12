from random import choice, randint
from typing import Optional

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, position: Optional[tuple] = None, body_color=None):
        self.position = position if position else (320, 240)
        self.body_color = body_color

    def draw(self):
        pass

class Snake(GameObject):
    def __init__(self, length=1, positions=[(320, 240)], direction=RIGHT, next_direction=None):
        super().__init__(positions[-1], SNAKE_COLOR)
        self.length = length
        self.positions = positions
        self.direction = direction
        self.next_direction = next_direction

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        if self.direction == UP:
            new_head = (self.positions[0][0], self.positions[0][1] - GRID_SIZE)
        elif self.direction == DOWN:
            new_head = (self.positions[0][0], self.positions[0][1] + GRID_SIZE)
        elif self.direction == LEFT:
            new_head = (self.positions[0][0] - GRID_SIZE, self.positions[0][1])
        elif self.direction == RIGHT:
            new_head = (self.positions[0][0] + GRID_SIZE, self.positions[0][1])

        self.positions.insert(0, new_head)
        self.positions.pop()

    def draw(self):
        screen.fill(BOARD_BACKGROUND_COLOR)
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if len(self.positions) > 1:
            last_rect = pygame.Rect(self.positions[-1], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.positions = [(320, 240)]
        self.direction = RIGHT


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE, randint(0, GRID_HEIGHT) * GRID_SIZE)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

def main():
    """
    Основной цикл игры.
    """
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        apple.draw()

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка столкновения с самим собой
        if snake.get_head_position() in snake.positions[:-1]:
            snake.reset()

        snake.draw()
        pygame.display.update()

if __name__ == '__main__':
    main()
