import os
import shutil


# Задача-1:
# Напишите скрипт, создающий директории dir_1 - dir_9 в папке,
# из которой запущен данный скрипт.
# И второй скрипт, удаляющий эти папки.


def create_directory_in_work_dir(dir_path):
    path = os.path.join(os.getcwd(), dir_path)
    try:
        os.makedirs(path)
        return True
    except:
        return False


def remove_directory_in_work_dir(dir_path):
    path = os.path.join(os.getcwd(), dir_path)
    if not os.path.isdir(path):
        return False
    try:
        os.removedirs(path)
        return True
    except:
        return False


def task_1():
    dirs = []
    for i in range(1, 10):
        d = f'dir_{i}'
        create_directory_in_work_dir(d)
        dirs.append(d)
    input('Press ENTER to remove dirs')
    for d in dirs:
        remove_directory_in_work_dir(d)


# Задача-2:
# Напишите скрипт, отображающий папки текущей директории.


def get_list_dir():
    work_dir = os.getcwd()
    return [d for d in os.listdir(work_dir) if os.path.isdir(f'{work_dir}//{d}')]


# Задача-3:
# Напишите скрипт, создающий копию файла, из которого запущен данный скрипт.


def duplicate_exec_file():
    file = os.path.basename(__file__)
    shutil.copyfile(__file__, f'{__file__.replace(file,"copy_"+file)}')


def main():
    exit_flag = False
    tasks = {
        '1': task_1,
        '2': lambda: print(get_list_dir()),
        '3': duplicate_exec_file,
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


if __name__ == '__main__':
    main()
