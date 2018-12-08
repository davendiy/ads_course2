#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 05.12.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com
tasks = int(input())
for mini_task in range(tasks):
    s = input().split()
    n, m = int(s[0]), int(s[1])
    l = []
    x, y = -1, -1
    xe, ye = -1, -1
    cost = list(map(lambda x: int(x), input().split()))
    for i in range(n):
        buff = []
        k = input()
        if x == -1:
            y, x = i, k.find('S')
        if xe == -1:
            ye, xe = i, k.find('E')
        for j in k:
            buff.append(j)
        l.append(buff)

    keys = [['', 0], ['R', cost[0]], ['G', cost[1]], ['B', cost[2]], ['Y', cost[3]], ['RG', cost[0] + cost[1]],
            ['RB', cost[0] + cost[2]], ['RY', cost[0] + cost[3]], ['GB', cost[1] + cost[2]], ['GY', cost[1] + cost[3]],
            ['BY', cost[2] + cost[3]], ['RGB', cost[0] + cost[1] + cost[2]], ['RGY', cost[0] + cost[1] + cost[3]],
            ['RBY', cost[0] + cost[2] + cost[3]], ['GBY', cost[1] + cost[2] + cost[3]], ['RGBY', sum(cost)]]
    # keys = ['G']
    keys.sort(key=lambda x: x[1])
    way = [False, '']

    for key in keys:
        hl = [[-1 for i in range(m)] for j in range(n)]
        hl[y][x] = 1
        indexes = [[y, x]]
        for i in range(n * m + 1):
            buff = []
            for j in indexes:
                if 0 <= j[1] + 1 < m and (l[j[0]][j[1] + 1] == '.' or key[0].find(l[j[0]][j[1] + 1]) != -1 or
                                          l[j[0]][j[1] + 1] == 'E') and hl[j[0]][j[1] + 1] == -1:
                    hl[j[0]][j[1] + 1] = hl[j[0]][j[1]] + 1
                    buff.append([j[0], j[1] + 1])
                if 0 <= j[1] - 1 < m and (l[j[0]][j[1] - 1] == '.' or key[0].find(l[j[0]][j[1] - 1]) != -1 or
                                          l[j[0]][j[1] - 1] == 'E') and hl[j[0]][
                    j[1] - 1] == -1:
                    hl[j[0]][j[1] - 1] = hl[j[0]][j[1]] + 1
                    buff.append([j[0], j[1] - 1])
                if 0 <= j[0] + 1 < n and (l[j[0] + 1][j[1]] == '.' or key[0].find(l[j[0] + 1][j[1]]) != -1 or
                                          l[j[0] + 1][j[1]] == 'E') and hl[j[0] + 1][
                    j[1]] == -1:
                    hl[j[0] + 1][j[1]] = hl[j[0]][j[1]] + 1
                    buff.append([j[0] + 1, j[1]])
                if 0 <= j[0] - 1 < n and (l[j[0] - 1][j[1]] == '.' or key[0].find(l[j[0] - 1][j[1]]) != -1 or
                                          l[j[0] - 1][j[1]] == 'E') and hl[j[0] - 1][j[1]] == -1:
                    hl[j[0] - 1][j[1]] = hl[j[0]][j[1]] + 1
                    buff.append([j[0] - 1, j[1]])
                if j == [ye, xe]:
                    way = [True, key[1]]
                    break
            indexes = buff
            if way[0]:
                break
        if way[0]:
            break

    if way[0]:
        print(way[1])
    else:
        print('Sleep')