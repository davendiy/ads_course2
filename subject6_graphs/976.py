#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 08.12.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


INF = 100050000


def floyd(adj_matrix):
    """ Алгоритм Флойда-Уоршела, видозмінений для
    знаходження циклів від'ємної ваги

    :param adj_matrix: матриця суміжності графа, в якій INF означає, що шляху нема
    :return: змінена матриця суміжності
    """
    n = len(adj_matrix)
    for i in range(n):
        adj_matrix[i][i] = 0      # на діагональні мають стояти нулі, це критично для алгоритму

    for k in range(n):
        for i in range(n):        # класичний алгоритм Флойда-Уоршела з поправкою на ребра від'ємної довжини
            for j in range(n):
                # щоб уникнути ситуації, коли алгоритм буде присваювати вершині
                # значення INF-1, INF-2 і тп. робимо додаткову перевірку
                # на відсутність шляху
                if adj_matrix[i][k] < INF and adj_matrix[k][j] < INF:
                    tmp = adj_matrix[i][k] + adj_matrix[k][j]
                    if tmp < -INF:           # при наявності циклу від'ємної довжини значення найкоротшого
                        tmp = -INF           # шляху може експоненційно зменшуватись, тому робимо обмеження
                    adj_matrix[i][j] = min(adj_matrix[i][j], tmp)

    for i in range(n):            # перевірка наявності циклів від'ємної довжини
        for j in range(n):
            # після роботи алгоритму Флойда-Уоршела на діагоналях буде від'ємне число, якщо
            # вершина належить до циклу від'ємної довжини, тому достатньо перевірити,
            # чи існує шлях від кожної вершини до вершини, яка належить до циклу від'ємної довжини
            for t in range(n):
                if adj_matrix[i][t] < INF and adj_matrix[t][t] < 0 and adj_matrix[t][j] < INF:
                    adj_matrix[i][j] = -INF

    return adj_matrix


def transform(element: int):
    """ Перетворює результуючу матрицю у
    вигляд, який вимагає e-olymp

    :param element: елемент матриці
    :return: відповідний рядок
    """
    if element == INF:
        res = '0'
    elif element == -INF:
        res = '2'
    else:
        res = '1'
    return res


if __name__ == '__main__':

    with open('input.txt', 'r') as file:
        test_n = int(file.readline())           # зчитування
        test_matrix = []
        for i2 in range(test_n):
            line = file.readline()
            tmp_line = line.split()
            tmp_line = list(map(lambda a: int(a) if a != '0' else INF, tmp_line))
            test_matrix.append(tmp_line)

    test_matrix = floyd(test_matrix)

    with open('output.txt', 'w') as file:       # вивід
        for row in test_matrix:
            file.write(' '.join(map(transform, row)))
            file.write('\n')
