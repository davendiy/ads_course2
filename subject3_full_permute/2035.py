#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


def task_input():

    with open('input.txt', 'r', encoding='utf-8') as inp_file:
        n = int(inp_file.readline())
        dictionary = []
        messages = []
        for i, line in enumerate(inp_file):
            if i < n:
                dictionary.append(line.strip())
            else:
                messages.append(line.strip())
    return dictionary, messages


def create_answer(message, scheme):

    if len(scheme) == 0:
        result = ''
        for letter in message:
            if letter != ' ':
                result += '*'
            else:
                result += ' '
    else:
        result = ''
        for letter in message:
            result += scheme[letter]
    return result


def test_string(message: str, dictionary: list):

    tmp_string = list(set(message.split()))
    result = [''] * len(dictionary)
    if len(tmp_string) > len(dictionary):
        result = create_answer(message, {})
    else:
        scheme = {' ': ' '}
        flag = test_sets(tmp_string, dictionary, result, scheme)
        if flag:
            result = create_answer(message, scheme)
        else:
            result = create_answer(message, {})
    return result


def test_sets(message, dictionary, result, scheme):

    flag1 = False
    tmp_element = message.pop(0)

    for i in range(len(dictionary)):
        if result[i] != '' or len(tmp_element) != len(dictionary[i]):
            continue
        flag2, change = test_words(tmp_element, dictionary, scheme, i)
        if not flag2:
            for letter in change:
                del scheme[letter]
            continue
        elif flag2 and len(message) == 0:
            result[i] = tmp_element
            return True

        result[i] = tmp_element
        recursive_flag = test_sets(message, dictionary, result, scheme)

        if not recursive_flag:
            result[i] = ''
            for letter in change:
                del scheme[letter]
        else:
            flag1 = True
            break
    message.insert(0, tmp_element)
    return flag1


def test_words(word, dictionary, scheme, index):
    change = ''
    flag = True
    if len(word) != len(dictionary[index]):
        return False, ''

    for j, letter in enumerate(word):
        tmp_image = scheme.get(letter, None)
        if tmp_image != dictionary[index][j] and tmp_image is not None:
            flag = False
            break
        elif tmp_image is None:
            scheme[letter] = dictionary[index][j]
            change += letter
    return flag, change


if __name__ == '__main__':
    test_dictionary, test_messages = task_input()
    with open('output.txt', 'w', encoding='utf-8') as file:
        for tmp_message in test_messages:
            res = test_string(tmp_message, test_dictionary)
            file.write(res + '\n')
