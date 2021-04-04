import pygame as pg
import ctypes
import datetime
import random


# Получает разрешение экрана
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screensize_x, screensize_y = screensize

# Создаём главное окно в 2/3 от разрешения экрана пользователя
MAIN_WINDOW = pg.display.set_mode((round(screensize_x // 1.5), round(screensize_y // 1.5)))

# Задаём чистоту обновления экрана
FPS = 60
clock = pg.time.Clock()

# Задаём заголовок программы
pg.display.set_caption("Рисуем деверо!")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HARBOR_BLUE = (105, 160, 206)
DARK_GREY = (46, 46, 46)
SUNLIGHT = (253, 251, 211)
SUNLIGHT_2 = (249, 215, 28)
MOONLIGHT = (255, 247, 237)
EARTH_TONE = (87, 71, 30)
GREEN = (63, 155, 11)
GREEN_2 = (116, 176, 32)
NIGHT_GREEN_2 = (87, 133, 24)
PANTONE_367 = (164, 214, 94)
# WOOD_TONE = (101, 67, 33)

# Создаём список координат звёзд
coordinates_all_stars = []

# Создаём список координат облаков
coordinates_all_clouds = []

# Создаём список скорости передвижения облаков
velocity_clouds = []


def main():
    run = True

    while run:
        # Задаём чистоту обновления экрана
        clock.tick(FPS)

        # Прописываем выход из программы
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        # hour = 7
        hour = what_time_is_it()

        draw_background(hour)
        draw_sky_elements(hour)
        draw_ground()
        draw_grass(hour)
        draw_clouds()
        draw_tree()


        # Обновляем экран
        pg.display.update()


def what_time_is_it():
    """Запрос - который час, формат 24 часа"""
    current_time = datetime.datetime.now()
    current_pure_time = current_time.strftime("%X")
    hour = int(current_pure_time[:2])
    return hour


def draw_background(hour):
    """Рисуем фон неба, в зависимости от времени суток"""
    if hour >= 6 and hour <= 20:
        MAIN_WINDOW.fill(HARBOR_BLUE)
    elif hour > 0 and hour < 6 or hour > 20 and hour <= 23:
        MAIN_WINDOW.fill(DARK_GREY)


def draw_sky_elements(hour):
    """Рисуем солнце или луну со звёздами, в зависимости от времени суток"""
    if hour >= 6 and hour <= 20:
        pg.draw.circle(MAIN_WINDOW, SUNLIGHT_2, (round(screensize_x // 1.5 * 0.88), round(screensize_y // 1.5 * 0.18)), screensize_y // 13)
    elif hour > 0 and hour < 6 or hour > 20 and hour <= 23:
        if len(coordinates_all_stars) < 20:
            for i in range(random.randint(20, 33)):
                x = random.randint(0, round(screensize_x // 1.5))
                y = random.randint(0, round((screensize_y // 1.5) // 1.20))
                coordinates_all_stars.append([(x, y), (x + 10, y), (x + 3, y + 5), (x + 5, y - 5), (x + 8, y + 5)])
        for i in range(len(coordinates_all_stars)):
            pg.draw.aalines(MAIN_WINDOW, SUNLIGHT_2, True, coordinates_all_stars[i], )
        pg.draw.circle(MAIN_WINDOW, MOONLIGHT, (round(screensize_x // 1.5 * 0.88), round(screensize_y // 1.5 * 0.18)), screensize_y // 13)


def draw_ground():
    """Рисуем землю"""
    width_x, height_y = get_tree_size()
    indent_y = ((screensize_y // 1.5) - height_y) // 5
    pg.draw.rect(MAIN_WINDOW, EARTH_TONE, (0, round((screensize_y // 1.5) - indent_y), round(screensize_x // 1.5), indent_y))


def draw_grass(hour):
    """Рисуем траву на земле"""
    width_x, height_y = get_tree_size()
    indent_y = ((screensize_y // 1.5) - height_y) // 5
    if hour >= 6 and hour <= 20:
        pg.draw.rect(MAIN_WINDOW, GREEN_2, (0, round(screensize_y // 1.5) - indent_y - (indent_y // 5), screensize_x // 1.5, indent_y // 5))
    elif hour > 0 and hour < 6 or hour > 20 and hour <= 23:
        pg.draw.rect(MAIN_WINDOW, NIGHT_GREEN_2, (0, round(screensize_y // 1.5) - indent_y - (indent_y // 5), screensize_x // 1.5, indent_y // 5))


def draw_tree():
    """Добавляем рисунок дерева на траву"""
    tree = pg.image.load(r'sprite\tree_1.png') # Размер картинки 600*492
    scale = pg.transform.scale(tree, (round((screensize_x // 1.5) // 2.133), round((screensize_y // 1.5) // 1.463)))
    scale_width, scale_height = scale.get_size()
    width_x, height_y = get_tree_size()
    indent_y = ((screensize_y // 1.5) - height_y) // 5
    MAIN_WINDOW.blit(scale, ((screensize_x // 1.5) * 0.02, (screensize_y // 1.5) - scale_height - indent_y * 0.40))


def get_tree_size():
    """Получаем размер картинки "tree_1.png" в зависимости от размера главного окна"""
    tree = pg.image.load(r'sprite\tree_1.png')  # Размер оригинала картинки 600*492
    scale = pg.transform.scale(tree, (round((screensize_x // 1.5) // 2.133), round((screensize_y // 1.5) // 1.463)))
    scale_width, scale_height = scale.get_size()
    return scale_width, scale_height


def create_cloud():
    """Создаёт облака"""
    x = random.randint(screensize_x // 1.5, screensize_x + round(screensize_x // 1.5))
    y = random.randint(0, round((screensize_y // 1.5) // 2.5))
    coordinates_all_clouds.append((x, y))


def draw_clouds():
    """Рисуем облака"""
    cloud = pg.image.load(r'sprite\cloud_1.png') # Размер картинки 800*533
    scale = pg.transform.scale(cloud, (round((screensize_x // 1.5) // 8), round((screensize_y // 1.5) // 6)))

    # Проверяем количество облаков, добавляем не хватающих.
    if len(coordinates_all_clouds) < 10:
        create_cloud()

    # Отрисовываем все облака
    for cloud in coordinates_all_clouds:
        MAIN_WINDOW.blit(scale, cloud)

    # Задаём скорость для каждого облака
    for velocity in range(len(coordinates_all_clouds)):
        velocity_clouds.append(random.randint(1, 5))

    # Передвигаем облако по "x", заданной скоростью из списка velocity_clouds
    for i in range(len(coordinates_all_clouds)):
        x, y = coordinates_all_clouds[i]
        x -= velocity_clouds[i]
        coordinates_all_clouds.pop(i)
        coordinates_all_clouds.insert(0 + i, (x, y))


    # Проверяем вышло ли облако за границу экрана
    for i in range(len(coordinates_all_clouds)):
        x, y = coordinates_all_clouds[i]
        scale_width, _ = scale.get_size()
        if x < 0 - scale_width:
            coordinates_all_clouds.pop(i)
            create_cloud()


if __name__ == "__main__":
    main()
    pg.quit()



# # НЕ МУСОР
#
# # Заготовка дождя
# for i in range(random.randint(20, 35)):
#     x = random.randint(0, round(screensize_x // 1.5))
#     y = random.randint(0, round(screensize_y // 1.5))
#     coordinates_for_star = [(x, y), (x + 10, y), (x + 3, y + 5), (x + 5, y + 15), (x + 8, y + 25)]
#     pg.draw.aalines(MAIN_WINDOW, SUNLIGHT, True, coordinates_for_star)
#

