#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 11.03.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


class Person:

    def __init__(self, name, byear):
        self.name = name
        self.byear = byear

    def input(self):
        self.name = input('')
        self.byear = input('')

    def print(self):
        print(self.name, self.byear, end=' ')


class Citizen(Person):

    def __init__(self, name, byear, adress, debt):
        Person.__init__(self, name, byear)
        self.adress = adress
        self.debt = debt

    def input(self):
        Citizen.input(self)
        tmp1 = input('Вулиця: ')
        tmp2 = input("Будинок: ")
        tmp3 = input('Квартира')

        self.adress = (tmp1, tmp2, tmp3)
        self.debt = input("Борг")


class Build:

    def __init__(self, street, number, citizens: list):
        self.street = street
        self.number = number
        self.citizens = citizens

    def add_citizen(self, citizen: Citizen):
        self.citizens.append(citizen)

    def del_citizen(self, citizen: Citizen):
        self.citizens.remove(citizen)

    def debt(self):
        return sum(map(lambda a: a.debt, self.citizens))


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        n = int(file.readline())           # n - к-ть мешканців
        builds = {}                    # словник {назва будинку: об'єкт Build}
        for i in range(n):
            tmp_name = file.readline()
            tmp_byear = file.readline()    # зчитуємо дані кожного мешканця
            tmp_street = file.readline()
            tmp_number = file.readline()
            tmp_flat = file.readline()
            tmp_debt = file.readline()

            build_key = tmp_street + tmp_number   # формуємо назву будинку
            if build_key not in builds:          # додаємо будинок в словник, якщо його там ще нема
                builds[build_key] = Build(tmp_street, tmp_number, [])

            # створюємо нового мешканця і додаємо до будинку
            new_citizen = Citizen(tmp_name, tmp_byear, (tmp_street, tmp_number, tmp_flat), tmp_debt)
            builds[build_key].add_citizen(new_citizen)

        # виводимо будинок з макс заборгованістю
        print(max(map(lambda a: a.debt, builds.values())))
