import numpy as np
import random

def generate_level(width, height, platform_density=0.2):
    """
    Генерирует массив уровня для платформера.
    :param width: ширина уровня
    :param height: высота уровня
    :param platform_density: плотность платформ
    :return: numpy-массив уровня
    """
    level = np.zeros((height, width), dtype=int)

    # Генерация платформ
    for y in range(height):
        for x in range(width):
            if y == height - 1:  # Дно уровня
                level[y, x] = 1
            elif random.random() < platform_density and y > 0:
                level[y, x] = 1

    # Удаляем "парящие" блоки
    for y in range(1, height):
        for x in range(width):
            if level[y, x] == 1 and level[y - 1, x] == 0 and random.random() < 0.5:
                level[y, x] = 0

    return level

def save_level_to_file(level, filename="level.txt"):
    """
    Сохраняет массив уровня в текстовый файл.
    :param level: numpy-массив уровня
    :param filename: имя файла
    """
    with open(filename, "w") as f:
        for row in level:
            f.write("".join(map(str, row)) + "\n")
    print(f"Уровень сохранён в {filename}")

# Пример использования
width = 20
height = 10
platform_density = 0.3

level = generate_level(width, height, platform_density)
save_level_to_file(level)

# Вывод уровня в консоль
print("\nСгенерированный уровень:")
for row in level:
    print("".join("X" if cell == 1 else "." for cell in row))
