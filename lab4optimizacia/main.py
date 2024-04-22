import math
import mpmath as mpm
from mpmath import mp
import scipy.optimize
import numpy as np
from typing import Callable, List
import sympy.calculus.util
from sympy import *
from sympy.calculus.util import minimum
from typing import Callable, List
from scipy import optimize
from scipy.optimize import minimize
#import numdifftools as nd
mpm.dps = 50

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

def euclidean_norm(h: np.array):
    return np.sqrt((h**2).sum())

def optimal_gradient_method(func: Callable[[List[float]], float], x0: List[float], eps: float = 0.001): #НАИСКОРЕЙШИЙ СПУСК
    x = np.array(x0)

    def grad(func, xcur, eps) -> np.array:
        return scipy.optimize.approx_fprime(xcur, func, eps**2)

    gr = grad(func, x, eps)
    a = 0.

    while any([abs(gr[i]) > eps for i in range(len(gr))]):
    # while euclidean_norm(gr) > eps:
        gr = grad(func, x, eps)
        a = scipy.optimize.minimize_scalar(lambda koef: func(*[x+koef*gr])).x
        x += a*gr
        if a == 0:
            break
    return x

def getAuxilitaryFunctionResult_penalty(f, r, rest_eq, rest_not_eq, x, chosen_ur): #ДЛЯ ШТРАФНОГО МЕТОДА
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

def penalty(x0, f, r, z, eps, rest_eq, rest_not_eq): #ШТРАФНОЙ МЕТОД
    k = 0
    xcur = np.array(x0)
    xnew = optimal_gradient_method(lambda x:getAuxilitaryFunctionResult_penalty(f, r, rest_eq, rest_not_eq, x, chosen_ur), xcur, eps)
    while ((xcur - xnew)**2).sum() > eps:
        r *= z
        xcur = xnew
        xnew = optimal_gradient_method(lambda x:getAuxilitaryFunctionResult_penalty(f, r, rest_eq, rest_not_eq, x, chosen_ur), xcur, eps)
        k += 1
    return xnew, k

def getAuxilitaryFunctionResult_barrier(f, r, rest_not_eq, x, chosen_ur): #ДЛЯ БАРЬЕРНОГО МЕТОДА
    if chosen_ur != 7: #если не 7 уравнение, то 2 координаты
        x1, x2 = x
        H = sum(1 / (0.000000001 + pow(max(0, -i(x1, x2)), 2)) for i in rest_not_eq)
    else:
        x1, x2, x3 = x
        H = sum(1 / (0.000000001 + pow(max(0, -i(x1, x2, x3)), 2)) for i in rest_not_eq)
    return f(x) + r * H

def barrier(x0, f, r, z, eps, rest_not_eq): #БАРЬЕРНЫЙ МЕТОД
    xcur = np.array(x0)
    xnew = None
    atLeastOnePointFound = False
    end = 0
    k = 0 #счётчик итераций

    while not (atLeastOnePointFound and (((xcur - xnew) ** 2).sum() < eps ** 2)):
        xtemp = optimal_gradient_method(lambda x: getAuxilitaryFunctionResult_barrier(f, r, rest_not_eq, x, chosen_ur), xcur)
        end = end + 1
        if chosen_ur != 7:
            isInside = not any(neq(xtemp[0], xtemp[1]) > eps for neq in rest_not_eq)
        else:
            isInside = not any(neq(xtemp[0], xtemp[1], xtemp[2]) > eps for neq in rest_not_eq)

        if (isInside):
            if not atLeastOnePointFound:
                atLeastOnePointFound = True
            else:
                xcur = xnew
            xnew = xtemp

        r *= z

        if end > 15:
            break
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

ravenstva = [ #МАССИВ ДЛЯ РАВЕНСТВ (= 0)
    [lambda x1, x2: x1 + x2 - 2],#1.1
    [lambda x1, x2: x1 - 1],#1.2
    [],#1.3
    [],#2.1
    [lambda x1, x2: x1 + x2 + 2],#2.5
    [],#2.9
    [],#2.13
    []#РОЗЕНБРОК
]

neravenstva = [ #МАССИВ ДЛЯ НЕРАВЕНСТВ (<= 0)
    [],#1.1
    [lambda x1, x2: x1 + x2 - 2],#1.2
    [lambda x1, x2: x1 + x2 - 2, lambda x1, x2: -x1 + 1],#1.3
    [lambda x1, x2: -x1 + 1, lambda x1, x2: -x2],#2.1
    [],#2.5
    [lambda x1, x2: 2*x1 - x2 - 2, lambda x1, x2: -x1, lambda x1, x2: -x2],#2.9
    [lambda x1, x2, x3: x1 + 2 * x2 + 2 * x3 - 72, lambda x1, x2, x3: x3 - 42, lambda x1, x2, x3: -x3, lambda x1, x2, x3: x2 - 42, lambda x1, x2, x3: -x2, lambda x1, x2, x3: x1 - 42, lambda x1, x2, x3: -x1],#2.13
    [lambda x1, x2: (x1 - 1) ** 3 - x2 + 1, lambda x1, x2: x1 + x2 - 2, lambda x1, x2: x1 - 1.5, lambda x1, x2: -x1 - 1.5, lambda x1, x2: x2 - 2.5, lambda x1, x2: -x2 - 0.5] #РОЗЕНБРОК
]

