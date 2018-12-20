# Задача-1:
# Дан список фруктов.
# Напишите программу, выводящую фрукты в виде нумерованного списка,
# выровненного по правой стороне.

# Пример:
# Дано: ["яблоко", "банан", "киви", "арбуз"]
# Вывод:
# 1. яблоко
# 2.  банан
# 3.   киви
# 4.  арбуз

# Подсказка: воспользоваться методом .format()


def task_1():
    fruits = ["яблоко", "банан", "киви", "арбуз"]
    i = 0
    size = max((len(f) for f in fruits))
    for f in fruits:
        i += 1
        print(f'{i}. {f:>{size}}')  # print('{0}. {1:>{2}}'.format(i, f, size))


# Задача-2:
# Даны два произвольные списка.
# Удалите из первого списка элементы, присутствующие во втором списке.


def task_2():
    def print_array(message, arr1, arr2):

        print(f'{message:-^20}')
        print(f'First array: {arr1}')
        print(f'Second array: {arr2}')

    array_1 = [i.strip() for i in input('Enter values of first array (the separate by \' , \')').split(',')]
    array_2 = [i.strip() for i in input('Enter values of second array (the separate by \' , \')').split(',')]

    print_array('Input', array_1, array_2)

    del_array = []
    for item in array_1:
        if item in array_2:
            del_array.append(item)

    for d in del_array:
        array_1.remove(d)

    print_array('Output', array_1, array_2)


# Задача-3:
# Дан произвольный список из целых чисел.
# Получите НОВЫЙ список из элементов исходного, выполнив следующие условия:
# если элемент кратен двум, то разделить его на 4, если не кратен, то умножить на два.


def task_3():
    import random

    origin_array = [random.randint(0, 100) for i in range(15)]

    lambda_function = lambda item: item / 4 if item % 2 == 0 else item * 2
    new_array = [lambda_function(item) for item in origin_array]

    '''   
        for item in origin_array:
            if item % 2 == 0:
                new_array.append(item / 4)
            else:
                new_array.append(item * 2)
    '''

    print(f'Generated array: {origin_array}')
    print(f'New array: {new_array}')


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
