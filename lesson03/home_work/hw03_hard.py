# Задание-1:
# Написать программу, выполняющую операции (сложение и вычитание) с простыми дробями.
# Дроби вводятся и выводятся в формате:
# n x/y ,где n - целая часть, x - числитель, у - знаменатель.
# Дроби могут быть отрицательные и не иметь целой части, или иметь только целую часть.
# Примеры:
# Ввод: 5/6 + 4/7 (всё выражение вводится целиком в виде строки)
# Вывод: 1 17/42  (результат обязательно упростить и выделить целую часть)
# Ввод: -2/3 - -2
# Вывод: 1 1/3
import re
import math
import os


class Fraction:

    fraction_regex = '(?P<Mark>\-)?(?:(?:(?P<Total>[\d]* )?(?:(?P<Num>[\d]+)\/(?P<Denom>[\d]+)))|(?P<Total_2>[\d]*))'

    full_part = 0
    numerator = 0
    denominator = 1

    def __init__(self, fraction_string):

        m = re.match(self.fraction_regex, fraction_string)

        mark = m.group('Mark')
        total = m.group('Total')
        if total is None:
            total = m.group('Total_2')
        num = m.group('Num')
        den = m.group('Denom')

        if mark is None:
            mark = '+'
        if total is not None:
            self.full_part = int(f'{total}')
        if num is not None or den is not None:
            self.numerator = int(num)
            self.denominator = int(den)
        self.__fraction_without_full_part()
        self.numerator = self.numerator * int(f'{mark}1')

    def __str__(self):
        mark = lambda x: '' if x >= 0 else '-'
        full = math.floor(abs(self.numerator) / self.denominator)
        out = lambda y: f'{y} ' if y != 0 else ''
        part = abs(self.numerator) % self.denominator
        part_side = ''
        if part != 0:
            part_side = f'{part}/{self.denominator}'
        return f'{mark(self.numerator)}{out(full)}{part_side}'

    def __fraction_without_full_part(self):
        self.numerator += self.full_part * self.denominator
        self.full_part = 0

    def __create_common_denominator(self, fraction):

        cur_den = self.denominator

        self.denominator = self.denominator * fraction.denominator
        self.numerator = self.numerator * fraction.denominator

        fraction.denominator = fraction.denominator * cur_den
        fraction.numerator = fraction.numerator * cur_den

        return fraction

    def add(self, fraction):

        if self.denominator != fraction.denominator:
            self.__create_common_denominator(fraction)
        self.numerator += fraction.numerator

    def sub(self, fraction):

        if self.denominator != fraction.denominator:
            self.__create_common_denominator(fraction)
        self.numerator -= fraction.numerator


def parse_expression(expression):

    reqex = Fraction.fraction_regex
    fraction_array = []
    match = re.match(reqex, expression)
    operators = []

    while match.group(0) is not '':
        fraction_array.append(Fraction(match.group(0).strip()))
        expression = expression.replace(match.group(0), '', 1).strip()
        if len(expression) == 0:
            break
        operators.append(expression[0])
        expression = expression[1:].strip()
        match = re.match(reqex, expression)
    return fraction_array, operators


def parse_and_calc_expression(expression):

    fraction_array, operators = parse_expression(expression)

    for i in range(len(operators)):
        if operators[i] is '+':
            fraction_array[0].add(fraction_array[i+1])
        else:
            fraction_array[0].sub(fraction_array[i + 1])

    return fraction_array[0]
    pass


def task_1():

    expression = input('Enter the expression:\n')
    print(parse_and_calc_expression(expression))


# Задание-2:
# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки
# они получают удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

class Worker:

    last_name = None
    first_name = None
    profession = None

    salary = 0
    time_norm = 0
    time_worked = 0

    def __init__(self, last_name, first_name, profession):
        self.last_name = last_name
        self.first_name = first_name
        self.profession = profession

    def __str__(self):

        fio = f'{self.last_name} {self.first_name}'
        prof = f'{self.profession} ({self.salary})'
        work = f'Work: {self.time_worked}/{self.time_norm}'
        total = f'Profit: {self.get_total_profit()}'

        return f'{fio:30}{prof:25}{work:20}{total}'

    def get_total_profit(self):

        sal_for_hour = self.salary / self.time_norm
        diff = self.time_worked - self.time_norm
        if diff == 0:
            bonus = 0
        elif diff > 0:
            bonus = diff * sal_for_hour * 2
        else:
            bonus = diff * sal_for_hour
        return round(self.salary + bonus, 2)


