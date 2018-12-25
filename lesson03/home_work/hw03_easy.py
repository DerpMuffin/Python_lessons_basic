# Задание-1:
# Напишите функцию, округляющую полученное произвольное десятичное число
# до кол-ва знаков (кол-во знаков передается вторым аргументом).
# Округление должно происходить по математическим правилам (0.6 --> 1, 0.4 --> 0).
# Для решения задачи не используйте встроенные функции и функции из модуля math.


def my_round(number, ndigits):
    mark = lambda x: 1 if x >= 0 else -1
    ten_n = 10 ** ndigits
    temp = number * ten_n
    if abs(temp - int(temp)) >= 0.5:
        temp += mark(temp)
    result = int(temp) / ten_n
    return result


def task_1():
    print(my_round(2.1234567, 5))
    print(my_round(2.1999967, 5))
    print(my_round(2.9999967, 5))

    print(my_round(-2.1234567, 5))
    print(my_round(-2.1999967, 5))
    print(my_round(-2.9999967, 5))


# Задание-2:
# Дан шестизначный номер билета. Определить, является ли билет счастливым.
# Решение реализовать в виде функции.
# Билет считается счастливым, если сумма его первых и последних цифр равны.
# !!!P.S.: функция не должна НИЧЕГО print'ить


def lucky_ticket(ticket_number):
    import re

    lucky_regex = '([\d]{3})([\d]{3})'
    match = re.match(lucky_regex, str(ticket_number))

    if match is None:
        return 'Incorrect ticket number'

    left_nums = match.group(1)
    right_nums = match.group(2)

    lambda_sum = lambda nums: sum(int(n) for n in nums)

    left_sum = lambda_sum(left_nums)
    right_sum = lambda_sum(right_nums)

    result = (lambda left, right: 'Lucky' if left == right else 'Unlucky')(left_sum, right_sum)
    return f'Ticket is {result}'


def task_2():
    print(lucky_ticket(123006))
    print(lucky_ticket(12321))
    print(lucky_ticket(436751))


exit_flag = False
tasks = {
    '1': task_1,
    '2': task_2,
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


