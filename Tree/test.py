import pygame as pg
from datetime import datetime


def main():
    """Вызов всех фукций, по рисованию картины"""
    print("Старт главной функции")
    hour = what_time_is_it()
    draw_background(hour)
    draw_sky_elements(hour)
    draw_ground()
    draw_grass()
    draw_tree()
    draw_clouds()
    print("Финиш главной функции")


def what_time_is_it():
    """Запрос - который час, формат 24 часа"""
    current_time = datetime.now()
    current_pure_time = current_time.strftime("%X")
    hour = int(current_pure_time[:2])
    return hour


def draw_background(hour):
    """Рисуем фон неба, в зависимости от времени суток"""
    if hour > 6 and hour < 20:
        print("Рисуем голубой фон")
    elif hour > 0 and hour < 6 or hour > 20 and hour < 23:
        print("Рисуем чёрный фон")


def draw_sky_elements(hour):
    """Рисуем солнце или луну со звёздами, в зависимости от времени суток"""
    if hour > 6 and hour < 20:
        print("Рисуем Солнце")
    elif hour > 0 and hour < 6 or hour > 20 and hour < 23:
        print("Рисуем Луну и звёзды")


def draw_ground():
    """Рисуем землю"""
    print("Рисуем землю")


def draw_grass():
    """Рисуем траву на земле"""
    print("Рисуем траву на земле")


def draw_tree():
    """Рисуем дерево на траве"""
    print("Рисуем дерево на траве")


def draw_clouds():
    """Рисуем облака"""
    print("Рисуем облака")


if __name__ == "__main__":
    main()