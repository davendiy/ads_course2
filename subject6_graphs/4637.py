#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 04.12.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

m, n, k = map(int, input().split())
res = [{} for x in range(n)]
max_values = [0 for x in range(n)]
pre_max_values = [0 for x in range(n)]
pre_res = [{} for x in range(n)]

for i in range(m):
    for j, tmp_value in enumerate(input().split()):
        tmp_value = int(tmp_value)
        if i == 0 and j == 0:
            res[j] = {tmp_value: 1}
            max_values[j] = tmp_value
        elif i == 0:
            for key, value in res[j - 1].items():
                res[j][key + tmp_value] = value
            max_values[j] = max_values[j-1] + tmp_value
        elif j == 0:
            for key, value in pre_res[j].items():
                res[j][key+tmp_value] = value
            max_values[j] = pre_max_values[j] + tmp_value
        else:
            max_values[j] = max(max_values[j-1], pre_max_values[j])
            for key, value in pre_res[j].items():
                if max_values[j] - key <= k and key + tmp_value in res[j]:
                    res[j][key+tmp_value] += value
                elif max_values[j] - key <= k:
                    res[j][key+tmp_value] = value

            for key, value in res[j-1].items():
                if max_values[j] - key <= k and key + tmp_value in res[j]:
                    res[j][key + tmp_value] += value
                elif max_values[j] - key <= k:
                    res[j][key + tmp_value] = value

            max_values[j] += tmp_value
    pre_res = res
    res = [{} for x in range(n)]
    pre_max_values = max_values
    max_values = [0 for x in range(n)]
print(pre_max_values[n-1], sum(pre_res[n-1].values()), sep='\n')
