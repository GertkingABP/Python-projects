import numpy as np
import sympy.calculus.util
from sympy import *
from sympy.calculus.util import minimum
from typing import Callable, List
from scipy import optimize
from scipy.optimize import minimize
import numdifftools as nd

#------------------------------------------------------------------ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ И ПЕРЕМЕННЫЕ------------------------------------------------------------------#

Path = []
helper = 0.000000001

def function_selection_4_ex(ur): #ДЛЯ НОВОГО НЬЮТОНА И НАИСКОРЕЙШЕГО
    if ur == 1:
        return lambda x: 4 * (x[0] - 5) ** 2 + (x[1] - 6) ** 2
    if ur == 2:
        return lambda x: (x[0] ** 2 + x[1] - 11) ** 2 + (x[0] + x[1] ** 2 - 7) ** 2
    if ur == 3:
        return lambda x: 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2 + 90 * (x[3] - x[2] ** 2) ** 2 + (1 - x[2]) ** 2 + 10.1 * ((x[1] - 1) ** 2 + (x[3] - 1) ** 2) + 19.8 * (x[1] - 1) * (x[3] - 1)
    if ur == 4:
        return lambda x: (x[0] + 10 * x[1]) ** 2 + 5 * (x[2] - x[3]) ** 2 + (x[1] - 2 * x[2]) ** 4 + 10 * (x[0] - x[3]) ** 4

def optimal_gradient_method(f: Callable[[List[float]], float], b: List[float], eps: float): #НАИСКОРЕЙШИЙ СПУСК
    x = np.array(b)

    def grad(f, xcur, eps) -> np.array:
        return optimize.approx_fprime(xcur, f, eps**2)

    gr = grad(f, x, eps)
    a = 0.

    while any([abs(gr[i]) > eps for i in range(len(gr))]):
        gr = grad(f, x, eps)
        a = optimize.minimize_scalar(lambda koef: f(*[x+koef*gr])).x
        x += a*gr
    return x

def newton_raphson(b: List[float], eps: float, f: Callable[..., float]): #НЬЮТОН-РАФСОН
    xcur = np.array(b)
    Path.append(xcur)
    hess_f = nd.Hessian(f)
    n = len(b)

    grad = optimize.approx_fprime(xcur, f, eps ** 4) #ш.2
    y = 0
    while any([pow(abs(grad[i]), 1.5) > eps for i in range(n)]): #ш.3
        y = y + 1
        h = np.linalg.inv(hess_f(xcur)) #ш.4 & ш.5
        pk = (-1 * h).dot(grad) #ш.6
        a = optimize.minimize_scalar(lambda a: f(xcur + pk * a), bounds=(0,)).x #ш.7
        xcur = xcur + a * pk #ш.8
        Path.append(xcur)
        grad = optimize.approx_fprime(xcur, f, eps * eps) #ш.2
        if y > 100:
            break
    return xcur #ш.0

def function_dif (b): #ПРОИЗВОДНАЯ ДЛЯ НАЧАЛЬНОЙ ФУНКЦИИ
    try:
        if (choosen_ur == 1):
            f_xi = 4 * (b[0] - 5)**2 + (b[1] - 6)**2
            return f_xi
        if (choosen_ur == 2):
            f_xi = (b[0]**2 + b[1] - 11)**2 + (b[0] + b[1]**2 - 7)**2
            return f_xi
        if (choosen_ur == 3):
            f_xi =  100 * (b[1] - b[0]**2)**2 + (1 - b[0])**2 + 90 * (b[3] - b[2]**2)**2 + (1 - b[2])**2 + 10.1 * ((b[1] - 1)**2 + (b[3] - 1)**2) + 19.8 * (b[1] - 1) * (b[3] - 1)
            return f_xi
        if (choosen_ur == 4):
            f_xi = (b[0] + 10 * b[1])**2 + 5 * (b[2] - b[3])**2 + (b[1] - 2 * b[2])**4 + 10 * (b[0] - b[3])**4
            return f_xi

    except NameError:
        print("\n\n Введенные вами значения x0 и h не удовлетворяют ОДЗ данного уравнения!\nПросьба изменить вводимые x0 или h при следующем вызове данного уравнения.")
        exit()

#------------------------------------------------------------------------------MAIN------------------------------------------------------------------------------#

choosen_ur = int((input("\n Выберите, какое уравнение хотите решить: \n \
1. 4(x1 - 5)^2 + (x2 - 6)^2 \n 2. (x1^2 + x2 - 11)^2 + (x1 + x2^2 - 7)^2 \n \
3. 100(x2 - x1^2)^2 + (1 - x1)^2 + 90(x4 - x3^2)^2 + (1 - x3)^2 + 10.1[(x2 -1)^2 + (x4 -1)^2] + 19.8(x2 - 1)(x4 - 1) \n \
4. (x1 + 10x2)^2 + 5(x3 - x4)^2 + (x2 - 2x3)^4 + 10(x1 - x4)^4 \n\n Номер уравнения: ")))

list_ur = list(range(1, 5))
iter = 0
if choosen_ur not in list_ur:
    while True:
         choosen_ur = int((input(" Вы ввели неверный номер уравнения, пожалуйста, введите номер от 1 до 4: ")))
         iter += 1
         if (iter % 4 == 0):
             print("\n Пожалуйста, выберите номер уравнения из следующего списка: \n 1. 4(x1 - 5)^2 + (x2 - 6)^2 \n 2. (x1^2 + x2 - 11)^2 + (x1 + x2^2 - 7)^2 \n \
3. 100(x2 - x1^2)^2 + (1 - x1)^2 + 90(x4 - x3^2)^2 + (1 - x3)^2 + 10.1[(x2 -1)^2 + (x4 -1)^2] + 19.8(x2 - 1)(x4 - 1) \n \
4. (x1 + 10x2)^2 + 5(x3 - x4)^2 + (x2 - 2x3)^4 + 10(x1 - x4)^4 \n\n Уравнение: ")
         elif (choosen_ur in list_ur):
             break


