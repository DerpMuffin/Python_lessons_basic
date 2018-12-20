import random


def generate_int_array(capacity, _from, to):
    return [random.randint(_from, to) for i in range(capacity)]


# Задача-1:
# Дан список, заполненный произвольными целыми числами, получите новый список,
# элементами которого будут квадратные корни элементов исходного списка,
# но только если результаты извлечения корня не имеют десятичной части и
# если такой корень вообще можно извлечь
# Пример: Дано: [2, -5, 8, 9, -25, 25, 4]   Результат: [3, 5, 2]


def task_1():
    import math

    int_array = generate_int_array(10, -50, 100)
    sqrt_array = []

    print(f'Int-array: {int_array}')

    for i in int_array:
        if i < 0:
            continue
        sqrt = math.sqrt(i)
        if int(sqrt) == sqrt:
            sqrt_array.append(int(sqrt))

    print(f'Result: {sqrt_array}')


# Задача-2: Дана дата в формате dd.mm.yyyy, например: 02.11.2013.
# Ваша задача вывести дату в текстовом виде, например: второе ноября 2013 года.
# Склонением пренебречь (2000 года, 2010 года)


def task_2():
    import locale
    from datetime import datetime

    locale.setlocale(locale.LC_ALL, 'ru_RU')

    date = datetime.now()
    print(date.strftime('%d %B %Y года'))


# Задача-3: Напишите алгоритм, заполняющий список произвольными целыми числами
# в диапазоне от -100 до 100. В списке должно быть n - элементов.
# Подсказка:
# для получения случайного числа используйте функцию randint() модуля random


def task_3():

    n = int(input('Enter the capacity of the array\n'))
    int_array = generate_int_array(n, -100, 100)
    print(f'Result array: {int_array}')


# Задача-4: Дан список, заполненный произвольными целыми числами.
# Получите новый список, элементами которого будут: 
# а) неповторяющиеся элементы исходного списка:
# например, lst = [1, 2, 4, 5, 6, 2, 5, 2], нужно получить lst2 = [1, 2, 4, 5, 6]
# б) элементы исходного списка, которые не имеют повторений:
# например, lst = [1 , 2, 4, 5, 6, 2, 5, 2], нужно получить lst2 = [1, 4, 6]


def task_4():

    int_array = generate_int_array(20, -10, 10)

    distinct_array = []
    solo_array = []

    for item in int_array:

        if item in distinct_array:
            if item in solo_array:
                solo_array.remove(item)
            continue

        distinct_array.append(item)
        solo_array.append(item)

    print(f'Origin array:\n{int_array};\nDistinct array:\n{distinct_array}\nSolo-item array:\n{solo_array}')


exit_flag = False
tasks = {
    '1': task_1,
    '2': task_2,
    '3': task_3,
    '4': task_4,
}

while not exit_flag:
    answer = input(f'Select task: [ {" | ".join(tasks.keys())} ]\n')

    if answer in tasks:
        tasks[answer]()
    else:
        print('Incorrect task number')

    exit_answer = input('Quit? [Y,N]\n')
    if exit_answer.upper() == 'Y':
        exit_flag = True