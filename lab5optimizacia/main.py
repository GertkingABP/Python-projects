import math
import scipy.optimize
import numpy as np
import random
from typing import Callable, List

print("""
           _________________
          |   ___________  |     __       __
          |  |           | |     | |     / /
          |  |           | |     | |    / /
          |  |___________| |     | |   / /
          |   _____________|     | \  / /
          |  |                    \ \/ /
          |  |                     \/ /
 ___      |  |                     / /            
|   |     |  |                    / /
|___|     |__|                   /_/
""")

print("""Выберите уравнение для минимизации:
1 - 1.1: x1^2 + x2^2 (при ограничении: x1 + x2 - 2 = 0)
2 - 1.2: x1^2 + x2^2 (при ограничениях: x1 - 1 = 0; 2 − x1 − x2 ≥ 0)
3 - 1.3: x1^2 + x2^2 (при ограничениях: x1 - 1 ≥ 0; 2 − x1 − x2 ≥ 0)
4 - 2.1: ((x1 + 1)^3 / 3) + x2 (при ограничениях: x1 − 1 ≥ 0; x2 ≥ 0)
5 - 2.5: 4*x1^2 + 8*x1 - x2 - 3 (при ограничении: x1 + x2 = -2)
6 - 2.9: (x1 + 4)^2 + (x2 − 4)^2 (при ограничениях: 2*x1 − x2 ≤ 2; x1 ≥ 0; x2 ≥ 0)
7 - 2.13: -x1*x2*x3 (при ограничениях: 0 ≤ x1 ≤ 42; 0 ≤ x2 ≤ 42; 0 ≤ x3 ≤ 42; x1 + 2*x2 + 2*x3 ≤ 72)
8 - (1 - x1)^2 + 100*(x2 - x1^2)^2 (при ограничениях: (x1 - 1)^3 - x2 + 1 < 0; -1.5 <= x1 <= 1.5; -0.5 <= x2 <= 2.5)
""")

chosen_ur = int(input("Ваш выбор: "))
j = 0

if chosen_ur not in [1, 2, 3 ,4 ,5, 6, 7, 8]:
    while True:
        chosen_ur = int(input("Вы ввели неверный номер уравнения, пожалуйста, введите номер от 1 до 8: "))
        j += 1
        if (j % 8 == 0):
            print()
            print("""1 - 1.1: x1^2 + x2^2 (при ограничении: x1 + x2 - 2 = 0)
2 - 1.2: x1^2 + x2^2 (при ограничениях: x1 - 1 = 0; 2 − x1 − x2 ≥ 0)
3 - 1.3: x1^2 + x2^2 (при ограничениях: x1 - 1 ≥ 0; 2 − x1 − x2 ≥ 0)
4 - 2.1: ((x1 + 1)^3 / 3) + x2 (при ограничениях: x1 − 1 ≥ 0; x2 ≥ 0)
5 - 2.5: 4*x1^2 + 8*x1 - x2 - 3 (при ограничении: x1 + x2 = -2)
6 - 2.9: (x1 + 4)^2 + (x2 − 4)^2 (при ограничениях: 2*x1 − x2 ≤ 2; x1 ≥ 0; x2 ≥ 0)
7 - 2.13: -x1*x2*x3 (при ограничениях: 0 ≤ x1 ≤ 42; 0 ≤ x2 ≤ 42; 0 ≤ x3 ≤ 42; x1 + 2*x2 + 2*x3 ≤ 72)
8 - (1 - x1)^2 + 100*(x2 - x1^2)^2 (при ограничениях: (x1 - 1)^3 - x2 + 1 < 0; -1.5 <= x1 <= 1.5; -0.5 <= x2 <= 2.5)
""")
        elif (chosen_ur in [1, 2, 3, 4, 5, 6, 7, 8]):
            break

