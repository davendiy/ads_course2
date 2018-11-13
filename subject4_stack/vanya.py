#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


class Stack_min:

    def __init__(self):
        self.data = []
        self.min = 10**10
        self.min_lst = []

    def push(self,item):
        if self.min >= item:
            self.min = item
            self.min_lst.append(self.min)
        return self.data.append(item)

    def pop(self):
        if len(self.data) == 0:
            raise Exception("Stack: 'pop' applied to empty container")
        else:
            if self.min == self.data.pop(-1):
                self.min = self.min_lst[len(self.min_lst) - 2]
        return self.data

    def minim(self):
        if len(self.data) == 0:
            raise Exception("Stack: 'minim' applied to empty container")
        else:
            return self.min



def task():
    s = Stack_min()
    res = []
    with open("input.txt", 'r') as file:
        data = file.readlines()[1:]
        for d in data:
            d = d.split()
            if d[0] == '1':
                s.push(int(d[1]))
            elif d[0] == '2':
                s.pop()
            else:
                res.append(s.minim())

    with open('output.txt', 'w') as file:
        for r in res:
            file.write(str(r) + "\n")



if __name__ == "__main__":
    task()


# def task():
#     res = []
#     mins = []
#     inf = []
#     min = 10**10
#     with open("input.txt", 'r') as file:
#         data = file.readlines()[1:]
#         for d in data:
#             d = d.split()
#             if d[0] == '1':
#                 if min >= int(d[1]):
#                     min = int(d[1])
#                     mins.append(min)
#                 inf.append(int(d[1]))
#             elif d[0] == '2':
#                 if len(inf) > 0:
#                     if mins[-1] == inf.pop():
#                         mins.pop()
#                         min = mins[-1]
#                 else:
#                     raise Exception('Error cant pop from len == 0')
#             else:
#                 res.append(min)
#
#     with open('output.txt', 'w') as file:
#         for r in res:
#             file.write(str(r) + "\n")
#
#
#
# if __name__ == "__main__":
#     task()