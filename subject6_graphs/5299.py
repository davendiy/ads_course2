#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# created: 24.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

NOT_VISIT = -1


class Node:
    """ Допоміжний клас - вузол деку """

    def __init__(self, item):
        """ Конструктор вузла деку

        :param item: Елемент деку
        """
        self.item = item  # поле, що містить елемент деку
        self.next = None  # наступний вузол
        self.prev = None  # попередній вузол


class Deque:
    """ Реалізує дек як рекурсивну структуру. """

    def __init__(self):
        """ Конструктор деку - Створює порожній дек.
        """
        self.mFront = None  # Посилання на перший елемент деку
        self.mBack = None   # Посилання на останній елемент деку

    def empty(self):
        """ Перевіряє чи дек порожній

        :return: True, якщо дек порожній
        """
        return self.mFront is None and self.mBack is None

    def appendleft(self, item):
        """ Додає елемент до початку деку

        :param item: елемент, що додається
        :return: None
        """
        node = Node(item)           # створюємо новий вузол деку
        node.mNext = self.mFront      # наступний вузол для нового - це елемент, який є першим
        if not self.empty():        # якщо додаємо до непорожнього деку
            self.mFront.mPrev = node  # новий вузол стає попереднім для першого
        else:
            self.mBack = node  # якщо додаємо до порожнього деку, новий вузол буде й останнім
        self.mFront = node     # новий вузол стає першим у деку

    def popleft(self):
        """ Повертає елемент з початку деку.

        :return: Перший елемент у деку
        """
        if self.empty():
            raise Exception('pop_front: Дек порожній')
        node = self.mFront       # node - перший вузол деку
        item = node.item        # запам'ятовуємо навантаження
        self.mFront = node.next  # першим стає наступний вузлом деку
        if self.mFront is None:  # якщо в деку був 1 елемент
            self.mBack = None    # дек стає порожнім
        else:
            self.mFront.prev = None  # інакше перший елемент посилається на None
        del node                    # Видаляємо вузол
        return item

    # методи append та pop повністю симетричні appendleft та popleft відповідно
    def append(self, item):
        """ Додає елемент у кінець деку

        :param item: елемент, що додається
        :return: None
        """
        elem = Node(item)
        elem.mPrev = self.mBack
        if not self.empty():
            self.mBack.mNext = elem
        else:
            self.mFront = elem
        self.mBack = elem

    def pop(self):
        """ Повертає елемент з кінця деку.

        :return: Останній елемент у деку
        """
        if self.empty():
            raise Exception('pop_back: Дек порожній')
        node = self.mBack
        item = node.item
        self.mBack = node.prev
        if self.mBack is None:
            self.mFront = None
        else:
            self.mBack.next = None
        del node
        return item

    def __del__(self):
        """ Деструктор - використовується для коректного видалення
            усіх елементів деку у разі видалення самого деку

        :return: None
        """
        while self.mFront is not None:  # проходимо по всіх елементах деку
            node = self.mFront  # запам'ятовуємо посилання на елемент
            self.mFront = self.mFront.next  # переходимо до наступного елементу
            del node  # видаляємо елемент
        self.mBack = None


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

        # Відтань - додаткове навантаження на вершину - величина найкоротшого шляху
        # від деякої фіксованої вершини до поточної вершини графа.
        # Використовується для хвильового алгоритму, алгоритмів Дейкстри, Белмана-Форда та ін.
        self.mDistance = NOT_VISIT  # До початку роботи алгортиму вважаємо, що вона є несінченністю!

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
        stack = Deque()
        current = end
        while True:
            stack.append(current)
            if current == start:
                break
            current = self[current].source()
            if current is None:
                return None

        way = []  # Послідовність вершин шляху
        while not stack.empty():
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

    # Відстань у старотовій вершині (тобто від стартової вершини до себе) визначається як 0
    graph[start].set_distance(0)

    q = Deque()       # Створюємо чергу
    q.appendleft(start)  # Додаємо у чергу початкову вершину

    while not q.empty():
        vertex_key = q.pop()   # Беремо перший елемент з черги
        vertex = graph[vertex_key]  # Беремо вершину за індексом

        # Для всіх сусідів (за ключами) поточної вершини
        for neighbor_key in vertex.neighbours():
            neighbour = graph[neighbor_key]   # Беремо вершину-сусіда за ключем
            if not neighbour.visited():       # Якщо сусід не був відвіданий
                q.appendleft(neighbor_key)       # додаємо його до черги
                neighbour.set_distance(vertex.distance() + 1)   # Встановлюємо значення відстані у вершині-сусіді
                # значенням на 1 більшии ніж у поточній вершині


def split(graph: Graph):
    count = 0
    for start in graph:        # type: VertexForAlgorithms
        if not start.visited():
            wave2(graph, start.key())
            max_distance = 0
            max_end = None
            for end in graph:     # type: VertexForAlgorithms
                if end.distance() > max_distance:
                    max_distance = end.distance()
                    max_end = end
                end.set_unvisited()

            if max_end is None:
                continue

            count += 1
            current = max_end
            while True:
                graph[current].set_distance(1)
                if current == start:
                    break
                current = graph[current].source()
                if current is None:
                    continue
    return count


if __name__ == '__main__':
    n, m = map(int, input().split())
    task = Graph()
    for i in range(1, n+1):
        task.addVertex(i)
    for i in range(m):
        task.addEdge(*map(int, input().split()))
    print(split(task))
