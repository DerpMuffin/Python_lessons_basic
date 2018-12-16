
__author__ = 'Абиссов Сергей Станиславович'

# Задача-1: Дано произвольное целое число (число заранее неизвестно).
# Вывести поочередно цифры исходного числа (порядок вывода цифр неважен).
# Подсказки:
# * постарайтесь решить задачу с применением арифметики и цикла while;
# * при желании решите задачу с применением цикла for.


def task_1(*args):
    if args[0] == '':
        import random
        digits = str(random.randrange(10000, 100000))
        print('Generated: ' + digits)
    else:
        digits = str(args[0])
    for d in digits:
        print(d)


# Задача-2: Исходные значения двух переменных запросить у пользователя.
# Поменять значения переменных местами. Вывести новые значения на экран.
# Подсказка:
# * постарайтесь сделать решение через дополнительную переменную 
#   или через арифметические действия
# Не нужно решать задачу так:
# print("a = ", b, "b = ", a) - это неправильное решение!


def task_2():

    a = input('Input first value: ')
    b = input('Input second value: ')

    print('Before swap: a = %s, b = %s' % (a, b))
    c = b
    b = a
    a = c
    print('After swap: a = %s, b = %s' % (a, b))

# Задача-3: Запросите у пользователя его возраст.
# Если ему есть 18 лет, выведите: "Доступ разрешен",
# иначе "Извините, пользование данным ресурсом только с 18 лет"


def task_3():

    age = int(input('Enter age: '))

    if age >= 18:
        print('Доступ разрешен')
    else:
        print('Извините, пользование данным ресурсом только с 18 лет')


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
