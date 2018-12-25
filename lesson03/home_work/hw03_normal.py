# Задание-1:
# Напишите функцию, возвращающую ряд Фибоначчи с n-элемента до m-элемента.
# Первыми элементами ряда считать цифры 1 1


def fibonacci(n, m):

    fib_nums = []

    for i in range(m):
        if i in [0, 1]:
            fib_nums.append(1)
            continue
        fib_nums.append(fib_nums[i-1] + fib_nums[i-2])

    return fib_nums[n:]


def task_1():
    fib_range = [int(i) for i in input('Enter the range of fibonacci numbers (the separate by \' , \' )').split(',')]
    if len(fib_range) != 2 or False in list(x >= 0 for x in fib_range):
        print('Incorrect range')
        return
    _from = min(fib_range)
    to = max(fib_range)
    print(f"Fibonacci numbers from {_from} to {to}:\n{', '.join(str(n) for n in fibonacci(_from, to))}")
    pass

# Задача-2:
# Напишите функцию, сортирующую принимаемый список по возрастанию.
# Для сортировки используйте любой алгоритм (например пузырьковый).
# Для решения данной задачи нельзя использовать встроенную функцию и метод sort()


def sort_to_max(origin_list):

    array_size = len(origin_list)

    for i in range(0, array_size):
        for j in range(1, array_size-i):
            if origin_list[j] < origin_list[j-1]:
                origin_list[j], origin_list[j-1] = origin_list[j-1], origin_list[j]

    return origin_list


def task_2():
    test_array = [2, 10, -12, 2.5, 20, -11, 4, 4, 0]
    print(f'Before sort - {test_array}')
    print(f'After sort - {sort_to_max(test_array)}')

# Задача-3:
# Напишите собственную реализацию стандартной функции filter.
# Разумеется, внутри нельзя использовать саму функцию filter.


def override_filter(func, array):
    if func is None:
        return array
    for i in array:
        if func(i):
            yield i


def task_3():
    test_array = [0, 1, 5, 2, 8, 6, 7, 8, 2, 1]
    test_func = lambda x: x < 5

    print(f'Test data - {test_array}')
    result = override_filter(test_func, test_array)
    print(f'Result of override filter {list(result)}')
    print(f'Result of default filter  {list(filter(test_func, test_array))}')


# Задача-4:
# Даны четыре точки А1(х1, у1), А2(x2 ,у2), А3(x3 , у3), А4(х4, у4).
# Определить, будут ли они вершинами параллелограмма.

class Vector:

    start = None
    end = None

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_length(self):

        k1, k2 = self.get_legs()

        return (k1 ** 2 + k2 ** 2) ** (1/2)

    def check_equal_and_parallel(self, vector):

        cur_k1, cur_k2 = self.get_legs()
        vec_k1, vec_k2 = vector.get_legs()

        return cur_k1 == vec_k1 and cur_k2 == vec_k2

    def get_legs(self):
        k1 = abs(self.start[0] - self.end[0])
        k2 = abs(self.start[1] - self.end[1])
        return k1, k2


def check_vertices(vertices):

    vectors = []
    count = len(vertices)
    for i in range(count):
        vectors.append(Vector(vertices[i], vertices[((i+1) % count)]))

    return vectors[0].check_equal_and_parallel(vectors[2]) and vectors[1].check_equal_and_parallel(vectors[3])


def task_4():

    points = {}

    for i in range(1, 5):
        point_name = f'A{i}'
        point = [float(f) for f in input(f'Enter {point_name} point (the separate by \' , \' )').split(',')]
        points[point_name] = point

    print(f'Points: ')
    for k, v in points.items():
        print(f'{k}: ({v[0]}; {v[1]})')

    result = check_vertices([v for v in points.values()])
    lam = lambda r: 'ARE' if r else "AREN'T"
    print(f'Points {lam(result)} vertices of parallelogram')


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