def parse_worker(data):
    workers_regex = '(?P<FN>[А-Яа-я]+)[\s]+(?P<LN>[А-Яа-я]+)[\s]+(?P<S>[\d]+)[\s]+(?P<P>[А-Яа-я]+)[\s]+(?P<N>[\d]+)'

    match = re.match(workers_regex, data)
    if len(match.groups()) != 5:
        return None
    worker = Worker(match.group('LN'), match.group('FN'), match.group('P'))
    worker.salary = int(match.group('S'))
    worker.time_norm = int(match.group('N'))
    return worker


def parse_hours(data):
    hours_regex = '(?P<FN>[А-Яа-я]+)[\s]+(?P<LN>[А-Яа-я]+)[\s]+(?P<W>[\d]+)'

    match = re.match(hours_regex, data)
    if len(match.groups()) != 3:
        return None

    return match.group('LN'), match.group('FN'), match.group('W')


def parse_files(workers_file, hours_file):

    workers = []

    with open(workers_file, 'r', encoding='utf-8') as file:
        for w in file.readlines()[1:]:
            worker = parse_worker(w)
            if worker is None:
                continue
            workers.append(worker)
    worked_list = []
    with open(hours_file, 'r', encoding='utf-8') as file:
        for h in file.readlines()[1:]:
            parsed = parse_hours(h)
            if len(parsed) != 3:
                continue
            worked_list.append(parsed)

    for i in worked_list:
        cur_worker = list(filter(lambda x: (x.last_name == i[0] and x.first_name == i[1]), workers))
        if len(cur_worker) != 0:
            cur_worker[0].time_worked = int(i[2])
        pass

    return workers


def task_2():
    workers = parse_files(workers_file='data//workers', hours_file='data//hours_of')
    for w in workers:
        print(w)
    pass

# Задание-3:
# Дан файл ("data/fruits") со списком фруктов.
# Записать в новые файлы все фрукты, начинающиеся с определенной буквы.
# Т.е. в одном файле будут все фрукты на букву “А”, во втором на “Б” и т.д.
# Файлы назвать соответственно.
# Пример имен файлов: fruits_А, fruits_Б, fruits_В ….
# Важно! Обратите внимание, что нет фруктов, начинающихся с некоторых букв.
# Напишите универсальный код, который будет работать с любым списком фруктов
# и распределять по файлам в зависимости от первых букв, имеющихся в списке фруктов.
# Подсказка:
# Чтобы получить список больших букв русского алфавита:
# print(list(map(chr, range(ord('А'), ord('Я')+1))))


OUTPUT_DIR = 'data\\fruits_output'
DEFAULT_NAME = 'fruits_'


def reset_files():
    if not os.path.isdir(OUTPUT_DIR):
        return
    for i in os.listdir(OUTPUT_DIR):
        file = f'{OUTPUT_DIR}\\{i}'
        if os.path.isfile(file):
            os.remove(file)


def write_into_file(content):
    char = content[0]
    filename = f'{OUTPUT_DIR}\\{DEFAULT_NAME}{char}.txt'
    if not os.path.isfile(filename):
        flag = 'w+'
    else:
        flag = 'a+'
    with open(filename, flag) as file:
        file.write(f'{content}\n')


def parse_fruits_file(filename):

    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    else:
        reset_files()

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if not (not line or line.isspace()):
                write_into_file(line)


def task_3():
    parse_fruits_file('data/fruits.txt')
    separator = ', \n'
    print(f"Files created:\n{separator.join(os.listdir(OUTPUT_DIR))}")
    pass


exit_flag = False
tasks = {
    '1': task_1,
    '2': task_2,
    '3': task_3,
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