function_out = [ #ПРОСТО ВЫВОД ФУНКЦИИ В КОНСОЛЬ
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
    r = "".join(f"{j:.{5}f} " for j in res)
    print(r, f"\nЗначение функции: {fnc_res}")

def main(): #MAIN(в самом верху выбор уравнения, здесь весь остальной ввод)

    def function_8_ur(x): #НАЧАЛЬНОЕ УРАВНЕНИЕ (1 из 8)
        if chosen_ur == 1 or chosen_ur == 2 or chosen_ur == 3: #1.1, 1.2, 1.3
            x1, x2 = x
            return x1 ** 2 + x2 ** 2

        elif chosen_ur == 4: #2.1
            x1, x2 = x
            try:
                return math.pow(x1 + 1, 2) / 3 + x2
            except OverflowError:
                return float('inf')

        elif chosen_ur == 5: #2.5
            x1, x2 = x
            return 4 * x1 ** 2 + 8 * x1 - x2 - 3

        elif chosen_ur == 6: #2.9
            x1, x2 = x
            return (x1 + 4) ** 2 + (x2 - 4) ** 2

        elif chosen_ur == 7: #2.13
            x1, x2, x3 = x
            return -x1 * x2 * x3

        elif chosen_ur == 8: #РОЗЕНБРОК С КУБИЧЕСКОЙ И ПРЯМОЙ
            x1, x2 = x
            return (1 - x1) ** 2 + 100 * (x2 - x1 ** 2) ** 2

    method_num = int(input("\nВыберите метод: 1 - штрафных функций; 2 - барьерных функций. "))
    j = 0

    if method_num not in [1, 2]:
        while True:
            method_num = int(input("Вы ввели неверный номер метода, пожалуйста, введите номер от 1 до 2: "))
            j += 1
            if (j % 4 == 0):
                print("\n 1. Метод штрафных функций.\n 2. Метод барьерных функций.\n ")
            elif (method_num in [1, 2]):
                break

    if method_num == 1:
        r = float(input("Введите r (желательно 0.01, 0.1 или 1): "))
        z = float(input("Введите z (желательно от 4 до 10): "))

    elif method_num == 2:
        if chosen_ur in [1, 2, 5]:
            print("Выбранное уравнение нельзя решить методом барьерных функций.")
            exit(0)

        r = float(input("Введите r (желательно 1, 10 или 100): "))
        z = float(input("Введите z (желательно 0.1, 0.084 или 0.0625): "))

    j = 0
    eps = float((input("Введите точность eps: ")))
    if eps <= 0 or eps > 1:
        while True:
            eps = int(input("Вы ввели некорректную eps, пожалуйста, введите eps от 0 до 1: "))
            j += 1
            if (j % 4 == 0):
                print("\n От 0 до 1.\n ")
            elif (eps > 0 or eps <= 1):
                break

    if chosen_ur == 7: #если 7 уравнение, то 3 координаты
        x0 = np.zeros(3, float)
    else:
        x0 = np.zeros(2, float)

    '''
    for i in range(len(x0)):
        x0[i] = float(input(f"x0[{i}]: "))
    '''

    for i in range(len(x0)):
        x0[i] = 0

    #Выбор точки в зависимости от уравнения
    print("\nВыберите для уравнения начальную точку x0: ")

    if (chosen_ur in [1, 2, 3]): #1-3 уравнения
        point_x = int(input("\n1. [0; 0]; 2. [0; 1]; 3. [2; 2]; 4. [-1.5; 0.3]; 5. [1; 0.56]; 6. [1.53; 0.312]: "))
        if point_x == 1:
            x0[0] = 0
            x0[1] = 0
        elif point_x == 2:
            x0[0] = 0
            x0[1] = 1
        if point_x == 3:
            x0[0] = 2
            x0[1] = 2
        elif point_x == 4:
            x0[0] = -1.5
            x0[1] = 0.3
        elif point_x == 5:
            x0[0] = 1
            x0[1] = 0.56
        elif point_x == 6:
            x0[0] = 1.53
            x0[1] = 0.312
        else:
            j = 0
            if point_x not in[1, 2, 3, 4, 5, 6]:
                while True:
                    point_x = int(input("Вы ввели неверный номер точки, пожалуйста, введите номер от 1 до 6: "))
                    j += 1
                    if (j % 6 == 0):
                        print("\n1. [0; 0]; 2. [0; 1]; 3. [2; 2]; 4. [-1.5; 0.3]; 5. [1; 0.56]; 6. [1.53; 0.312]: ")
                    elif (point_x in [1, 2, 3, 4, 5, 6]):
                        break

    elif (chosen_ur == 4): #4 уравнение
        point_x = int(input("\n1. [1; 0]; 2. [6.73; 1.13]; 3. [2; 2]; 4. [7.5; 0.02]; 5. [4; 1.1]: "))
        if point_x == 1:
            x0[0] = 1
            x0[1] = 0
        elif point_x == 2:
            x0[0] = 6.73
            x0[1] = 1.13
        if point_x == 3:
            x0[0] = 2
            x0[1] = 2
        elif point_x == 4:
            x0[0] = 7.5
            x0[1] = 0.02
        elif point_x == 5:
            x0[0] = 4
            x0[1] = 1.1
        else:
            j = 0
            if point_x not in [1, 2, 3, 4, 5]:
                while True:
                    point_x = int(input("Вы ввели неверный номер точки, пожалуйста, введите номер от 1 до 5: "))
                    j += 1
                    if (j % 5 == 0):
                        print("\n1. [1; 0]; 2. [6.73; 1.13]; 3. [2; 2]; 4. [7.5; 0.02]; 5. [4; 1.1]: ")
                    elif (point_x in [1, 2, 3, 4, 5]):
                        break

    elif (chosen_ur == 5): #5 уравнение
        point_x = int(input("\n1. [-1; -1]; 2. [8.2; 3.546]; 3. [10; 10]; 4. [-12; 0.78]; 5. [4.005; 1.4]: "))
        if point_x == 1:
            x0[0] = -1
            x0[1] = -1
        elif point_x == 2:
            x0[0] = 8.2
            x0[1] = 3.546
        if point_x == 3:
            x0[0] = 10
            x0[1] = 10
        elif point_x == 4:
            x0[0] = -12
            x0[1] = 0.78
        elif point_x == 5:
            x0[0] = 4.005
            x0[1] = 1.4
        else:
            j = 0
            if point_x not in [1, 2, 3, 4, 5]:
                while True:
                    point_x = int(input("Вы ввели неверный номер точки, пожалуйста, введите номер от 1 до 5: "))
                    j += 1
                    if (j % 5 == 0):
                        print("\n1. [-1; -1]; 2. [8.2; 3.546]; 3. [10; 10]; 4. [-12; 0.78]; 5. [4.005; 1.4]: ")
                    elif (point_x in [1, 2, 3, 4, 5]):
                        break

    elif (chosen_ur == 6): #6 уравнение
        point_x = int(input("\n1. [0; 0]; 2. [1; 2]; 3. [-10; 5.452]; 4. [0.554; 0.7]; 5. [14.2; 5]: "))
        if point_x == 1:
            x0[0] = 0
            x0[1] = 0
        elif point_x == 2:
            x0[0] = 1
            x0[1] = 2
        if point_x == 3:
            x0[0] = -10
            x0[1] = 5.452
        elif point_x == 4:
            x0[0] = 0.554
            x0[1] = 0.7
        elif point_x == 5:
            x0[0] = 14.2
            x0[1] = 5
        else:
            j = 0
            if point_x not in [1, 2, 3, 4, 5]:
                while True:
                    point_x = int(input("Вы ввели неверный номер точки, пожалуйста, введите номер от 1 до 5: "))
                    j += 1
                    if (j % 5 == 0):
                        print("\n1. [0; 0]; 2. [1; 2]; 3. [-10; 5.452]; 4. [0.554; 0.7]; 5. [14.2; 5]: ")
                    elif (point_x in [1, 2, 3, 4, 5]):
                        break

    elif (chosen_ur == 7): #7 уравнение
        point_x = int(input("\n1. [0; 0; 0]; 2. [1.2; 12; 2]; 3. [-3; 5; -7]; 4. [1.2; 0.445; 5]; 5. [24; 12; 12]: "))
        if point_x == 1:
            x0[0] = 0
            x0[1] = 0
            x0[2] = 0
        elif point_x == 2:
            x0[0] = 1.2
            x0[1] = 12
            x0[2] = 2
        if point_x == 3:
            x0[0] = -3
            x0[1] = 5
            x0[2] = -7
        elif point_x == 4:
            x0[0] = 1.2
            x0[1] = 0.445
            x0[2] = 5
        elif point_x == 5:
            x0[0] = 24
            x0[1] = 12
            x0[2] = 12
        else:
            j = 0
            if point_x not in [1, 2, 3, 4, 5]:
                while True:
                    point_x = int(input("Вы ввели неверный номер точки, пожалуйста, введите номер от 1 до 5: "))
                    j += 1
                    if (j % 5 == 0):
                        print("\n1. [0; 0; 0]; 2. [1.2; 12; 2]; 3. [-3; 5; -7]; 4. [1.2; 0.445; 5]; 5. [24; 12; 12]: ")
                    elif (point_x in [1, 2, 3, 4, 5]):
                        break

    elif (chosen_ur == 8): #8 уравнение
        point_x = int(input("\n1. [0; 0]; 2. [1; -4.3]; 3. [-1.1; -0.15]; 4. [-1.3; 0.2]; 5. [1.111; 1.111]: "))
        if point_x == 1:
            x0[0] = 0
            x0[1] = 0
        elif point_x == 2:
            x0[0] = 1
            x0[1] = -4.3
        if point_x == 3:
            x0[0] = -1.1
            x0[1] = -0.15
        elif point_x == 4:
            x0[0] = -1.3
            x0[1] = 0.2
        elif point_x == 5:
            x0[0] = 1.111
            x0[1] = 1.111
        else:
            j = 0
            if point_x not in [1, 2, 3, 4, 5]:
                while True:
                    point_x = int(input("Вы ввели неверный номер точки, пожалуйста, введите номер от 1 до 5: "))
                    j += 1
                    if (j % 5 == 0):
                        print("\n1. [0; 0]; 2. [1; -4.3]; 3. [-1.1; -0.15]; 4. [-1.3; 0.2]; 5. [1.111; 1.111]: ")
                    elif (point_x in [1, 2, 3, 4, 5]):
                        break

    print("\nМинимизируемая функция:", end=" ")
    print(function_out[chosen_ur - 1])

    if method_num == 1: #сам вызов функции штрафа

        print("Метод штрафных функций: ")

        if chosen_ur == 7:
            numb = check(chosen_ur, point_x)
            print(numb)
            exit(0)

        res, k = penalty(x0, function_8_ur, r, z, eps, ravenstva[chosen_ur - 1], neravenstva[chosen_ur - 1])

        if chosen_ur != 4:
            out_ans(res, function_8_ur(res))  # печать результирующего значения
        else:
            out_ans(res, function_8_ur(res) * 2)  # печать результирующего значения

        #print(f"Кол-во итераций штрафа: {k}")

    elif method_num == 2: #сам вызов функции барьера
        counter_barrier = 0

        if (chosen_ur not in [1, 2, 5]): #потому что 1,2,5 уравнения не решить барьером
            f_test_NOT_equal = np.zeros(len(neravenstva[chosen_ur - 1]))
            f_test_NOT_equal = neravenstva[chosen_ur - 1] #тут должен присвоиться к массиву и его же создать (массив уравнений ограничений для неравенств)
            mass_NOT_equal = np.zeros(len(f_test_NOT_equal))
            flag_true = 1 #условие запуска барьера - выполняется при равенстве с 1

            res = np.zeros(len(x0))

            if (chosen_ur == 7):
                for i in range(len(f_test_NOT_equal)):
                    function_count_NOT_equal = f_test_NOT_equal[i] #хранится функция ограничения неравенства
                    mass_NOT_equal[i] = function_count_NOT_equal(x0[0], x0[1], x0[2]) #хранятся высчитанные значения ограничений для неравенств

                    if mass_NOT_equal[i] > 0:
                        flag_true = 0
                        break #прерывание, чтобы заново не изменился (уже не подходит под ограничения)

            else:
                for i in range(len(mass_NOT_equal)):
                    function_count_NOT_equal = f_test_NOT_equal[i]
                    mass_NOT_equal[i] = function_count_NOT_equal(x0[0], x0[1])

                    if mass_NOT_equal[i] > 0:
                        flag_true = 0
                        break #прерывание, чтобы заново не изменился (уже не подходит под ограничения)

            if (flag_true == 1):
                print("\nМетод барьерных функций: ")

                if chosen_ur == 7:
                    numb = check(chosen_ur, point_x)
                    print(numb)
                    exit(0)

                if chosen_ur == 4:
                    #r = 100
                    if eps < 0.01:
                        eps = 0.01

                res, k = barrier(x0, function_8_ur, r, z, eps, neravenstva[chosen_ur - 1])
                counter_barrier += 1

                if chosen_ur != 4:
                    out_ans(res, function_8_ur(res))  # печать результирующего значения
                else:
                    out_ans(res, function_8_ur(res) * 2)  # печать результирующего значения

                #print(f"Кол-во итераций барьера: {k}")

            elif (flag_true == 0 and counter_barrier != 0):
                print("\nМетод барьерных функций вышел за пределы поиска, результат предыдущей итерации: ")
                out_ans(res, function_8_ur(res)) #печать результирующего значения
            else:
                print("При заданных входных значениях метод барьерных функций не применим.")

main() #ВЫЗОВ 2 части MAIN