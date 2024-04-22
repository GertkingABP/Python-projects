import numpy as np
import numdifftools as nd
from typing import Callable, List
from scipy import optimize
import math as mt

dimensionsInFunctions = [2 for i in range(7)]

#-------------------------------------------------------ФУНКЦИИ--------------------------------------------------------#
def function_8_ur(chosen_ur, x_i):#ВЫБОР 1 ИЗ 8 УРАВНЕНИЙ
    if chosen_ur == 1:
        return lambda x: 4 * (x[0] - 5) ** 2 + (x[1] - 6) ** 2

    if chosen_ur == 2:
        if (x_i == 2):
            return lambda x: 10 * x_i + (
                        (x[0] ** 2 - 10 * mt.cos(2 * 3.14 * x[0])) + (x[1] ** 2 - 10 * mt.cos(2 * 3.14 * x[1])))
        if (x_i == 3):
            return lambda x: 10 * x_i + (
                        (x[0] ** 2 - 10 * mt.cos(2 * 3.14 * x[0])) + (x[1] ** 2 - 10 * mt.cos(2 * 3.14 * x[1])) + (
                            x[2] ** 2 - 10 * mt.cos(2 * 3.14 * x[2])))
        if (x_i == 4):
            return lambda x: 10 * x_i + (
                        (x[0] ** 2 - 10 * mt.cos(2 * 3.14 * x[0])) + (x[1] ** 2 - 10 * mt.cos(2 * 3.14 * x[1])) + (
                            x[2] ** 2 - 10 * mt.cos(2 * 3.14 * x[2])) + (x[3] ** 2 - 10 * mt.cos(2 * 3.14 * x[3])))

    if chosen_ur == 3:
        return lambda x: -20 * mt.exp(-0.2 * mt.sqrt(0.5 * (x[0] ** 2 + x[1] ** 2))) - mt.exp(
            0.5 * (mt.cos(2 * 3.14 * x[0]) + mt.cos(2 * 3.14 * x[1]))) + 2.71828 + 20

    if chosen_ur == 4:
        return lambda x: (1.5 - x[0] + x[0] * x[1]) ** 2 + (2.25 - x[0] + x[0] * x[1] ** 2) ** 2 + (
                    2.625 - x[0] + x[0] * x[1] ** 3) ** 2

    if chosen_ur == 5:
        return lambda x: 100 * mt.sqrt(abs(x[1] - 0.01 * x[0] ** 2)) + 0.01 * abs(x[0] + 10)

    if chosen_ur == 6:
        return lambda x: 0.26 * (x[0] ** 2 + x[1] ** 2) - 0.48 * x[0] * x[1]

    if chosen_ur == 7:
        return lambda x: 100 * (x[1] - x[0] ** 2) ** 2 + (x[0] - 1) ** 2


def best_sample(func: Callable[[np.array], float], x_start: List[float], eps: float, N: int = 100, M: int = 300,
                 b: float = 0.5):#НАИЛУЧШАЯ ПРОБА
    x = x_start
    k = 0
    h = 1
    while k < N:
        y_xlam = []
        f = []

        for _ in range(M):
            e = np.random.uniform(-1, 1, len(x))
            y = x + h * e / np.linalg.norm(e)
            y_xlam.append(y)
            f.append(func(y))

        min_index = np.argmin(f)
        f_min = f[min_index]

        if f_min < func(x):
            x = y_xlam[min_index]
            k += 1
        else:
            if h <= eps:
                return x
            elif h > eps:
                h *= b

    return x


def adaptive_search(func: Callable[[np.array], float], x_start: List[float], eps: float, N: int = 100, M: int = 300,
                    a: float = 1.5, b: float = 0.5):#АДАПТИВНЫЙ СЛУЧАЙНЫЙ ПОИСК
    x = x_start
    h = 1
    k = 0
    j = 1
    while k < N:
        e = np.random.uniform(-1, 1, len(x))
        y = x + h * e / np.linalg.norm(e)

        if func(y) < func(x):
            z = x + a * (y - x)
            if func(z) < func(x):
                x = z
                h *= a
                k += 1
                j = 1
                continue

        if j < M:
            j += 1
        else:
            if h <= eps:
                break

            h *= b
            j = 1

    return x

#---------------------------------------------------------MAIN---------------------------------------------------------#
print('Выберите функцию:')
print('1.Химмельблау: 4*(x1 - 5)^2 + (x2 - 6)^2')
print('2.Расстрыгина: 10n +∑[x*i^2 - 10*cos⁡(2*π*xi)] ')
print("3.Экли: -20*exp(-0.2*√(0.5*(x1^2+ x2^2)) - exp(0.5*(cos(2*3.14*x1)+ cos(2*3.14*x1)))+ e + 20")
print("4.Била: (1.5 - x1 + x1*x2)^2 + (2.25 - x1 + x1*x2^2)^2 + (2.625 - x1 + x1*x2^3)^2")
print("5.Букина: 100*√|x2 - 0.01*x1^2| + 0.01*|x1 + 10|")
print("6.Матьяса: 0.26*(x1^2 + x2^2) - 0.48*x1*x2")
print("7.Розенброка: 100*(x2-x1^2)^2 + (x1 - 1)^2")

