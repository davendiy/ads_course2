#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 08.12.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from collections import deque

WALL_CELL = '#'     # символ, який позначає стіну
START_CELL = 'S'    # символ, який позначає стартову точку
END_CELL = 'E'      # символ, який позначає кінцеву точку
WAVE_NOT_VISITED = -1    # символ, який позначає не відвідану точку в хвильовій матриці
WAVE_VISITED = 1         # символ, який позначає відвідану точку в хвильовій матриці


def task(filename_in='input.txt', filename_out='output.txt'):
    """ Реалізація зчитування з файлу тривімірного лабіринта у тому вигляді,
    який вимагає e-olymp

    :param filename_in: файл введення
    :param filename_out: файл виведення
    """
    start_coord = (1, 1, 1)    # дефолтні координати початку і кінця
    end_coord = (1, 1, 1)

    outfile = open(filename_out, 'w')
    with open(filename_in, 'r') as file:
        params = file.readline()           # параметри лабіринту

        # в одному файлі тестів декілька, тому проводимо процедуру поки параметри не нульові
        while '0 0 0' not in params:
            x, y, z = map(int, params.split())
            # заготовка лабіринту з зовнішніми стінами
            maze = [[[WALL_CELL] * (z + 2) for i in range(y + 2)] for i in range(x + 2)]

            for i in range(1, x + 1):
                for j in range(1, y + 1):               # зчитка лабіринту з заданими параметрами
                    tmp_line = file.readline().strip()
                    while not tmp_line:                 # пропускаємо пусті рядки
                        tmp_line = file.readline().strip()
                    tmp_line = WALL_CELL + tmp_line + WALL_CELL   # додаємо зовнішні стіни

                    if START_CELL in tmp_line:          # перевірка наявності стартової і кінцевої точок
                        start_coord = (i, j, tmp_line.index(START_CELL))
                    if END_CELL in tmp_line:
                        end_coord = (i, j, tmp_line.index(END_CELL))
                    maze[i][j] = list(tmp_line)

            result = wave(maze, start_coord, end_coord)   # запуск хвильового алгоритму
            if result == WAVE_NOT_VISITED:
                outfile.write('Trapped!\n')               # виведення результату у файл
            else:
                outfile.write('Escaped in {} minute(s).\n'.format(result))

            params = file.readline().strip()
            while not params:                             # зчитування нових параметрів
                params = file.readline()
    outfile.close()


def wave(maze, start, end):
    """ Реалізація хвильового алгоритму для 3-вимірного лабіринту

    :param maze: 3-вимірний масив
    :param start: кортеж з 3-х елементів (початкова точка)
    :param end: кортеж з 3-х елементів  (кінцева точка)
    :return: хвильова матриця
    """
    dx = [-1, 0, 0, 1, 0, 0]
    dy = [0, -1, 0, 0, 1, 0]      # 3-вимірний випадок
    dz = [0, 0, -1, 0, 0, 1]

    x = len(maze)
    y = len(maze[0])
    z = len(maze[0][0])

    # хвильова матриця
    wave_matrix = [[[WAVE_NOT_VISITED] * (z) for i in range(y)] for i in range(x)]
    q = deque()      # замість черги використовуємо встроєний дек
    q.appendleft(start)
    wave_matrix[start[0]][start[1]][start[2]] = 0

    while q:               # далі все аналогічно
        current = q.pop()
        i, j, k = current

        for tmp_dx, tmp_dy, tmp_dz in zip(dx, dy, dz):
            next_i = i + tmp_dx
            next_j = j + tmp_dy
            next_k = k + tmp_dz

            if wave_matrix[next_i][next_j][next_k] == WAVE_NOT_VISITED and \
                    maze[next_i][next_j][next_k] != WALL_CELL:
                q.appendleft((next_i, next_j, next_k))
                wave_matrix[next_i][next_j][next_k] = wave_matrix[i][j][k] + 1

    return wave_matrix[end[0]][end[1]][end[2]]


if __name__ == '__main__':
    task()
