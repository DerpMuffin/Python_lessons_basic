# Задание-1: уравнение прямой вида y = kx + b задано в виде строки.
# Определить координату y точки с заданной координатой x.

equation = 'y = -12x + 11111140.2121'
x = 2.5


# вычислите и выведите y


def task_1():
    import re

    regex = '(y)=([\-\d]+([\.][\d]+)*)*x(([\-\+])([\-\d]+(.[\d]+)*))*'
    match = re.match(regex, equation.replace(' ', ''))
    if match is None:
        print('Bad parse')
        return
    k = float(match.group(2))
    b = float(match.group(4))
    y = k * x + b

    print(f'y = {y}')


# Задание-2: Дата задана в виде строки формата 'dd.mm.yyyy'.
# Проверить, корректно ли введена дата.
# Условия корректности:
# 1. День должен приводиться к целому числу в диапазоне от 1 до 30(31)
#  (в зависимости от месяца, февраль не учитываем)
# 2. Месяц должен приводиться к целому числу в диапазоне от 1 до 12
# 3. Год должен приводиться к целому положительному числу в диапазоне от 1 до 9999
# 4. Длина исходной строки для частей должна быть в соответствии с форматом 
#  (т.е. 2 символа для дня, 2 - для месяца, 4 - для года)

# Пример корректной даты
date = '01.11.1985'

# Примеры некорректных дат
date = '01.22.1001'
date = '1.12.1001'
date = '-2.10.3001'


def task_2():
    import re
    import calendar

    input_date = input('Input date:\n')
    format_regex = '([\d]{2}).([\d]{2}).([\d]{4})'

    match = re.match(format_regex, input_date)
    if match is None:
        print('Incorrect date format')
        return

    day = int(match.group(1))
    month = int(match.group(2))
    year = int(match.group(3))

    if year == 0:
        print('Year is incorrect')
        return

    if month < 1 or month > 12:
        print('Month out of range')
        return

    days_in_month = calendar.monthrange(year, month)[1]
    if day < 1 or day > days_in_month:
        print('Day out of range')
        return

    print('Date is correct')


# Задание-3: "Перевёрнутая башня" (Задача олимпиадного уровня)
#
# Вавилонцы решили построить удивительную башню —
# расширяющуюся к верху и содержащую бесконечное число этажей и комнат.
# Она устроена следующим образом — на первом этаже одна комната,
# затем идет два этажа, на каждом из которых по две комнаты, 
# затем идёт три этажа, на каждом из которых по три комнаты и так далее:
#         ...
#     12  13  14
#     9   10  11
#     6   7   8
#       4   5
#       2   3
#         1
#
# Эту башню решили оборудовать лифтом --- и вот задача:
# нужно научиться по номеру комнаты определять,
# на каком этаже она находится и какая она по счету слева на этом этаже.
#
# Входные данные: В первой строчке задан номер комнаты N, 1 ≤ N ≤ 2 000 000 000.
#
# Выходные данные:  Два целых числа — номер этажа и порядковый номер слева на этаже.
#
# Пример:
# Вход: 13
# Выход: 6 2
#
# Вход: 11
# Выход: 5 3


def task_3():
    import math

    num = int(input('Enter the number:\n'))

    if num < 1 or num > 2000000000:
        print('Incorrect input')
        return

    cur_lvl = 1
    lvl_2 = 1
    while lvl_2 ** 2 < num:
        num -= lvl_2 ** 2
        lvl_2 += 1
        cur_lvl += lvl_2

    cur_lvl -= lvl_2 - math.ceil(num / lvl_2)
    left_num = num % lvl_2
    if left_num == 0:
        left_num = lvl_2
    print(f'Level - {cur_lvl}\nLeft_side_num - {left_num}')


def print_reverse_pyramid(block_count=10, use_separate=True):
    total = 0
    text = []
    for i in range(block_count):
        for j in range(i):
            mess = ''
            for m in range(i):
                total += 1
                mess += f'{total:>3} '
            text.append(f'{mess:^75}')
        if use_separate:
            text.append('\n')
    for t in text[::-1]:
        print(t)


exit_flag = False
tasks = {
    '1': task_1,
    '2': task_2,
    '3': task_3,
    '4': print_reverse_pyramid
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
