# Задание-1:
# Матрицы в питоне реализуются в виде вложенных списков:
# Пример. Дано:
matrix = [[1, 0, 8],
          [3, 4, 1],
          [0, 4, 2]]
          
# Выполнить поворот (транспонирование) матрицы
# Пример. Результат:
# matrix_rotate = [[1, 3, 0],
#                  [0, 4, 4],
#                  [8, 1, 2]]

# Суть сложности hard: Решите задачу в одну строку


def get_matrix_format(matrix_array):
    return '\n'.join([str(i) for i in matrix_array])


def task_1():

    t_matrix = [[matrix[j][i] for j in range(len(matrix[i]))] for i in range(len(matrix))]
    print(f'Before rotate:\n{get_matrix_format(matrix)}\n')
    print(f'After rotate:\n{get_matrix_format(t_matrix)}\n')


# Задание-2:
# Найдите наибольшее произведение пяти последовательных цифр в 1000-значном числе.
# Выведите произведение и индекс смещения первого числа последовательных 5-ти цифр.
# Пример 1000-значного числа:
number = """
73167176531330624919225119674426574742355349194934
96983520312774506326239578318016984801869478851843
85861560789112949495459501737958331952853208805511
12540698747158523863050715693290963295227443043557
66896648950445244523161731856403098711121722383113
62229893423380308135336276614282806444486645238749
30358907296290491560440772390713810515859307960866
70172427121883998797908792274921901699720888093776
65727333001053367881220235421809751254540594752243
52584907711670556013604839586446706324415722155397
53697817977846174064955149290862569321978468622482
83972241375657056057490261407972968652414535100474
82166370484403199890008895243450658541227588666881
16427171479924442928230863465674813919123162824586
17866458359124566529476545682848912883142607690042
24219022671055626321111109370544217506941658960408
07198403850962455444362981230987879927244284909188
84580156166097919133875499200524063689912560717606
05886116467109405077541002256983155200055935729725
71636269561882670428252483600823257530420752963450"""


def multiplication_elements(array):
    result = 1
    for i in array:
        result *= i
    return result


def get_max_multipl_in_list(string, size_line):
    queue = []
    index = 0
    max_index = 0
    max_mult = 1
    max_queue = []
    for n in string:
        if len(queue) >= size_line:
            queue.pop(0)
        queue.append(int(n))
        index += 1
        if len(queue) == size_line:
            temp = multiplication_elements(queue)
            if temp > max_mult:
                max_mult = temp
                max_queue = list(queue)
                max_index = index

    return max_queue, max_index - size_line


def task_2():
    size_line = 5
    num_without_returns = number.replace('\n', '')
    line, shift = get_max_multipl_in_list(num_without_returns, size_line)
    print(f'Line:{line}\nMax multiplication: {multiplication_elements(line)}\nShift: {shift}')
    print(f'Shift of origin num: {num_without_returns[shift:shift+size_line]}')

# Задание-3 (Ферзи):
# Известно, что на доске 8×8 можно расставить 8 ферзей так, чтобы они не били
# друг друга. Вам дана расстановка 8 ферзей на доске.
# Определите, есть ли среди них пара бьющих друг друга.
# Программа получает на вход восемь пар чисел,
# каждое число от 1 до 8 — координаты 8 ферзей.
# Если ферзи не бьют друг друга, выведите слово NO, иначе выведите YES.


board = []

temp_points = {
    1: [0, 7],
    2: [1, 6],
    3: [2, 5],
    4: [3, 4],
    5: [4, 3],
    6: [5, 2],
    7: [6, 1],
    8: [7, 0],
}

no_att_points = {
    1: [0, 6],
    2: [1, 3],
    3: [2, 1],
    4: [3, 7],
    5: [4, 5],
    6: [5, 0],
    7: [6, 2],
    8: [7, 4],
}


def get_chess_board():
    return [[0 for i in range(8)] for j in range(8)]


def set_queens_on_board(queens):
    global board
    board = get_chess_board()
    for n, p in queens.items():
        set_queen_on_board(p, n)
    print(f'Positions:\n{get_matrix_format(board)}\n')


def set_queen_on_board(queen, n):
    board[queen[0]][queen[1]] = n


def check_queen_attacks(queen, n):

    def __check_point(x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            if board[x][y] not in [0, n]:
                attacked_queens.append([x, y])

    attacked_queens = []

    for i in range(8):
        # check horizontal
        __check_point(queen[0], i)
        # check vertical
        __check_point(i, queen[1])

        # check diagonal_1
        x_1, y_1 = queen[0] - 1, queen[1] - 1
        x_2, y_2 = queen[0] + 1, queen[1] + 1
        __check_point(x_1, y_1)
        __check_point(x_2, y_2)

        # check diagonal_2
        d_1, d_2 = queen[0] + queen[1] - i, i
        __check_point(d_1, d_2)
        __check_point(d_2, d_1)

    return attacked_queens


def test_queens(queens):
    set_queens_on_board(queens)
    for n, p in queens.items():
        attacks = check_queen_attacks(p, n)
        if len(attacks) != 0:
            print('YES')
            break
    else:
        print('NO')


def task_3():

    print('Test run:\n')
    test_queens(temp_points)
    print(f'{"-"*20}')

    print('No attack run:\n')
    test_queens(no_att_points)
    print(f'{"-"*20}')

    print('Manual run:\n')
    queens = {}
    for i in range(1, 9):
        queens[i] = [int(f) for f in input(f'Enter position of Queen {i} (the separate by \' , \' )').split(',')]
    test_queens(queens)
    print(f'{"-"*20}')


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