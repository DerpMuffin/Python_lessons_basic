# Задание-1: Решите задачу (дублированную ниже):

# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки они получают
# удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

# С использованием классов.
# Реализуйте классы сотрудников так, чтобы на вход функции-конструктора
# каждый работник получал строку из файла


class Worker:

    workers_regex = '(?P<FN>[А-Яа-я]+)[\s]+(?P<LN>[А-Яа-я]+)[\s]+(?P<S>[\d]+)[\s]+(?P<P>[А-Яа-я]+)[\s]+(?P<N>[\d]+)'

    last_name = None
    first_name = None
    profession = None

    salary = 0
    time_norm = 0
    time_worked = 0

    def __init__(self, data_string):
        self.__parse_data(data_string)

    def __parse_data(self, data):
        import re
        match = re.match(self.workers_regex, data)
        self.last_name = match.group('LN')
        self.first_name = match.group('FN')
        self.profession = match.group('P')
        self.salary = int(match.group('S'))
        self.time_norm = int(match.group('N'))

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


def parse_hours(data):
    import re
    hours_regex = '(?P<FN>[А-Яа-я]+)[\s]+(?P<LN>[А-Яа-я]+)[\s]+(?P<W>[\d]+)'

    match = re.match(hours_regex, data)
    if len(match.groups()) != 3:
        return None

    return match.group('LN'), match.group('FN'), match.group('W')


def parse_files(workers_file, hours_file):

    workers = []
    with open(workers_file, 'r', encoding='utf-8') as file:
        for w in file.readlines()[1:]:
            workers.append(Worker(w))
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


if __name__ == '__main__':
    workers = parse_files(workers_file='data//workers', hours_file='data//hours_of')
    for w in workers:
        print(w)
