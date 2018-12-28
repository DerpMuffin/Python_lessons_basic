# Все задачи текущего блока решите с помощью генераторов списков!

# Задание-1:
# Дан список, заполненный произвольными целыми числами. 
# Получить новый список, элементы которого будут
# квадратами элементов исходного списка
# [1, 2, 4, 0] --> [1, 4, 16, 0]


def task_1():

    array = [int(i) for i in input('Enter values of array (the separate by \' , \')').split(',')]
    sq_array = [i ** 2 for i in array]
    print(sq_array)

# Задание-2:
# Даны два списка фруктов.
# Получить список фруктов, присутствующих в обоих исходных списках.


def task_2():

    fruits_1 = [i.strip() for i in input('Enter fruits of first array (the separate by \' , \')').split(',')]
    fruits_2 = [i.strip() for i in input('Enter fruits of second array (the separate by \' , \')').split(',')]
    cross_fruits = [f for f in fruits_1 if f in fruits_2]
    print(cross_fruits)

# Задание-3:
# Дан список, заполненный произвольными числами.
# Получить список из элементов исходного, удовлетворяющих следующим условиям:
# + Элемент кратен 3
# + Элемент положительный
# + Элемент не кратен 4


def task_3():

    array = [int(i) for i in input('Enter values of array (the separate by \' , \')').split(',')]
    filtered_array = [i for i in array if i % 3 == 0 and i > 0 and i % 4 != 0]
    print(filtered_array)


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
