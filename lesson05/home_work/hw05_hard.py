# Задание-1:
# Доработайте реализацию программы из примера examples/5_with_args.py,
# добавив реализацию следующих команд (переданных в качестве аргументов):
#   cp <file_name> - создает копию указанного файла
#   rm <file_name> - удаляет указанный файл (запросить подтверждение операции)
#   cd <full_path or relative_path> - меняет текущую директорию на указанную
#   ls - отображение полного пути текущей директории
# путь считать абсолютным (full_path) -
# в Linux начинается с /, в Windows с имени диска,
# все остальные пути считать относительными.

# Важно! Все операции должны выполняться в той директории, в который вы находитесь.
# Исходной директорией считать ту, в которой был запущен скрипт.

# P.S. По возможности, сделайте кросс-платформенную реализацию.


import os
import sys
import shutil


def get_help():
    print(f'cp [filename] - {copy.__doc__}')
    print(f'rm [filename] - {remove.__doc__}')
    print(f'cd [dir_name] - {change_dir.__doc__}')
    print(f'ls - {get_dir_path.__doc__}')


def __check_exist_file(filename):
    return os.path.isfile(filename)


def copy(filename):
    """создает копию указанного файла"""
    if not __check_exist_file(filename):
        print('File not found')
        return
    file = os.path.basename(filename)
    new_filename = filename.replace(file, "copy_"+file)
    shutil.copyfile(filename, new_filename)
    print(f'Created file {new_filename}')


def remove(filename):
    """удаляет указанный файл"""
    if not __check_exist_file(filename):
        print('File not found')
        return
    answer = input(f'Remove {filename}?[Y/N]')
    if answer.upper() == 'Y':
        os.remove(filename)
        print(f'{filename} removed')
    else:
        print('Canceled')


def change_dir(dir_name):
    """меняет текущую директорию на указанную"""
    if os.path.isdir(dir_name):
        os.chdir(dir_name)
        get_dir_path()
    else:
        print('Directory not found')


def get_dir_path():
    """отображение полного пути текущей директории"""
    print(f'Current path:\n{os.getcwd()}')


commands = {
    'help': get_help,
    'cp': lambda: copy(sys.argv[2]),
    'rm': lambda: remove(sys.argv[2]),
    'cd': lambda: change_dir(sys.argv[2]),
    'ls': get_dir_path
}


if sys.argv[1] in commands.keys():
    commands[sys.argv[1]]()
