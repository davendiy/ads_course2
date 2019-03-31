#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import cgi
import matplotlib.pyplot as plt
import numpy as np
from structure import *

form = cgi.FieldStorage()


if COST in form or REVENUE in form:
    item_type = COST if COST in form else REVENUE
    diagram = DIAGRAM_COSTS if COST in form else DIAGRAM_REVENUES

    # отримуємо словник категорій {Name1: id1, ...}
    categories = name_dict(data_connector.get_categories(item_type))
    counter = {}

    # для кожної катеогорії обчислюємо суму
    for k, v in categories.items():
        counter[k] = data_connector.get_sum(item_type=item_type, Category_id=v)

    # будуємо гістограму (взято зі stackowerflow)
    labels, values = zip(*counter.items())

    indexes = np.arange(len(labels))
    width = 0.6

    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)

    plt.savefig(diagram)
    with open(DIAGRAM_PATTERN, 'r', encoding='utf-8') as file:
        page = file.read()

    print(change_html(page.format(type=item_type, diagram=diagram), mode=STRING_MODE))
