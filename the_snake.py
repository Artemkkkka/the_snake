from random import randint
from typing import Optional

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
POINTER = tuple[int, int]
UP: POINTER = (0, -1)
DOWN: POINTER = (0, 1)
LEFT: POINTER = (-1, 0)
RIGHT: POINTER = (1, 0)

# Цвет фона - черный:
COLOR = tuple[int, int, int]
BOARD_BACKGROUND_COLOR: COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock: pygame.time.Clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    GameObject — это базовый класс, от которого наследуются другие игровые
    объекты. Он содержит общие атрибуты игровых объектов — например, эти
    атрибуты описывают позицию и цвет объекта. Этот же класс содержит и
    заготовку метода для отрисовки объекта на игровом поле — draw.
    """

    def __init__(self, body_color: COLOR = BOARD_BACKGROUND_COLOR):
        """
        Инициализирует базовые атрибуты объекта, такие как
        его позиция и цвет.
        """
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self) -> None:
        """
        Это абстрактный метод, который предназначен для переопределения в
        дочерних классах. Этот метод должен определять, как объект будет
        отрисовываться на экране. По умолчанию — pass.
        """


class Apple(GameObject):
    """
    Apple — класс, унаследованный от GameObject, описывающий яблоко и действия
    с ним. Яблоко должно отображаться в случайных клетках игрового поля.
    """

    def __init__(
            self,
            snake_position: list[tuple[int, int]] = [
                ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
            ],
            body_color: COLOR = APPLE_COLOR
    ):
        """
        Задаёт цвет яблока и вызывает метод randomize_position, чтобы
        установить начальную позицию яблока.
        """
        super().__init__(body_color=body_color)
        self.snake_position = snake_position
        self.randomize_position(self.snake_position)

    def randomize_position(self, snake_position) -> None:
        """
        Устанавливает случайное положение яблока на игровом поле — задаёт
        атрибуту position новое значение. Координаты выбираются так,
        чтобы яблоко оказалось в пределах игрового поля.
        """
        max_width = GRID_WIDTH - 1
        max_height = GRID_HEIGHT - 1
        while True:
            width = randint(0, max_width) * GRID_SIZE
            height = randint(0, max_height) * GRID_SIZE
            if (
                width, height
            ) not in snake_position:
                self.position = (width, height)
                return

    def draw(self) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Snake — класс, унаследованный от GameObject, описывающий змейку и её
    поведение. Этот класс управляет её движением, отрисовкой,
    а также обрабатывает действия пользователя.
    """

    def __init__(self, body_color: COLOR = SNAKE_COLOR):
        """Инициализирует начальное состояние змейки."""
        super().__init__(body_color=body_color)
        self.length: int = 1
        self.positions: list[tuple[int, int]] = [self.position]
        self.direction: POINTER = RIGHT
        self.next_direction: Optional[POINTER] = None
        self.last: Optional[tuple[int, int]] = None

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Обновляет позицию змейки, учитывая границы поля."""
        width, height = self.get_head_position()
        new_head: tuple[int, int] = (
            (width + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH,
            (height + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT
        )

        if self.length == len(self.positions):
            self.last = self.positions[-1]
            self.positions.pop()
        else:
            self.last = None

        self.positions.insert(0, new_head)

    def draw(self) -> None:
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]


def handle_keys(game_object) -> None:
    """Обрабатывает нажатия клавиш, чтобы менять направление змейки."""
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


def main() -> None:
    """
    В основном цикле игры (в функции main) происходит обновление состояний
    объектов: змейка обрабатывает нажатия клавиш и двигается в соответствии
    с выбранным направлением.
    """
    # Инициализация PyGame:
    pygame.init()

    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)

        apple.draw()
        snake.move()
        snake.draw()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position(snake.positions)
        snake.update_direction()
        handle_keys(snake)
        pygame.display.update()


if __name__ == '__main__':
    main()
