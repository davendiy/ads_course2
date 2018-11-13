import numpy as np
import matplotlib.pyplot as plt
from math import sin

# from numpy import sin

# стилі ліній
styles = ['-', '--', '-.', ':', '.', ',',
          'o', 'v', '^', '<', '>',
          '1', '2', '3', '4',
          's', 'p', '*', 'h', 'H',
          '+', 'x', 'D', 'd', '|', '_']

# кольори ліній
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']


def gety(f, x):
    """Повертає значення функції f для всіх точок з x
    """
    try:
        y = f(x)
    except Exception as e:
        print('Exception handling', e)
        n = x.size
        y = np.zeros(n)
        for i in range(n):
            y[i] = f(x[i])
    return y


def tabulate(f, a, b, n):
    """Табулює функцію f на інтервалі [a,b] у n точках
    """
    x = np.linspace(a, b, n)
    y = gety(f, x)
    return x, y


def fun(x):
    """x**3 - 7*x - 1
    """
    return x**3 - 7*x - 1


def movespinesticks():
    """
    Перемістити осі у нульову позицію
    """
    ax = plt.gca()  # отримати поточний об'єкт класу axes
    # зробити праву та верхню осі невидимими:
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    # перенести нижню вісь у позицію y=0:
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    # перенести ліву вісь у позицію x == 0:
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))


def plotfunc4(a, b, n, *f):
    """Зображує графік функцій *f на інтервалі [a,b] у n точках
    """
    tabb = False  # чи було табульовано першу функцію
    x = 0
    m = len(f)  # кількість функцій
    for i, ff in enumerate(f):
        style = styles[i % len(styles)] + colors[i % len(colors)]
        #        style = np.random.choice(styles) + np.random.choice(colors)
        if not tabb:
            x, y = tabulate(ff, a, b, n)  # табулювати функцію
            plt.subplot(m, 1, 1)  # перший підграфік
            tabb = True
        else:
            y = gety(ff, x)  # отримати y за x для функції
            plt.subplot(m, 1, i + 1)  # черговий підграфік
        movespinesticks()  # перемістити осі
        plt.xlabel('x')  # встановити надпис на осі x
        plt.ylabel('y')  # встановити надпис на осі y
        plt.plot(x, y, style, label=ff.__doc__)  # створити графік з легендою
        plt.legend(loc='best')  # встановити легенду
    plt.show()  # показати графік


def sindivx(x):
    """sin(x)/x
    """
    if x == 0:
        return 1
    else:
        return sin(x) / x


if __name__ == '__main__':
    test_n = int(input('Кількість точок: '))
    test_a = float(input('Початок відрізку: '))
    test_b = float(input('Кінець відрізку: '))

    funcs = [fun, sindivx]
    plotfunc4(test_a, test_b, test_n, *funcs)
