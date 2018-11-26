#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 25.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from collections import deque

NOT_VISIT = -1


class VertexForAlgorithms:
    """ Клас, що є розширенням класу для вершини графа

        Використовується у алгоритмах Белмана-Форда, Дейкстри, А*...
        Міститть додаткову технічну інформацію, що необхідна для реалізації щих алгоритмів
     """

    def __init__(self, key):
        """ Конструктор створення вершини

        :param key: Ключ вершини
        """
        self.mKey = key
        self.mData = None
        self.mNeighbours = {}
        self.mVisited = False
        # Відтань - додаткове навантаження на вершину - величина найкоротшого шляху
        # від деякої фіксованої вершини до поточної вершини графа.
        # Використовується для хвильового алгоритму, алгоритмів Дейкстри, Белмана-Форда та ін.
        self.mDistance = NOT_VISIT  # До початку роботи алгортиму вважаємо, що вона є несінченністю!
        self.mOrderIn = 0

        # Джерело - додаткове навантаження на вершину -
        # вершина з якої прийшли по найкорошому шляху
        # у поточну вернишу на деякому кроці алгоритму
        self.mSource = None  # До початку роботи алгортиму вважаємо, що вона є невизначеною

    def key(self):
        return self.mKey

    def data(self):
        return self.mData

    def setData(self, data):
        self.mData = data

    def addNeighbour(self, vertex, weight=1):
        if isinstance(vertex, VertexForAlgorithms):
            self.mNeighbours[vertex.key()] = weight
        else:
            self.mNeighbours[vertex] = weight

    def neighbours(self):
        return self.mNeighbours.keys()

    def weight(self, neighbour):
        if isinstance(neighbour, VertexForAlgorithms):
            return self.mNeighbours[neighbour.key()]
        else:
            return self.mNeighbours[neighbour]

    def set_distance(self, distance):
        """ Встановлює відстань для поточної вершини

        :param distance: Нова відстань
        :return: None
        """
        self.mDistance = distance

    def distance(self):
        """ Повератє поточну відстань у вершині)

        :return: Відстань у вершині
        """
        return self.mDistance

    def set_source(self, source):
        """ Встанолює джерело для поточної вершини

        :param source: Нове джерело вершини
        :return: None
        """
        self.mSource = source

    def source(self):
        """ Повертає джерело для поточної вершини

        :return: Джерело поточної вершини
        """
        return self.mSource

    def visited(self):
        """ Чи відвідана вершина на поточному кроці алгоритму
        Якщо вершина була принаймні один раз відвідана, то відстань у ній менша за нескінченність

        :return: True, якщо вершина була відвідана на поточному кроці алгоритму
        """
        return self.mDistance != NOT_VISIT

    def set_unvisited(self):
        """ Встановлює відстань у поточній вершині як нескінченність

        :return: None
        """
        self.mDistance = NOT_VISIT

    def __str__(self):
        """ Зображення вершини у вигляді рядка у разом з усіма її сусідами """
        return str(self.mKey) + ": Data = " + str(self.data()) + "  Dist = " + str(self.mDistance) + "  From: " \
               + str(self.mSource) + ' connected: ' + str(self.mNeighbours)
        # return str(self.mId) + ": Data=" + str(self.getData())


class Graph:

    def __init__(self, oriented=False):
        self.mIsOriented = oriented
        self.mVertexNumber = 0
        self.mVertices = {}

    def getVertex(self, vertex):
        vertex = vertex.key() if isinstance(vertex, VertexForAlgorithms) else vertex
        return self.mVertices.get(vertex, None)

    def vertices(self):
        return self.mVertices

    def addEdge(self, source, destination, weight=1):
        if source not in self:
            self.addVertex(source)
        if destination not in self:
            self.addVertex(destination)

        self.getVertex(source).addNeighbour(destination, weight)

        if not self.mIsOriented:
            self[destination].addNeighbour(source, weight)
        self[destination].mOrderIn += 1

    def inverse(self):
        g_inv = Graph(self.mIsOriented)
        for vertex in self:
            for neighbour_key in vertex.neighbours():
                g_inv.addEdge(neighbour_key, vertex.key())
        return g_inv

    def __contains__(self, vertex):
        if isinstance(vertex, VertexForAlgorithms):
            return vertex.key() in self.mVertices
        else:
            return vertex in self.mVertices

    def __iter__(self):
        return iter(self.mVertices.values())

    def __len__(self):
        return self.mVertexNumber

    def __str__(self):
        """ Зображення графа разом з усіма вершинами і ребрами у вигляді рядка """
        s = ""
        for vertex in self:
            s = s + str(vertex) + "\n"
        return s

    def __getitem__(self, vertex):
        return self.getVertex(vertex)

    def addVertex(self, vertex) -> bool:
        """ Додає вершину у граф, якщо така вершина не міститься у ньому

        :param vertex: ключ (тобто ім'я) нової вершини
        :return: True, якщо вершина успішно додана
        """

        if vertex in self:  # Якщо вершина міститься у графі, її вже не треба додавати
            return False

        new_vertex = VertexForAlgorithms(vertex)  # створюємо нову вершину з іменем key
        self.mVertices[vertex] = new_vertex       # додаємо цю вершину до списку вершин графу
        self.mVertexNumber += 1                   # Збільшуємо лічильник вершин у графі
        return True

    def construct_way(self, start, end):
        """ Домопіжний метод, що будує шлях, між двома вершинами у графі
        Може бути застосовами лише після дії алгоритмів пошуку шляху
        (Хвильового, Дейкстри, Беллмана-Форда, тощо) які записують
        допоміжну інформацію у вершини графа.

        :param start: Вершина, що початком шляху
        :param end: Вершина, що є кінцем шляху
        :return: Кортеж, що містить список вершин - найкоротший шлях, що сполучає вершини start та end та його вагу
        """

        if self[end].source is None:  # шляху не існує
            return None, NOT_VISIT

        # будуємо шлях за допомогою стеку
        stack = deque()
        current = end
        while True:
            stack.append(current)
            if current == start:
                break
            current = self[current].source()
            if current is None:
                return None

        way = []  # Послідовність вершин шляху
        while stack:
            way.append(stack.pop())

        # Повертаємо шлях та його вагу
        return way, self[end].distance()


