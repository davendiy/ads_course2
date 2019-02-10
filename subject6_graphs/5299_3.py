#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 27.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


amount = 0


def try_kuhn(graph: list, vertex: int, used: list, mt: list):
    if used[vertex]:
        return False

    used[vertex] = True
    for i in range(len(graph[vertex])):
        to = graph[vertex][i]
        if mt[to] == -1:
            mt[to] = vertex
            global amount
            amount -= 1
            return True

        elif try_kuhn(graph, mt[to], used, mt):
            mt[to] = vertex
            return True
    return False


if __name__ == '__main__':
    try:
        n, m = map(int, input().split())
        task_mt = [-1 for i in range(m)]
        amount = n

        task_graph = [[] for i in range(n)]

        for i in range(m):
            tmp_from, tmp_to = map(int, input().split())
            task_graph[tmp_from-1].append(tmp_to-1)

        for i in range(n):
            task_used = [False for j in range(n)]
            try_kuhn(task_graph, i, task_used, task_mt)

        print(amount)
    except IndexError:
        print(amount)
