from random import randint

import pygame as pg

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock: pg.time.Clock = pg.time.Clock()


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
        pass


class Apple(GameObject):
    """
    Apple — класс, унаследованный от GameObject, описывающий яблоко и действия
    с ним. Яблоко должно отображаться в случайных клетках игрового поля.
    """

    def __init__(self, body_color: COLOR = APPLE_COLOR):
        """
        Задаёт цвет яблока и вызывает метод randomize_position, чтобы
        установить начальную позицию яблока.
        """
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self) -> None:
        """
        Устанавливает случайное положение яблока на игровом поле — задаёт
        атрибуту position новое значение. Координаты выбираются так,
        чтобы яблоко оказалось в пределах игрового поля.
        """
        width: int = randint(0, GRID_WIDTH)
        height: int = randint(0, GRID_HEIGHT)
        while (width * GRID_SIZE, height * GRID_SIZE) in Snake().positions:
            width = randint(0, GRID_WIDTH - 1)
            height = randint(0, GRID_HEIGHT - 1)
        
        self.position = (width * GRID_SIZE, height * GRID_SIZE)

    def draw(self) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Snake — класс, унаследованный от GameObject, описывающий змейку и её
    поведение. Этот класс управляет её движением, отрисовкой,
    а также обрабатывает действия пользователя.
    """

    def __init__(self, body_color: COLOR = SNAKE_COLOR):
        """Инициализирует начальное состояние змейки."""
        super().__init__(body_color = body_color)
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
        head: tuple[int, int] = self.get_head_position()
        width, height = head
        new_width: int = (width + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH
        new_height: int = (height + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT
        new_head: tuple[int, int] = (new_width, new_height)

        if self.length == len(self.positions):
            self.positions.insert(0, new_head)
            self.last = self.positions[-1]
            self.positions.pop()
        else:
            self.positions.insert(0, new_head)
            self.last = None

        if new_head in self.positions[1:]:
            self.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self) -> None:
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]


def handle_keys(game_object) -> None:
    """Обрабатывает нажатия клавиш, чтобы менять направление змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """
    В основном цикле игры (в функции main) происходит обновление состояний
    объектов: змейка обрабатывает нажатия клавиш и двигается в соответствии
    с выбранным направлением.
    """
    # Инициализация PyGame:
    pg.init()

    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        apple.draw()
        snake.move()
        snake.draw()
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position()
        handle_keys(snake)
        snake.update_direction()
        pg.display.update()


if __name__ == '__main__':
    main()