choosen_method = int(input("\n Выберите метод с помощью которого вы будете решать уравнение: \n \
1. Метод Хука-Дживса.\n 2. Метод наискорейшего спуска.\n 3. Метод Ньютона-Рафсона.\n\n Метод: "))

j = 0
if choosen_method not in [1, 2, 3]:
    while True:
         choosen_method = int(input(" Вы ввели неверный номер метода, пожалуйста, введите номер от 1 до 3: "))
         j += 1
         if (j % 4 == 0):
             print("\n 1. Метод Хука-Дживса.\n 2. Метод наискорейшего спуска.\n 3. Метод Ньютона-Рафсона\n\n Метод: ")
         elif (choosen_method in [1 , 2]):
             break

eps = float((input(" Введите точность eps: ")))

while eps <= 0:
    eps = float((input(" Вы ввели eps, параметры которой не подходят к следующему условию: \n 1. eps > 0 \n \
Пожалуйста введите подходящее значение eps: ")))

if choosen_ur  in [1, 2]: #создает пустые размерные матрицы для номера уравнений
    h = np.zeros(2, float)
    b = np.zeros(2, float)
    f_xi_diff = np.zeros(2, float)
    x_st  = np.zeros(2, float)

elif choosen_ur  in [3, 4]:
    h = np.zeros(4, float)
    b = np.zeros(4, float)
    f_xi_diff = np.zeros(4, float)
    x_st = np.zeros(4, float)

if choosen_method == 1: #ДЛЯ ХУКА-ДЖИВСА
    z = float((input(" Введите z: ")))
    print(" Введите вектор h: ")
    for i in range(len(h)):
        h[i] = float(input(f" h[{i}]: "))

print("\n Введите начальную точку b: ")
for i in range(len(b)):
    b[i] = float(input(f" b[{i}]: "))

#-----------------------------------------------------------------------МЕТОД-ХУКА-ДЖИВСА-----------------------------------------------------------------------#
def exploratory_search (b): #ИССЛЕДОВАТЕЛЬСКИЙ ПОИСК
    try:
        key_1st = 1 #переход на ш.3
        for i in range(0, len(b)):
            if key_1st == 1:
                fb = function_dif(b) #ш.1

            b[i] = b[i] + h[i] * 1
            f = function_dif(b) #ш.3

            if f + helper< fb: #ш.4
                fb = f

            else:
                b[i] = b[i] - 2 * h[i] * 1
                f = function_dif(b) #ш.5
                if f +  + helper< fb: #ш.6
                    fb = f

            key_1st = 0

        return b, fb

    except NameError:
        print("Ошибка в исследующем поиске!")

if choosen_method == 1: #ЕСЛИ ХУКА-ДЖИВС
    k = 0
    key_3rd = 1 #переход на ш.3
    while True:
        if key_3rd == 1:
            k += 1
            xk = b #ш.1
                                             #ш.2
            b2, fb2 = exploratory_search(xk) #вызов алгоритма 2.1.2.2(исследующий поиск)

        xk  = b + 2 * (b2 - b) #ш.3

        x, fx = exploratory_search(xk) #ш.4

        b = b2 #ш.5

        if fx + helper< function_dif(b): #ш.6
            b2 = x #переход на ш.3
            key_3rd = 0

        elif fx -  helper> function_dif(b): #ш.7
            key_3rd = 1 #переход на ш.1

        else: #ш.8
            if choosen_ur in [1, 2]:
                if pow((pow(h[0], 2) + pow(h[1], 2)), 0.5) <= eps + helper:
                    x_st = b #ш.10
                    break

                else: #ш.9
                    h = z * h
                    key_3rd = 1 #переход на ш.1

            elif choosen_ur in [3, 4]:
                if pow((pow(h[0], 2) + pow(h[1], 2) + pow(h[2], 2) + pow(h[3], 2)), 0.5) <= eps + helper:
                    x_st = b #ш.10
                    break

                else: #ш.9
                    h = z * h
                    key_3rd = 1 #переход на ш.1

    answer = x_st
    print ("\n Результат работы метода Хука-Дживса:")

#--------------------------------------------------------------------------НАИСКОРЕЙШИЙ--------------------------------------------------------------------------#

if choosen_method == 2: #ЕСЛИ НАКИСКОРЕЙШИЙ СПУСК
    function2 = function_selection_4_ex(choosen_ur)
    answer = optimal_gradient_method(function2, b, eps)
    print("\n Результат работы метода наискорейшего спуска:")

#--------------------------------------------------------------------------НЬЮТОН-РАФСОН-------------------------------------------------------------------------#

if choosen_method == 3: #ЕСЛИ НЬЮТОН-РАФСОН
    function3 = function_selection_4_ex(choosen_ur)
    answer = newton_raphson(b, eps, function3)
    print("\n Результат работы метода Ньютона-Рафсона:")

#------------------------------------------------------------------------------ОТВЕТ-----------------------------------------------------------------------------#

print (f" x* = {np.round(answer, 6)} \n f(x*) = {np.round(function_dif(answer), 4)}")