chosen_ur = -1
while True:
    try:
        chosen_ur = int(input('\nНомер: '))
    except:
        print("Данные некорректны.")
        continue
    if 0 < chosen_ur < 8:
        break
    print('Введите число от 1 до 7.')
x_i = -1
if (chosen_ur == 2):
    while True:
        try:
            x_i = int(input('Выберите количество x (от 2 до 4): '))
        except:
            print("Данные некорректны.")
            continue
        if 1 < x_i < 5:
            break
        print('Нужно ввести от 2 до 4.')
    dimensionsInFunctions[chosen_ur - 1] = x_i


print("\nВыберите метод: ")
print('1. Метод адаптивного поиска.')
print('2. Метод наилучшей пробы.')

method = -1
while True:
    try:
        method = int(input('\nВаш выбор: '))
    except:
        print("Данные некоректны")
        continue
    if 0 < method < 3:
        break
    print('Такого номера нет. Введите 1 или 2.')

function = function_8_ur(chosen_ur, x_i)
x0 = [0. for i in range(dimensionsInFunctions[chosen_ur - 1])]
h = [0.0001 for i in range(dimensionsInFunctions[chosen_ur - 1])]
x_min = [0. for i in range(dimensionsInFunctions[chosen_ur - 1])]

print('\nВведите точку по координатам:')
i = 0
while i < dimensionsInFunctions[chosen_ur - 1]:
    try:
        x0[i] = float(input(str(i + 1) + ': '))
        i = i + 1
    except:
        print('Неверный ввод.')

while True:
    try:
        eps = float(input("\nВведите точность от 0 до 1: "))
        if 1 > eps > 0:
            break
        elif eps <= 0:
            print('Точность должна быть более 0.')
        elif eps > 1:
            print('Точность должна быть не более 1.')
    except:
        print('Вы ввели что-то другое...')

if method == 1:
    x_min = adaptive_search(function, x0, eps)

if method == 2:
    x_min = best_sample(function, x0, eps)

print("\nМинимум: ", x_min)

if chosen_ur == 1:
    function1 = 4 * (x_min[0] - 5) ** 2 + (x_min[1] - 6) ** 2

if chosen_ur == 2:
    if (x_i == 2):
        function1 = 10 * x_i + (
                (x_min[0] ** 2 - 10 * mt.cos(2 * 3.14 * x_min[0])) + (x_min[1] ** 2 - 10 * mt.cos(2 * 3.14 * x_min[1])))

    if (x_i == 3):
        function1 = 10 * x_i + (
                (x_min[0] ** 2 - 10 * mt.cos(2 * 3.14 * x_min[0])) + (x_min[1] ** 2 - 10 * mt.cos(2 * 3.14 * x_min[1])) + (
                x_min[2] ** 2 - 10 * mt.cos(2 * 3.14 * x_min[2])))

    if (x_i == 4):
        function1 = 10 * x_i + (
                (x_min[0] ** 2 - 10 * mt.cos(2 * 3.14 * x_min[0])) + (x_min[1] ** 2 - 10 * mt.cos(2 * 3.14 * x_min[1])) + (
                x_min[2] ** 2 - 10 * mt.cos(2 * 3.14 * x_min[2])) + (x_min[3] ** 2 - 10 * mt.cos(2 * 3.14 * x_min[3])))

if chosen_ur == 3:
    function1 = -20 * mt.exp(-0.2 * mt.sqrt(0.5 * (x_min[0] ** 2 + x_min[1] ** 2))) - mt.exp(
        0.5 * (mt.cos(2 * 3.14 * x_min[0]) + mt.cos(2 * 3.14 * x_min[1]))) + 2.71828 + 20

if chosen_ur == 4:
    function1 = (1.5 - x_min[0] + x_min[0] * x_min[1]) ** 2 + (2.25 - x_min[0] + x_min[0] * x_min[1] ** 2) ** 2 + (
            2.625 - x_min[0] + x_min[0] * x_min[1] ** 3) ** 2

if chosen_ur == 5:
    function1 = 100 * mt.sqrt(abs(x_min[1] - 0.01 * x_min[0] ** 2)) + 0.01 * abs(x_min[0] + 10)

if chosen_ur == 6:
    function1 = 0.26 * (x_min[0] ** 2 + x_min[1] ** 2) - 0.48 * x_min[0] * x_min[1]

if chosen_ur == 7:
    function1 = 100 * (x_min[1] - x_min[0] ** 2) ** 2 + (x_min[0] - 1) ** 2

print("\nЗначение функции: ", function1)