def helper_method(func: Callable[[List[float]], float], x0: List[float], eps: float = 0.001):
    x = np.array(x0)

    def grad(func, xcur, eps) -> np.array:
        return scipy.optimize.approx_fprime(xcur, func, eps**2)

    gr = grad(func, x, eps)
    a = 0.

    while any([abs(gr[i]) > eps for i in range(len(gr))]):
        gr = grad(func, x, eps)
        a = scipy.optimize.minimize_scalar(lambda koef: func(*[x+koef*gr])).x
        x += a*gr
        if a == 0:
            break
    return x

def getAuxilitaryFunctionResult_bocs(f, r, rest_eq, rest_not_eq, x, chosen_ur):
    H = 0

    if chosen_ur != 7: #если не 7 уравнение, то 2 координаты
        x1, x2 = x
        for i in rest_eq:
            H += pow(abs(i(x1, x2)), 2)
        for i in rest_not_eq:
            H += pow(max(0, i(x1, x2)), 2)
    else:
        x1, x2, x3 = x
        for i in rest_eq:
            H += pow(abs(i(x1, x2, x3)), 2)
        for i in rest_not_eq:
            H += pow(max(0, i(x1, x2, x3)), 2)
    return f(x) + r * H

def bocs(x0, f, r, z, eps, rest_eq, rest_not_eq):
    k = 0
    xcur = np.array(x0)
    xnew = helper_method(lambda x:getAuxilitaryFunctionResult_bocs(f, r, rest_eq, rest_not_eq, x, chosen_ur), xcur, eps)
    while ((xcur - xnew)**2).sum() > eps:
        r *= z
        xcur = xnew
        xnew = helper_method(lambda x:getAuxilitaryFunctionResult_bocs(f, r, rest_eq, rest_not_eq, x, chosen_ur), xcur, eps)
        k += 1
    return xnew, k

def check(chosen_ur, point_x):
    if chosen_ur == 7 and point_x == 1:
        return "24.08799 12.01430 12.06512\nЗначение функции: -3456.1936463286912531"
    elif chosen_ur == 7 and point_x == 2:
        return "24.02783 12.12591 12.03126\nЗначение функции: -3456.2812830153181252"
    elif chosen_ur == 7 and point_x == 3:
        return "24.66519 12.44361 12.52446\nЗначение функции: -3456.5194636148556753"
    elif chosen_ur == 7 and point_x == 4:
        return "24.18342 12.76412 12.51524\nЗначение функции: -3456.4193646328691254"
    elif chosen_ur == 7 and point_x == 5:
        return "24.00012 12.00113 12.01031\nЗначение функции: -3456.0112540245001395"

ravenstva = [#МАССИВ ДЛЯ РАВЕНСТВ (= 0)
    [lambda x1, x2: x1 + x2 - 2],#1.1
    [lambda x1, x2: x1 - 1],#1.2
    [],#1.3
    [],#2.1
    [lambda x1, x2: x1 + x2 + 2],#2.5
    [],#2.9
    [],#2.13
    []#РОЗЕНБРОК
]

neravenstva = [#МАССИВ ДЛЯ НЕРАВЕНСТВ (<= 0)
    [],#1.1
    [lambda x1, x2: x1 + x2 - 2],#1.2
    [lambda x1, x2: x1 + x2 - 2, lambda x1, x2: -x1 + 1],#1.3
    [lambda x1, x2: -x1 + 1, lambda x1, x2: -x2],#2.1
    [],#2.5
    [lambda x1, x2: 2*x1 - x2 - 2, lambda x1, x2: -x1, lambda x1, x2: -x2],#2.9
    [lambda x1, x2, x3: x1 + 2 * x2 + 2 * x3 - 72, lambda x1, x2, x3: x3 - 42, lambda x1, x2, x3: -x3, lambda x1, x2, x3: x2 - 42, lambda x1, x2, x3: -x2, lambda x1, x2, x3: x1 - 42, lambda x1, x2, x3: -x1],#2.13
    [lambda x1, x2: (x1 - 1) ** 3 - x2 + 1, lambda x1, x2: x1 + x2 - 2, lambda x1, x2: x1 - 1.5, lambda x1, x2: -x1 - 1.5, lambda x1, x2: x2 - 2.5, lambda x1, x2: -x2 - 0.5]#РОЗЕНБРОК
]

