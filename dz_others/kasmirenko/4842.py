#!/usr/bin/env python3
# -*-encoding: utf-8-*-


def right_insert(given_list: list, value):
    """
    функція, яка вставляє елемент у впорядкований список
    :param given_list: список елементів
    :param value: значення елемента, який треба вставити
    """
    i = 0
    n1 = len(given_list)
    # проходимо по елеменах токи їх значення менші, ніж даний елемент
    while i < n1 and given_list[i] < value:
        i += 1

    # вставляємо даний елемент після останнього меншого
    given_list.insert(i, value)


def rotate(given_dict: dict):
    """
    перевертання словника
    значення стають ключами, а ключі - значеннями

    :param given_dict: словник {ключ - список значень}
    :return: новий словник
    """
    res = {}

    # проходимо по всіх ключах і списках значень словника
    for key, value in given_dict.items():
        # проходимо по всіх значеннях у списку значень
        for v in value:

            # для кожного або створюємо новий запис у результуючому словнику,
            # або впорядковано додаємо до існуючого
            if v not in res.keys():
                res[v] = [key]
            else:
                right_insert(res[v], key)
    return res


if __name__ == '__main__':
    # test_dict = {}         # англо-латинський словник
    #
    # # зчитування
    # while True:
    #     line = input()       # зчитаний рядок, який перевіряємо на непорожність
    #     if not line:
    #         break
    #     line = line.strip().split(' - ')   # розбиваємо рядок по дефісам
    #     line[1] = line[1].split(', ')      # а праву частину результату розбиваємо по комам
    #     test_dict[line[0]] = line[1]       # додаємо новий запис до словника
    #
    # rez = rotate(test_dict)       # перевертаємо і впорядковано виводим
    # print(len(rez))
    # for el in sorted(rez.keys()):
    #     print('{} - {}'.format(el, ', '.join(rez[el])))

    test_dict = {}
    with open('input.txt', 'r') as file:
        for line in file:
            line = line.strip().split(' - ')  # розбиваємо рядок по дефісам
            line[1] = line[1].split(', ')  # а праву частину результату розбиваємо по комам
            test_dict[line[0]] = line[1]  # додаємо новий запис до словника

    rez = rotate(test_dict)
    with open("output.txt", 'w') as outfile:
        outfile.write(str(len(rez)))
        outfile.write('\n')
        for el in sorted(rez.keys()):
            outfile.write('{} - {}\n'.format(el, ', '.join(rez[el])))
