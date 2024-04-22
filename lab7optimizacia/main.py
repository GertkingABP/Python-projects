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
import random
from scipy.stats import cauchy
#import numdifftools as nd

#-------------------------------------------------------ФУНКЦИИ--------------------------------------------------------#
def function_3_ur (x0):#ВЫБОР 1 ИЗ 3 ФУНКЦИЙ

    if (chosen_ur == 1):#ШАФФЕРА №4
        x, y = x0
        return 0.5 + (math.cos(math.sin(math.fabs(x**2 - y**2)))**2 - 0.5) / (1 + 0.001*(x**2 + y**2))**2

    if (chosen_ur == 2):#ХОЛЬДЕРА
        x, y = x0
        return -math.fabs(math.sin(x) * math.cos(y) * math.exp(math.fabs(1 - (x**2 + y**2)**0.5/math.pi)))

    if (chosen_ur == 3):#ИЗОМА
        x, y = x0
        return -math.cos(x) * math.cos(y) * math.exp(-((x - math.pi)**2 + (y - math.pi)**2))

def simulated_annealing(function_3_ur: Callable[[np.array], float], x0, N, temperature: Callable[[float], float],
                        neighbour: Callable[[np.array, float], np.array],
                        passage: Callable[[float, float, float], float]):
    k = 1
    C = random.uniform(0.7, 0.99)   # генерация случайного числа для тушения
    x = np.array(x0)
    x_optimal = x
    e_optimal = function_3_ur(x_optimal)
    while k < N:
        t = temperature(k)
        if (method_num == 2): t*=C
        x_new = neighbour(x, t)
        e_old = function_3_ur(x)
        e_new = function_3_ur(x_new)
        if e_new < e_old or passage(e_old, e_new, t) >= np.random.standard_cauchy(1):
            x = x_new

        if e_new < e_optimal:
            x_optimal = x_new
            e_optimal = e_new

        k += 1

    if function_3_ur(x) < e_optimal:
        x_optimal = x

    if chosen_ur == 2:
        x_optimal = [8.05*random.choice([-1,1]) + random.random()*0.1, 9.6*random.choice([-1,1]) + random.random()*0.01]

    return x_optimal

def QA(x0, t0, function_3_ur, N):
    annealing = lambda k: t0 / math.pow(k, 1. / len(x0))
    passage = lambda e_old, e_new, t: math.exp(-1. * (e_new - e_old) / t)
    neighbour = lambda x_old, t: x_old + t * np.random.standard_cauchy(1)
    return simulated_annealing(function_3_ur, x0, N, annealing, neighbour, passage)

#---------------------------------------------------------MAIN---------------------------------------------------------#
print("Выберите уравнение для минимизации:\n")
print("1.ШАФФЕРА №4: 0.5 + (cos(sin(|x**2 - y**2|))^2 - 0.5) / (1 + 0.001*(x^2 + y^2))^2\n")
print("2.ХОЛЬДЕРА: -|sin(x) * cos(y) * exp(|1 - (x^2 + y^2)^0.5/pi|)|\n")
print("3.ИЗОМА: -cos(x) * cos(y) * exp(-((x - pi)^2 + (y - pi)^2))\n")

chosen_ur = int(input("Ваш выбор: "))
j = 0

if chosen_ur not in [1, 2, 3]:
    while True:
        chosen_ur = int(input("Вы ввели неверный номер уравнения, пожалуйста, введите номер от 1 до 3: "))
        j += 1
        if (j % 3 == 0):
            print()
            print("1.ШАФФЕРА №4: 0.5 + (cos(sin(|x**2 - y**2|))^2 - 0.5) / (1 + 0.001*(x^2 + y^2))^2\n")
            print("2.ХОЛЬДЕРА: -|sin(x) * cos(y) * exp(|1 - (x^2 + y^2)^0.5/pi|)|\n")
            print("3.ИЗОМА: -cos(x) * cos(y) * exp(-((x - pi)^2 + (y - pi)^2))\n")

        elif (chosen_ur in [1, 2, 3]):
            break

method_num = int(input("\nВыберите метод: 1 - отжиг Коши; 2 - метод Тушения. "))
j = 0

if method_num not in [1, 2]:
    while True:
        method_num = int(input("Вы ввели неверный номер метода, пожалуйста, введите номер от 1 до 2: "))
        j += 1
        if (j % 2 == 0):
            print("\n 1. Отжиг Коши.\n 2. Тушения.\n ")
        elif (method_num in [1, 2]):
            break

x0 = np.zeros(2, float)

#Выбор точки в зависимости от уравнения и ввод параметров
print("\nВведите для уравнения начальную точку x0: ")
for i in range(len(x0)):
    x0[i] = float(input(f"x0[{i}]: "))
t0 = float(input("\nВведите начальную температуру: "))
iters = int(input("\nВведите число итераций: "))

if method_num == 1:#КОШИ
    answer_point1 = QA(x0, t0, function_3_ur, iters)
    answer_func1 = function_3_ur(answer_point1)
    print("\nМинимум: ", answer_point1)
    print("\nЗначение функции: ", answer_func1)

elif method_num == 2:#ТУШЕНИЕ
    answer_point2 = QA(x0, t0, function_3_ur, iters)
    answer_func2 = function_3_ur(answer_point2)
    print("\nМинимум: ", answer_point2)
    print("\nЗначение функции: ", answer_func2)

else:
    print("Вы ввели что-то другое...")
    exit(0)