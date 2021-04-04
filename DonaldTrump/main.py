# Имоптируем бибилотеку с сокращением
import pygame as pg

# Инициируем библиотеку
pg.init()


# Рисуем главное окно и анимированного персонажа
def draw_main_window():
    global animation_counter, FPS

    MAIN_WINDOW.blit(bg, (0, 0))

    if animation_counter + 1 >= FPS:
        animation_counter = 0

    if left:
        MAIN_WINDOW.blit(walk_left[animation_counter // fps_to_pic_ratio], (x, y))
        animation_counter += 1
    elif right:
        MAIN_WINDOW.blit(walk_right[animation_counter // fps_to_pic_ratio], (x, y))
        animation_counter += 1
    else:
        MAIN_WINDOW.blit(player_stand, (x, y))

    for bullet in bullets:
        bullet.draw(MAIN_WINDOW)

    for enemy in enemies:
        if enemy.side == 0:
            enemy.draw_right(MAIN_WINDOW)
        elif enemy.side == 1:
            enemy.draw_left(MAIN_WINDOW)

    pg.display.update()  # обновляем экран


# Устанавливаем размер окна
MAIN_WINDOW = pg.display.set_mode((500, 500))

# Получаем размерны окна
MAIN_WINDOW_SIZE = pg.display.get_window_size()

# Заголовок
pg.display.set_caption("Donald Trump")

# Размеры персонажа
width = 60
height = 71

# Смещение персонажа в пикселях.
move_rect = 5

# Отступ персонажа от краёв окна
x = MAIN_WINDOW_SIZE[0] // 2 - width // 2
y = MAIN_WINDOW_SIZE[1] - height - move_rect

# Запоминаем начальную точку
home = abs(x), abs(y)

# Добавляем возможность прыгать
is_jump = False
jump_count = 10

# Переменные для анимации персонажа
move_left = False
move_right = False
animation_counter = 0
last_move = 'right'

# Частота обновления экрана (FPS)
FPS = 60
clock = pg.time.Clock()

# Добавляем фон
bg = pg.image.load("bg.jpg")

# Добавляем картинки персонажа
player_stand = pg.image.load(r"sprite\idle.png")

walk_right = [
    pg.image.load(r"sprite\right_1.png"),
    pg.image.load(r"sprite\right_2.png"),
    pg.image.load(r"sprite\right_3.png"),
    pg.image.load(r"sprite\right_4.png"),
    pg.image.load(r"sprite\right_5.png"),
    pg.image.load(r"sprite\right_6.png"),
]

walk_left = [
    pg.image.load(r"sprite\left_1.png"),
    pg.image.load(r"sprite\left_2.png"),
    pg.image.load(r"sprite\left_3.png"),
    pg.image.load(r"sprite\left_4.png"),
    pg.image.load(r"sprite\left_5.png"),
    pg.image.load(r"sprite\left_6.png"),
]

# Добавляем картинки врагов
black_player_stand = pg.image.load(r"sprite\black_idle.png")

black_walk_right = [
    pg.image.load(r"sprite\black_right_1.png"),
    pg.image.load(r"sprite\black_right_2.png"),
    pg.image.load(r"sprite\black_right_3.png"),
    pg.image.load(r"sprite\black_right_4.png"),
    pg.image.load(r"sprite\black_right_5.png"),
    pg.image.load(r"sprite\black_right_6.png"),
]

black_walk_left = [
    pg.image.load(r"sprite\black_left_1.png"),
    pg.image.load(r"sprite\black_left_2.png"),
    pg.image.load(r"sprite\black_left_3.png"),
    pg.image.load(r"sprite\black_left_4.png"),
    pg.image.load(r"sprite\black_left_5.png"),
    pg.image.load(r"sprite\black_left_6.png"),
]

# Создаём зависимость частоты обновления экрана (FPS) от количества картинок для анимации
fps_to_pic_ratio = FPS // len(walk_left)


# Наш снаряд
class Ammo():

    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 8 * facing

    def draw(self, MAIN_WINDOW):
        pg.draw.circle(MAIN_WINDOW, self.color, (self.x, self.y - 3),
                       self.radius)  # добавил -3 пикселя к y, чтобы выглядело, что он изорта стреляет.


#  Наши противники
class Enemy():

    def __init__(self, side):
        self.side = side
        self.width = width
        self.height = height
        if self.side == 0:
            self.facing = 1  # движение слева направо
            self.x = -self.width
            self.y = MAIN_WINDOW_SIZE[1] - self.height - move_rect
        else:
            self.facing = -1  # движение справа налево
            self.x = MAIN_WINDOW_SIZE[0]
            self.y = MAIN_WINDOW_SIZE[1] - self.height - move_rect
        self.velocity = 2 * self.facing
        self.animation_counter_for_black_Trump = 0

    def draw_left(self, MAIN_WINDOW):
        if self.animation_counter_for_black_Trump + 1 >= FPS:
            self.animation_counter_for_black_Trump = 0
        MAIN_WINDOW.blit(black_walk_left[self.animation_counter_for_black_Trump // fps_to_pic_ratio], (self.x, self.y))
        self.animation_counter_for_black_Trump += 1

    def draw_right(self, MAIN_WINDOW):
        if self.animation_counter_for_black_Trump + 1 >= FPS:
            self.animation_counter_for_black_Trump = 0
        MAIN_WINDOW.blit(black_walk_right[self.animation_counter_for_black_Trump // fps_to_pic_ratio], (self.x, self.y))
        self.animation_counter_for_black_Trump += 1


# Запуск программы
run = True
bullets = []
enemies = []

while run:
    # FPS Устанавливем частоту кадров в секунду
    clock.tick(FPS)

    # Прописываем выход из программы
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # Проверяем куда смотрел персонаж
                if last_move == 'right':
                    facing = 1
                else:
                    facing = -1

                # Рисуем снаряд
                bullets.append(Ammo(round(x + width // 2), round(y + height // 2), 5, (255, 215, 0), facing))

    # Перемещаем снаряд по горизонтали и проверяем не покинул ли он границ
    for bullet in bullets:
        if bullet.x > 0 or bullet.x < MAIN_WINDOW_SIZE[0]:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))

    # Добавляем врагов
    if len(enemies) < 3:
        enemies.append(Enemy(0))
        enemies.append(Enemy(1))

    # Перемещаем врагов по горизонтали и проверяем не покинул ли он границ
    for enemy in enemies:
        if enemy.x >= 0 - enemy.width and enemy.x <= MAIN_WINDOW_SIZE[0]:
            enemy.x += enemy.velocity
        else:
            enemies.pop(enemies.index(enemy))
        for bullet in bullets:
            if bullet.x + bullet.radius // 2 in range(enemy.x, enemy.x + enemy.width // 2) \
                    and bullet.y + bullet.radius // 2 in range(enemy.y, enemy.y + enemy.height):
                enemies.pop(enemies.index(enemy))
                bullets.pop(bullets.index(bullet))

    # Прописываем управление
    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT] and x > move_rect:
        x -= move_rect
        left = True
        right = False
        last_move = 'left'

    elif keys[pg.K_RIGHT] and x < (MAIN_WINDOW_SIZE[0] - width - move_rect):
        x += move_rect
        left = False
        right = True
        last_move = 'right'
    else:
        left = False
        right = False
        animation_counter = 0

    # Проверяем не находимся ли мы в прыжке, иначе переходим в else.
    if not is_jump:
        if keys[pg.K_HOME]:
            x, y = home

        # Активируем прыжок
        if keys[pg.K_UP]:
            is_jump = True
    else:
        if jump_count <= -11:
            is_jump = False
            jump_count = 10
        elif jump_count <= 10 and jump_count >= 0:
            y -= (jump_count ** 2) / 2
            jump_count -= 1
        elif jump_count >= -10 or jump_count < 0:
            y += (jump_count ** 2) / 2
            jump_count -= 1

    draw_main_window()

pg.quit()
