#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


class HashTable1:
    """
    Хеш-таблиця у якій колізії розв'язуються методом лінійного зондування
    """

    def __init__(self):
        """
        конструктор, ініціалізує таблицю
        """

        self.size = 11
        self.current_size = 0
        self.slots = [None] * self.size
        self.data = [None] * self.size

    def hash(self, key):
        """
        повертає хеш ключа
        :param key: ключ
        :return: хещ
        """

        return key % self.size

    def rehash(self, prevhash):
        """
        функція повторного хешування (лінійне зондування)
        :param prevhash: хеш ключа
        :return: новий хеш
        """
        return (prevhash + 1) % self.size

    def put(self, key, value):
        """
        Додає пару (ключ, значення) до хеш таблиці
        :param key: ключ
        :param value: значення
        """
        if self.current_size == self.size:
            raise IndexError

        tmp_hash = self.hash(key)
        if self.slots[tmp_hash] is None:
            self.slots[tmp_hash] = key  # якщо слот пустий - додаємо ключ в один список
            self.data[tmp_hash] = value  # значення - в інший
            self.current_size += 1

        elif self.slots[tmp_hash] == key:
            self.data[tmp_hash] = value  # якщо вже існує елемент з таким ключем, то міняємо тільки значення

        else:
            # якщо в слоті стоїть елемент з іншим ключем - шукаєм вільне місце методом лінійного
            # зондування
            next_hash = self.rehash(tmp_hash)
            while self.slots[next_hash] is not None and self.slots[next_hash] != key:
                next_hash = self.rehash(next_hash)

            if self.slots[next_hash] is None:
                self.slots[next_hash] = key  # якщо слот пустий - додаємо ключ в один список
                self.data[next_hash] = value  # значення - в інший
                self.current_size += 1
            else:
                self.data[next_hash] = value

    def get(self, key):
        """
        повертає значення за ключем
        :param key: ключ
        :return: значення
        """

        tmp_hash = self.hash(key)
        if self.slots[tmp_hash] is None:
            return None

        elif self.slots[tmp_hash] == key:
            return self.data[tmp_hash]
        else:
            next_hash = self.rehash(tmp_hash)
            while self.slots[next_hash] is not None and self.slots[next_hash] != key \
                    and next_hash != tmp_hash:

                next_hash = self.rehash(next_hash)
                if self.slots[next_hash] is None or next_hash == tmp_hash:
                    return None
                elif self.slots[next_hash] == key:
                    return self.data[next_hash]

    __setitem__ = put
    __getitem__ = get

    def __len__(self):
        return self.current_size

    def __contains__(self, item):
        return not self[item] is None

    def __str__(self):
        return "{}\n{}".format(self.slots, self.data)
