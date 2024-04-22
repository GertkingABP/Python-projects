import math

def function (xi):
    try:
        if (choice_yp == 1):
            f_xi = pow(xi, 2) - 2 * xi + 1  # 1 пример (x-1)^2 = x^2 - 2*x + 1
            return f_xi
        if (choice_yp == 2):
            f_xi = 4 * pow(xi, 3) - 8 * pow(xi, 2) - 11 * xi + 5
            return f_xi
        if (choice_yp == 3):
            if xi == 0:
                xi = 0.001
            f_xi = xi + 3 / pow(xi, 2)
            return f_xi
        if (choice_yp == 4):
            if xi == -2:
                xi = -1.999
            elif xi == 2:
                xi = 2.001
            f_xi = (xi + 2.5) / (4 - pow(xi, 2))
            return f_xi
        if (choice_yp == 5):
            f_xi = -math.sin(xi) - ((math.sin(3 * xi)) / 3)
            return f_xi
        if (choice_yp == 6):
            f_xi = -2 * math.sin(xi) - math.sin(2 * xi) - ((2 * math.sin(3 * xi)) / 3)
            return f_xi
    except:
        print("\n\n Введенные вами значения x0 и h не удовлетворяют ОДЗ данного уравнения! \
        \n Просьба изменить вводимые x0 или h при следующем вызове данного уравнения. ")
        exit()


choice_yp = int((input("\n Приветствуем вас в приложении.\n Выберите какое уравнение хотите решить: \n\
 ! ВАЖНО! Вводите только тот номер уравнения, который указан в перечне: \
                    \n\n 1. (x - 1)^2 \n 2. 4x^3 - 8x^2 - 11x + 5 \n 3. x + 3/(x^2) \n \
4. (x + 2.5) / (4 - x^2) \n 5. sin(x) - sin(3x) / 3 \n 6. -2sin(x) - sin(2x) - (2sin(3x)) / 3 \n\n Номер уравнения для решения: ")))

list_choice_yp = list(range(1, 7))
i = 0
if choice_yp not in list_choice_yp:
    while True:
         choice_yp = int((input(" Вы ввели неверный номер уравнения, пожалуйста, введите номер от 1 до 6,"
                               " чтобы выбрать уравнение для решения из списка: ")))
         i += 1
         if (i % 4 == 0):
             print("\n 1. (x - 1)^2 \n 2. 4x^3 - 8x^2 - 11x + 5 \n 3. x + 3/(x^2) \n \
    4. (x + 2.5) / (4 - x^2) \n 5. sin(x) - sin(3x) / 3 \n 6. -2sin(x) - sin(2x) - (2sin(3x)) / 3 \n\n Номер уравнения для решения: ")
         elif (choice_yp in list_choice_yp):
             break

choice_method = int(input("\n Выберите метод с помощью которого вы будете решать уравнение: \n\
! ВАЖНО! Вводите только тот номер метода, который указан в перечне: \n\
 1. \"Метод деления пополам (дихотомии)\" \n 2. \"Метод параболической аппроксимации Пауэлла\" \n\n Номер метода для решения: "))

j = 0
if choice_method not in [1, 2]:
    while True:
         choice_method = int((input(" Вы ввели неверный номер метода, пожалуйста, введите номер от 1 до 2,"
                               " чтобы выбрать метод для решения уравнения из списка: ")))
         j += 1
         if (j % 4 == 0):
             print("\n 1. \"Метод деления пополам (дихотомии)\" \n 2. \"Метод параболической аппроксимации Пауэлла\"\
             \n\n Номер метода для решения уравнения: ")
         elif (choice_method in [1 , 2]):
             break


x0 = float((input(" \n Введите значение X0: ")))   #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# if  choice_yp == 3:
#     while True:
#         x0 = float((input(" Вы ввели значение х0, которое не подходит к ОДЗ данного уравнения, пожалуйста введите новое значение: ")))
#         if x0 != 0:
#             break

# x0 = float((input(" Вы ввели значение х0, которое не подходит к ОДЗ данного уравнения, пожалуйста введите новое значение: ")))
# elif choice_yp == 4:
#     while True:
#         x0 = float((input(" Вы ввели значение х0, которое не подходит к ОДЗ данного уравнения, пожалуйста введите новое значение: ")))
#         if x0 != 2 and x0 != -2:
#             break

h = float((input(" Введите значение h: ")))
eps = float((input(" Введите значение e: ")))

while eps <= 0:
    eps = float((input(" Вы ввели eps, параметры которой не подходят к следующему условию: \n 1. eps > 0 \n \
Пожалуйста введите значение eps, подходящее под это условие: ")))



# ------------------------------------ Метод Дэвиса-Свенна-Кэмпи ------------------------------------------------------
flag = 0; a_flag = 0; b_flag = 0
xi = x0

