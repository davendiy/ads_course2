#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 11.12.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from collections import deque

WALL_CELL = 'R'
START1 = 'g'
START2 = 'l'
END = 'e'


def readMazesFromFile(filename):
    tmp = ''
    with open(filename, 'r') as file:
        n = int(file.readline())
        for test in range(n):
            maze = []  # Створення порожньої матриці для задавання лабіринту
            while not tmp:
                tmp = file.readline()

            n1, m1 = map(int, tmp.split())
            start1 = (1, 1)
            start2 = (1, 1)
            end = (1, 1)
            i = 1
            while True:
                str_row = file.readline()
                if not str_row:
                    str_row = file.readline()
                if not str_row or str_row[0].isdigit():
                    tmp = str_row
                    break
                row = list(str_row.strip())
                if len(row) == 0:  # Захист від зайвих рядків у кінці файлу
                    break

                # додавання лівої та правої "стіни" лабіринту
                row.insert(0, WALL_CELL)
                row.append(WALL_CELL)

                if START1 in row:
                    start1 = (i, row.index(START1))
                if START2 in row:
                    start2 = (i, row.index(START2))
                if END in row:
                    end = (i, row.index(END))

                maze.append(row)  # додавання рядка до лабіринту

            rowLast = [WALL_CELL] * (n1 + 2)  # останній рядок матриці, що визначає нижню стіну
            maze.append(rowLast)
            yield maze, start1, start2, end


def task_wave(maze, start1, start2, end):
    """ Функція побудови хвильової матриці для лібіринту
    P4 зі стартовою точкою start
    wall_cell - символ, що позначає стіну лабіринта або непрохідну його клітину
    """
    dx = [-1, 0, 1, 0]
    dy = [0, -1, 0, 1]

    n = len(maze)  # кількість рядків у матриці P4
    m = len(maze[0])  # кількість стовпчиків у матриці P4

    # створення та ініціалізація хвильової матриці
    # такої ж розмірності, що і матриця лабіринту
    waveMatrix1 = [[-1 for i in range(m)] for i in range(n)]
    waveMatrix2 = [[-1 for i in range(m)] for i in range(n)]

    q = deque()  # Створюємо чергу
    q.appendleft((start2, 2))
    q.appendleft((start1, 1))  # Додаємо у чергу координати стартової клітини

    waveMatrix1[start1[0]][start1[1]] = 0  # Відстань від стартової клітини до себе нуль
    waveMatrix2[start2[0]][start2[1]] = 0
    while q:
        current = q.pop()  # Беремо перший елемент з черги
        i = current[0][0]  # координата поточного рядка матриці
        j = current[0][1]  # координата поточного стовчика матриці
        side = current[1]
        # Додаємо в чергу всі сусідні клітини
        for k in range(len(dx)):

            i1 = i + dy[k]  # координата рядка сусідньої клітини
            j1 = j + dx[k]  # координата стовпчика сусідньої клітини

            # які ще не були відвідані та у які можна пересуватися

            if waveMatrix1[i1][j1] == -1 and maze[i1][j1] != WALL_CELL and side == 1 and waveMatrix2[i1][j1] == -1:
                q.appendleft(((i1, j1), 1))
                # Встановлюємо відстань на одиницю більшу ніж для поточної
                waveMatrix1[i1][j1] = waveMatrix1[i][j] + 1

            if waveMatrix2[i1][j1] == -1 and maze[i1][j1] != WALL_CELL and side == 2 and maze[i1][j1] != END:
                q.appendleft(((i1, j1), 2))
                waveMatrix2[i1][j1] = waveMatrix2[i][j] + 1

    # print('\n-----------')
    # for row in waveMatrix1:
    #     tmp = ' '.join(map(str, row))
    #     print(tmp.replace('-1', '_'))
    # print()
    # for row in waveMatrix2:
    #     tmp = ' '.join(map(str, row))
    #     print(tmp.replace('-1', '_'))
    return waveMatrix1[end[0]][end[1]] != -1


if __name__ == '__main__':
    with open('output88.txt', 'w') as outfile:
        for tmp_maze, tmp_start1, tmp_start2, tmp_end in readMazesFromFile('input88.txt'):
            res = task_wave(tmp_maze, tmp_start1, tmp_start2, tmp_end)
            if res:
                outfile.write('YES\n')
            else:
                outfile.write('NO\n')
