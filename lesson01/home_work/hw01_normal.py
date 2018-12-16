
__author__ = 'Абиссов Сергей Станиславович'

# Задача-1: Дано произвольное целое число, вывести самую большую цифру этого числа.
# Например, дается x = 58375.
# Нужно вывести максимальную цифру в данном числе, т.е. 8.
# Подразумевается, что мы не знаем это число заранее.
# Число приходит в виде целого беззнакового.
# Подсказки:
# * постарайтесь решить задачу с применением арифметики и цикла while;
# * при желании и понимании решите задачу с применением цикла for.


def task_1(*args):
    if args[0] == '':
        import random
        digits = str(random.randrange(10000, 100000))
        print('Generated: ' + digits)
    else:
        digits = str(args[0])

    max_value = 0
    for d in digits:
        if int(d) > max_value:
            max_value = int(d)
    print(str(max_value))


# Задача-2: Исходные значения двух переменных запросить у пользователя.
# Поменять значения переменных местами. Вывести новые значения на экран.
# Решите задачу, используя только две переменные.
# Подсказки:
# * постарайтесь сделать решение через действия над числами;
# * при желании и понимании воспользуйтесь синтаксисом кортежей Python.


def task_2():

    a = input('Input first value: ')
    b = input('Input second value: ')

    print('Before swap: a = %s, b = %s' % (a, b))
    a, b = b, a
    print('After swap: a = %s, b = %s' % (a, b))


# Задача-3: Напишите программу, вычисляющую корни квадратного уравнения вида
# ax² + bx + c = 0.
# Коэффициенты уравнения вводятся пользователем.
# Для вычисления квадратного корня воспользуйтесь функцией sqrt() модуля math:
# import math
# math.sqrt(4) - вычисляет корень числа 4


def task_3():

    from  math import sqrt

    a = int(input('Input a value: '))
    b = int(input('Input b value: '))
    c = int(input('Input c value: '))

    print("ax² + bx + c = 0".replace('a', str(a)).replace('b', str(b)).replace('c', str(c)))

    d = b**2 - 4 * a * c

    if d > 0:
        x1 = (-b + sqrt(d)) / (2 * a)
        x2 = (-b - sqrt(d)) / (2 * a)
        print('x1 = %s; x2 = %s' % (x1, x2))

    elif d == 0:
        x = -b / (2 * a)
        print('x = ' + str(x))

    else:
        print('---')


exit_flag = False
while not exit_flag:
    answer = input('Select task: [1|2|3]')

    if answer == '1':
        value = input('Input test digit value: ')
        task_1(value)
    elif answer == '2':
        task_2()
    elif answer == '3':
        task_3()

    exit_answer = input('Quit? [Y,N]')
    if exit_answer.upper() == 'Y':
        exit_flag = True
