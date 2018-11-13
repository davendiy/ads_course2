#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


def step(parent, par_count, outfile, now_index, max_count, index):
    """
    крок алгоритма
    :param parent: символ дужки
    :param par_count: к-ть відкритих дужок
    :param outfile: файл виведення
    :param now_index: к-ть магічних дужок, останній індекс
    :param max_count: максимальна к-ть магічних дужок
    :param index: нинішній індекс в рядку
    :return: змінені параметри, або False
    """
    success = True

    if parent == '(':
        par_count += 1
    elif parent == ')' and par_count > 0:
        par_count -= 1
    elif parent == ']' and par_count > 0 and now_index < max_count - 1:
        outfile.write('1\n')
        now_index += 1
        par_count -= 1
    elif parent == ']' and par_count > 0 and now_index == max_count - 1:
        tmp = par_count - string.count(')', index)
        out_file.write(str(tmp) + '\n')
        par_count -= tmp
        now_index += 1
    else:
        success = False

    return (par_count, now_index) if success else None


# def simplify(parents):
#     res = parents[:]
#     for i in range(len(parents) - 1):
#         if parents[i] == ')':
#             for j in range(i, -1, -1):
#                 if res[j] == '(':
#                     res = res[:j] + ' ' + res[j+1:]
#                     break
#             else:
#                 break
#             res = res[:i] + ' ' + res[i+1:]
#     return res


if __name__ == '__main__':
    success_balance = 1
    with open('output.txt', 'w') as out_file:
        out_file.write('1\n')
        curr_count = 0
        end_index = 0
        with open('input.txt', 'r') as file:
            head = file.readline().split()
            n, m = int(head[0]), int(head[1])
            count_par = 0
            string = file.read()

        # string = simplify(string)
        for index, tmp_symb in enumerate(string):
            if tmp_symb == '\n':
                continue
            tmp_res = step(tmp_symb, curr_count, out_file, end_index, m, index)

            if tmp_res is None:
                success_balance = 0
                break

            curr_count, end_index = tmp_res
            if curr_count < 0:
                success_balance = 0
                break

            if end_index == m:
                break

    if success_balance == 0:
        with open('outfile.txt', 'w') as file:
            file.write('0')
