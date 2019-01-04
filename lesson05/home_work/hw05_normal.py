import os
import hw05_easy as easy

# Задача-1:
# Напишите небольшую консольную утилиту,
# позволяющую работать с папками текущей директории.
# Утилита должна иметь меню выбора действия, в котором будут пункты:
# 1. Перейти в папку
# 2. Просмотреть содержимое текущей папки
# 3. Удалить папку
# 4. Создать папку
# При выборе пунктов 1, 3, 4 программа запрашивает название папки
# и выводит результат действия: "Успешно создано/удалено/перешел",
# "Невозможно создать/удалить/перейти"

# Для решения данной задачи используйте алгоритмы из задания easy,
# оформленные в виде соответствующих функций,
# и импортированные в данный файл из easy.py


def enter_dir_name():
    return input('Enter directory name:\n')


def get_result_operation(func, action_name):
    if func():
        return f'{action_name} is Successful'
    else:
        return f'{action_name} is Failure'


def move_to_dir(dir_name):
    try:
        os.chdir(dir_name)
        return True
    except:
        return False


def main():
    exit_flag = False

    def __exit():
        nonlocal exit_flag
        exit_flag = True
        return 'Exit'

    move_action = lambda: move_to_dir(enter_dir_name())
    remove_action = lambda: easy.remove_directory_in_work_dir(enter_dir_name())
    create_action = lambda: easy.create_directory_in_work_dir(enter_dir_name())

    tasks = [
        {'id': '1', 'name': 'Перейти в папку', 'action': lambda: get_result_operation(move_action, 'Move')},
        {'id': '2', 'name': 'Просмотреть содержимое текущей папки', 'action': easy.get_list_dir},
        {'id': '3', 'name': 'Удалить папку', 'action': lambda: get_result_operation(remove_action, 'Remove')},
        {'id': '4', 'name': 'Создать папку', 'action': lambda: get_result_operation(create_action, 'Create')},
        {'id': '0', 'name': 'Выход', 'action': lambda: __exit()},
    ]

    while not exit_flag:
        actions = '\n'.join([f"{t['id']}. {t['name']}" for t in tasks])
        answer = input(f'Select action:\n{actions}\n')

        sel_task = [t['action'] for t in tasks if t['id'] == answer]
        if sel_task:
            print(f'Result:\n{sel_task[0]()}\n')
        else:
            print('Incorrect task number')

        if not exit_flag:
            input("="*15)


if __name__ == '__main__':
    main()