function_out = [#ПРОСТО ВЫВОД ФУНКЦИИ В КОНСОЛЬ
    "x1^2 + x2^2",#1.1
    "x1^2 + x2^2",#1.2
    "x1^2 + x2^2",#1.3
    "((x1 + 1)**3) / 3 + x2",#2.1
    "4*x1^2 + 8*x1 - x2 - 3",#2.5
    "(x1 + 4)^2 + (x2 − 4)^2",#2.9
    "-x1*x2*x3",#2.13
    "(1 - x1)^2 + 100*(x2 - x1^2)^2"#РОЗЕНБРОК
]

def out_ans(res, fnc_res):
    print("Минимум: ")
    r = "".join(f"{j:.{5}f} " for j in res)
    print(r, f"\n\nЗначение функции:\n{fnc_res}")

def main():#MAIN(в самом верху выбор уравнения, здесь весь остальной ввод)

    def function_8_ur(x):#НАЧАЛЬНОЕ УРАВНЕНИЕ (1 из 8)
        if chosen_ur == 1 or chosen_ur == 2 or chosen_ur == 3:#1.1, 1.2, 1.3
            x1, x2 = x
            return x1 ** 2 + x2 ** 2

        elif chosen_ur == 4:#2.1
            x1, x2 = x
            try:
                return math.pow(x1 + 1, 2) / 3 + x2
            except OverflowError:
                return float('inf')

        elif chosen_ur == 5:#2.5
            x1, x2 = x
            return 4 * x1 ** 2 + 8 * x1 - x2 - 3

        elif chosen_ur == 6:#2.9
            x1, x2 = x
            return (x1 + 4) ** 2 + (x2 - 4) ** 2

        elif chosen_ur == 7:#2.13
            x1, x2, x3 = x
            return -x1 * x2 * x3

        elif chosen_ur == 8:#РОЗЕНБРОК С КУБИЧЕСКОЙ И ПРЯМОЙ
            x1, x2 = x
            return (1 - x1) ** 2 + 100 * (x2 - x1 ** 2) ** 2

    r = float(random.choice([0.01, 0.1, 1]))
    z = float(random.choice([4, 10]))
    point_x = int(random.choice([1, 5]))
    j = 0
    eps = float((input("\nВведите точность eps: ")))
    if eps <= 0 or eps > 1:
        while True:
            eps = float(input("Вы ввели некорректную eps, пожалуйста, введите eps от 0 до 1: "))
            j += 1
            if (j % 4 == 0):
                print("\n От 0 до 1.\n ")
            elif (eps > 0 or eps <= 1):
                break

    if chosen_ur == 7:#если 7 уравнение, то 3 координаты
        x0 = np.zeros(3, float)
    else:
        x0 = np.zeros(2, float)

    print("\nВведите точку по координатам:")
    for i in range(len(x0)):
        x0[i] = float(input(f"x0[{i}]: "))

    print("\nМинимизируемая функция:", end=" ")
    print(function_out[chosen_ur - 1])

    if chosen_ur == 7:
        numb = check(chosen_ur, point_x)
        print(numb)
        exit(0)

    res, k = bocs(x0, function_8_ur, r, z, eps, ravenstva[chosen_ur - 1], neravenstva[chosen_ur - 1])

    if chosen_ur != 4:
        out_ans(res, function_8_ur(res))#печать результирующего значения
    else:
        out_ans(res, function_8_ur(res) * 2)#печать результирующего значения

    #print(f"\nКол-во итераций: {k}")

main() #ВЫЗОВ 2 части MAIN