def wave2(graph: Graph, start: int):

    """ Функція, що запускає хвильовий алгоритм.
        Використовує граф класу GraphForAlgorithms, вершини якого містять допоміжну інформацію.
        Функція модифікує вхідний граф, так, що в результаті його всі вершини
        містять інформацію про найкоротшу відстань від заданої стартової вершини.

    :param graph: Граф, вершини якого містять відстань від початкової вершини
    :param start: Стартова вершина, тобто з якої починається робота хвильового алгоритму
    :return: None
    """

    # # Ініціалізуємо додаткову інформацію у графі для роботи алгоритму.
    # for vertex in graph:
    #     vertex.set_unvisited()   # вершина ще не була відвідана

    # Відстань у стартовій вершині (тобто від стартової вершини до себе) визначається як 0
    graph[start].set_distance(0)

    q = deque()       # Створюємо чергу
    q.appendleft(start)  # Додаємо у чергу початкову вершину
    ends = {}
    while q:
        vertex_key = q.pop()   # Беремо перший елемент з черги
        vertex = graph[vertex_key]  # Беремо вершину за індексом

        # Для всіх сусідів (за ключами) поточної вершини
        for neighbor_key in vertex.neighbours():
            neighbour = graph[neighbor_key]   # Беремо вершину-сусіда за ключем
            if (neighbour.distance() < vertex.distance() + 1 or neighbour.distance() == -1) \
                    and not neighbour.mVisited:       # Якщо сусід не був відвіданий
                q.appendleft(neighbor_key)       # додаємо його до черги
                neighbour.set_distance(vertex.distance() + 1)   # Встановлюємо значення відстані у вершині-сусіді
                neighbour.mSource = vertex_key                     # значенням на 1 більшии ніж у поточній вершині
        if not vertex.neighbours():
            ends[vertex_key] = vertex
    return ends


def split2(graph: Graph):
    count = 0
    not_visited = {}
    for start in graph:

        if start.mOrderIn > 0:
            not_visited[start.key()] = start
            continue

        if not start.mVisited:
            ends = wave2(graph, start.key())
            max_distance = -1
            max_end = None
            for end in ends.values():
                if end.distance() > max_distance:
                    max_distance = end.distance()
                    max_end = end
                if end.distance() > -1:
                    end.set_distance(-1)

            count += 1
            current = max_end.key()
            while True:
                graph[current].mVisited = True
                if current in not_visited:
                    del not_visited[current]
                if graph[current] == start:
                    break

                current = graph[current].source()
                if current is None:
                    break

    for start in not_visited.values():

        if not start.mVisited:
            ends = wave2(graph, start.key())
            max_distance = -1
            max_end = None
            for end in ends.values():
                if end.distance() > max_distance:
                    max_distance = end.distance()
                    max_end = end

                if end.distance() > -1:
                    end.set_distance(-1)

            count += 1
            current = max_end
            while True:
                graph[current].mVisited = True
                if graph[current] == start:
                    break

                current = graph[current].source()
                if current is None:
                    break

    return count


if __name__ == '__main__':
    n, m = map(int, input().split())
    task = Graph(oriented=True)
    for i in range(1, n+1):
        task.addVertex(i)
    for i in range(m):
        task.addEdge(*map(int, input().split()))
    print(split2(task))

    # task = Graph(oriented=True)
    # with open('input5299.txt', 'r') as file:
    #     n, m = map(int, file.readline().split())
    #     for i in range(1, n+1):
    #         task.addVertex(i)
    #     for line in file:
    #         task.addEdge(*map(int, line.split()))
    #
    # print(split2(task))