while True:
    if flag == 0:           # первые 1-3 шаг для алгоритма Свенна
        f_xi = function(x0)
        f_xi_h_positive = function(x0 + h)
        if f_xi > f_xi_h_positive:
            k = 2
            a = x0
            xi = x0 + h
            f_xi = f_xi_h_positive
            flag += 1
            a_flag = 1
        else:
            f_xi_h_negative = function(x0 - h)
            if f_xi_h_negative >= f_xi:
                a = x0 - h
                b = x0 + h
                break
            else:
                b = x0
                xi = x0 - h
                f_xi = f_xi_h_negative
                h = -h
                k = 2
                flag += 1
                b_flag = 1

    elif flag != 0:                       # петля 4-6 шаг
        xi_next = x0 + pow(2, k - 1) * h
        f_xk = function(xi_next)
        if (f_xi <= f_xk) and (h > 0):
            b = xi_next
            b_flag = 1
        elif (f_xi <= f_xk) and (h <= 0):
            a = xi_next
            a_flag = 1
        else:
            if h > 0:
                a = xi
                a_flag = 1
            else:
                b = xi
                b_flag = 1

        k += 1         # возврат на 4 шаг и присвоение переменным предыдущих значений
        f_xi = f_xk
        xi = xi_next

        if (a_flag == 1) and (b_flag == 1):       # проверка на условие остановки цикла (пока a и b не будут найдены)
            break

    else:
        print("\n\n Ошибка! Проверьте правильность ввода!")  # на крайний случай

a0 = a
b0 = b

print (f"\n а равен: {a} \n b равен:  {b}")


# ------------------------------------ Метод деления пополам (дихотомии) -----------------------------------
if choice_method == 1:
    print("\nПрограмма для решения задачи минимизации \"Метод деления пополам (дихотомии)\" ")

    a = a0
    b = b0

    sigma = float((input(" Введите значение sigma: ")))

    while (sigma <= 0) or (sigma >= eps):
        sigma = float((input(" Вы ввели sigma, параметры которой не подходят к следующим условиям: \n 1. sigma > 0 \n \
2. sigma < eps \n Пожалуйста введите значение sigma, подходящее под эти условия: ")))

    while True:
        x1 = (1/2) * (a + b) - sigma
        x2 = (1/2) * (a + b) + sigma

        f_x1 = function(x1)
        f_x2 = function(x2)

        if f_x1 <= f_x2:
            b = x2
        else:
            a = x1

        if (b - a)/2 < eps:
            break

    x_star = (a + b)/2
    f_star = function(x_star)

    print (f"\n x* равен: {round(x_star, 4)} \n f(x*) равен:  {round(f_star, 4)}")


# ------------------------------------ Метод параболической аппроксимации Пауэлла ---------------------
if choice_method == 2:
    print("\nПрограмма для решения задачи минимизации \"Метод параболической аппроксимации Пауэлла\" ")

    a = a0
    b = b0

    x1 = a
    x2 = (1/2) * (a + b)
    x3 = b

    while True:
        f1 = function(x1)
        f2 = function(x2)
        f3 = function(x3)

        function_list = [f1, f2, f3]           # поиск минимума
        min_f= min(function_list, key = float)

        if (min_f == f1):
            x_ = x1
        elif (min_f == f2):
            x_ = x2
        else:
            x_ = x3

        x4 = (1/2) * ((pow(x2, 2) - pow(x3, 2)) * f1 + (pow(x3, 2) - pow(x1, 2)) * f2 + (pow(x1, 2) - pow(x2, 2)) * f3) / ((x2 - x3) * f1 + (x3 - x1) * f2 + (x1 - x2) * f3)


        if (math.fabs(x4 - x_) <= eps):    # условие выхода из алгоритма
            break

        mas_x = [x1, x2, x3, x4]

        for iterator in range(4):
            for j in range(3-iterator):
                if mas_x[j] > mas_x[j+1]:
                    mas_x[j], mas_x[j+1] = mas_x[j+1], mas_x[j]     # сортировка значений

        x1 = mas_x[0]
        x2 = mas_x[1]
        x3 = mas_x[2]
        x4 = mas_x[3]

        f1 = function(x1)
        f2 = function(x2)
        f3 = function(x3)
        f4 = function(x4)

        function_list_new = [f1, f2, f3, f4]

        for i in range(3):
            for j in range(3-i):
                if function_list_new[j] > function_list_new[j+1]:
                    function_list_new[j], function_list_new[j+1] = function_list_new[j+1], function_list_new[j]     # сортировка значений

        if (function_list_new[3] == f1):
            x1 = x2
            x2 = x3
            x3 = x4
        elif (function_list_new[3] == f2):
            x1 = x1
            x2 = x3
            x3 = x4
        elif (function_list_new[3] == f3):
            x1 = x1
            x2 = x2
            x3 = x4
        else:
            x1 = x1    # потому что х4 - и так будет иметь наибольшее значение, т.е. перенумеровывать не надо
            x2 = x2
            x3 = x3

    x_star = x4
    f_star = function(x_star)

    print (f"\n x* равен: {round(x_star, 4)} \n f(x*) равен:  {round(f_star, 4)}")
