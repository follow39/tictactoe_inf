import random

FREE = '·'  # символ пустой клетки
PLAYER = 'O'  # символ первого игрока
COMPUTER = 'X'  # символ второго игрока
IN_A_ROW = 5  # число клеток, необходимое для победы
BASIC_SIZE = IN_A_ROW * 2 - 3  # начальный размер стороны поля

current_size = BASIC_SIZE
move_counter = 1  # счетчик ходов
player = ''  # переменная для хранения текущего игрока
last_move = 0  # переменная для хранения прошлого хода

board = [FREE for i in range(0, BASIC_SIZE ** 2)]

list_c = []  # список для хранения цепочек из символов пользователя
list_c_self = []  # список для хранения цепочек из символов компьютера


class chain:
    p1 = tuple  # координаты начала
    p2 = tuple  # координаты конца
    length = 0  # длина
    p1_close = False  # ограничение со стороны p1
    p2_close = False  # ограничение со стороны p2
    # h- горизонтальное направление, v - вертикальное, d - диагональное
    dir = 'h'


# функция для печати поля
def print_board(board):
    x = 1
    end = ''

    # печать первой строки с номерами столбцов
    print('\n# |\t', end='')
    for i in range(1, current_size + 1):
        end = ''
        if i < 10:
            end += ' '
        end += '|\t'
        print(i, end=end)
    end = ''
    end += '\n'
    end += '----'
    end += '----' * current_size
    end += '\n'
    print('', end=end)  # печать полосы под строкой с номерами столбцов

    # печать поля
    for i in board:
        if x % current_size == 1:
            end = ''
            if x // current_size < 9:
                end += ' '
            end += '|\t'
            print(x // current_size + 1, end=end)  # печать номера строки
        end = ' |\t'
        if x % current_size == 0:
            end = ' |\n'
            if i != 1:
                end += '----'
                end += '----' * current_size
                end += '\n'
        x += 1
        print(i, end=end)  # печать клетки


# функция для хода, принимает в качестве аргумента текущего игрока
def move(player, board, current_size):
    n = 0

    if player == PLAYER:
        n, board, current_size = input_move(board, current_size)

        while not is_free(n, board):  # пока не введена свободная клетка
            print(
                'Эта клетка уже занята, выберите другую!\n'
                'Для продолжения нажмите любую клавишу...')  # вывод сообщения
            input()  # ожидание нажатия клавиши
            n, board, current_size = input_move(board, current_size)
    else:
        n = move_c()
        if n % current_size > current_size - 2:
            board, current_size = resize_board(current_size + 2, board,
                                               current_size)
        else:
            if n > current_size ** 2 - current_size:
                board, current_size = resize_board(current_size + 2, board,
                                                   current_size)

    board[n] = player  # запись хода
    return n, board, current_size


# функция для проверки занятости клетки
def is_free(n, board):
    if board[n] == FREE:
        return True  # возврат значения
    return False  # возврат значения


# функция для ввода хода
def input_move(board, current_size):
    print('Введите номер строки - ', end='')  # вывод сообщения о вводе данных
    i = int(input())  # ввод строки
    print('Введите номер столбца - ', end='')  # вывод сообщения о вводе данных
    j = int(input())  # ввод столбца

    if i >= current_size:  # проверка выхода за границы поля
        board, current_size = resize_board(i + 1, board, current_size)
    if j >= current_size:  # проверка выхода за границы поля
        board, current_size = resize_board(j + 1, board, current_size)

    result = (i - 1) * current_size + (j - 1)  # номер клетки в новом поле

    return result, board, current_size  # возврат результата


# функция для изменения размеров поля
def resize_board(new_side, board, current_size):
    new_board = [FREE for i in range(0, new_side ** 2)]  # создание нового поля

    shift = 0  # переменная сдвига

    for i in range(1, current_size ** 2):
        if i % current_size == 0:
            shift += new_side
        new_board[i % current_size + shift - 1] = board[i - 1]

    return new_board, new_side


# функция для проверки условия победы
def win_condition(player):
    # проверка победы по горизонтали
    counter = 1  # обнуление счетчика
    # цикл от 1 до количества клеток, которое необходимо для победы
    for i in range(1, IN_A_ROW):
        if board[last_move + i] == player:
            counter += 1  # увеличение счетчика
        else:
            break
    # цикл от 1 до количества клеток, которое необходимо для победы
    for i in range(1, IN_A_ROW):
        if last_move - i >= last_move - last_move % current_size:
            if board[last_move - i] == player:
                counter += 1  # увеличение счетчика
        else:
            break
    if counter >= IN_A_ROW:  #
        return True

    # проверка победы по вертикали
    counter = 1  # обнуление счетчика
    # цикл от 1 до количества клеток, которое не  обходимо для победы
    for i in range(1, IN_A_ROW + 1):
        if board[last_move + i * current_size] == player:
            counter += 1  # увеличение счетчика
        else:
            break
    # цикл от 1 до количества клеток, которое необходимо для победы
    for i in range(1, IN_A_ROW + 1):
        if last_move - i * current_size >= 0 % current_size:
            if board[last_move - i * current_size] == player:
                counter += 1  # увеличение счетчика
        else:
            break
    if counter >= IN_A_ROW:  #
        return True

    # проверка победы по диагонали
    counter = 1  # обнуление счетчика
    # цикл от 1 до количества клеток, которое необходимо для победы
    for i in range(1, IN_A_ROW + 1):
        if board[last_move + i * current_size + i] == player:
            counter += 1  # увеличение счетчика
        else:
            break
    # цикл от 1 до количества клеток, которое необходимо для победы
    for i in range(1, IN_A_ROW + 1):
        if last_move - i * current_size - i >= 0 % current_size:
            if board[last_move - i * current_size - i] == player:
                counter += 1  # увеличение счетчика
        else:
            break
    if counter >= IN_A_ROW:
        return True

    return False


def move_c():
    list_c.clear()
    list_c_self.clear()

    # выявление цепочек противника
    # проверка по горизонтали
    for i in range(0, current_size ** 2):
        k = i // current_size  # номер строки

        if i - 1 >= 0 and board[i - 1] == PLAYER:
            continue

        if board[i] == PLAYER and board[i + 1] == PLAYER:
            for j in range(1, IN_A_ROW + 1):
                if board[i + j] != PLAYER:
                    ch = chain()
                    ch.p1 = (k, i % current_size)
                    ch.p2 = (k, i % current_size + j - 1)
                    ch.length = j
                    ch.p1_close = True if (i - 1 < 0 or board[
                        i - 1] == COMPUTER) else False
                    ch.p2_close = True if board[i + j] == COMPUTER else False
                    ch.dir = 'h'
                    list_c.append(ch)
                    break
            continue
    # проверка по вертикали
    for i in range(0, current_size ** 2):
        k = i // current_size  # номер строки

        if k - 1 >= 0 and board[i - current_size] == PLAYER:
            continue

        if board[i] == PLAYER and board[i + current_size] == PLAYER:
            for j in range(1, IN_A_ROW + 1):
                if board[i + j * current_size] != PLAYER:
                    ch = chain()
                    ch.p1 = (k, i % current_size)
                    ch.p2 = (k + j - 1, i % current_size)
                    ch.length = j
                    ch.p1_close = True if (k - 1 < 0 or board[
                        i - current_size] == COMPUTER) else False
                    ch.p2_close = True if \
                        board[i + j * current_size] == COMPUTER else False
                    ch.dir = 'v'
                    list_c.append(ch)
                    break
            continue
    # проверка по диагонали
    for i in range(0, current_size ** 2):
        k = i // current_size  # номер строки

        if i - 1 >= 0 and k - 1 >= 0 and board[i - 1 - current_size] == PLAYER:
            continue

        if board[i] == PLAYER and board[i + 1 + current_size] == PLAYER:
            for j in range(1, IN_A_ROW + 1):
                if board[i + j + j * current_size] != PLAYER:
                    ch = chain()
                    ch.p1 = (k, i % current_size)
                    ch.p2 = (k + j - 1, i % current_size + j - 1)
                    ch.length = j
                    ch.p1_close = True \
                        if ((i % current_size == 0) or
                            (i - 1 < 0 and k - 1 < 0) or
                            board[i - 1 - current_size] == COMPUTER) \
                        else False
                    ch.p2_close = True \
                        if board[i + j + j * current_size] == COMPUTER \
                        else False
                    ch.dir = 'd'
                    list_c.append(ch)
                    break
            continue

    # выявление своих цепочек
    # проверка по горизонтали
    for i in range(0, current_size ** 2):
        k = i // current_size  # номер строки

        if i - 1 >= 0 and board[i - 1] == COMPUTER:
            continue

        if board[i] == COMPUTER and board[i + 1] == COMPUTER:
            for j in range(1, IN_A_ROW + 1):
                if board[i + j] != COMPUTER:
                    ch = chain()
                    ch.p1 = (k, i % current_size)
                    ch.p2 = (k, i % current_size + j - 1)
                    ch.length = j
                    ch.p1_close = True \
                        if (i - 1 < 0 or board[i - 1] == PLAYER or
                            (i // current_size) != ((i - 1) // current_size)) \
                        else False
                    ch.p2_close = True if board[i + j] == PLAYER else False
                    ch.dir = 'h'
                    list_c_self.append(ch)
                    break
            continue
    # проверка по вертикали
    for i in range(0, current_size ** 2):
        k = i // current_size  # номер строки

        if k - 1 >= 0 and board[i - current_size] == COMPUTER:
            continue

        if board[i] == COMPUTER and board[i + current_size] == COMPUTER:
            for j in range(1, IN_A_ROW + 1):
                if board[i + j * current_size] != COMPUTER:
                    ch = chain()
                    ch.p1 = (k, i % current_size)
                    ch.p2 = (k + j - 1, i % current_size)
                    ch.length = j
                    ch.p1_close = True if (k - 1 < 0 or board[
                        i - current_size] == PLAYER) else False
                    ch.p2_close = True \
                        if board[i + j * current_size] == PLAYER else False
                    ch.dir = 'v'
                    list_c_self.append(ch)
                    break
            continue
    # проверка по диагонали
    for i in range(0, current_size ** 2):
        k = i // current_size  # номер строки

        if i - 1 >= 0 and k - 1 >= 0 and \
                board[i - 1 - current_size] == COMPUTER:
            continue

        if board[i] == COMPUTER and board[i + 1 + current_size] == COMPUTER:
            for j in range(1, IN_A_ROW + 1):
                if board[i + j + j * current_size] != COMPUTER:
                    ch = chain()
                    ch.p1 = (k, i % current_size)
                    ch.p2 = (k + j - 1, i % current_size + j - 1)
                    ch.length = j
                    ch.p1_close = True \
                        if ((i - 1 < 0 and k - 1 < 0) or
                            board[i - 1 - current_size] != PLAYER or
                            (i // current_size) ==
                            ((i - 1 - current_size) // current_size)) \
                        else False
                    ch.p2_close = True \
                        if board[i + j + j * current_size] == PLAYER else False
                    ch.dir = 'd'
                    list_c_self.append(ch)
                    break
            continue

    # проверка победы 1 ходом
    for l in list_c_self:
        if l.length + 1 == IN_A_ROW and (not l.p1_close or not l.p2_close):
            if l.dir == 'h':
                if not l.p1_close:
                    return l.p1[0] * current_size + (l.p1[1] - 1)
                if not l.p2_close:
                    return l.p2[0] * current_size + (l.p2[1] + 1)
            if l.dir == 'v':
                if not l.p1_close:
                    return (l.p1[0] - 1) * current_size + l.p1[1]
                if not l.p2_close:
                    return (l.p2[0] + 1) * current_size + l.p2[1]
            if l.dir == 'd':
                if not l.p1_close:
                    return (l.p1[0] - 1) * current_size + (l.p1[1] - 1)
                if not l.p2_close:
                    return (l.p2[0] + 1) * current_size + (l.p2[1] + 1)

    # проверка победы противника на его следующий ход
    for l in list_c:
        if l.length + 1 == IN_A_ROW and (not l.p1_close or not l.p2_close):
            if l.dir == 'h':
                if not l.p1_close:
                    return l.p1[0] * current_size + (l.p1[1] - 1)
                if not l.p2_close:
                    return l.p2[0] * current_size + (l.p2[1] + 1)
            if l.dir == 'v':
                if not l.p1_close:
                    return (l.p1[0] - 1) * current_size + l.p1[1]
                if not l.p2_close:
                    return (l.p2[0] + 1) * current_size + l.p2[1]
            if l.dir == 'd':
                if not l.p1_close:
                    return (l.p1[0] - 1) * current_size + (l.p1[1] - 1)
                if not l.p2_close:
                    return (l.p2[0] + 1) * current_size + (l.p2[1] + 1)

    # поиск победы в 2 хода
    for l in list_c_self:
        if l.length + 2 == IN_A_ROW and (not l.p1_close or not l.p2_close):
            if l.dir == 'h':
                if not l.p1_close:
                    return l.p1[0] * current_size + (l.p1[1] - 1)
                if not l.p2_close:
                    return l.p2[0] * current_size + (l.p2[1] + 1)
            if l.dir == 'v':
                if not l.p1_close:
                    return (l.p1[0] - 1) * current_size + l.p1[1]
                if not l.p2_close:
                    return (l.p2[0] + 1) * current_size + l.p2[1]
            if l.dir == 'd':
                if not l.p1_close:
                    return (l.p1[0] - 1) * current_size + (l.p1[1] - 1)
                if not l.p2_close:
                    return (l.p2[0] + 1) * current_size + (l.p2[1] + 1)

    # ограничение цепочек противника длиной 3
    for l in list_c:
        if l.length + 2 == IN_A_ROW and (not l.p1_close or not l.p2_close):
            if l.dir == 'h':
                if not l.p1_close:
                    return l.p1[0] * current_size + (l.p1[1] - 1)
                if not l.p2_close:
                    return l.p2[0] * current_size + (l.p2[1] + 1)
            if l.dir == 'v':
                if not l.p1_close:
                    return (l.p1[0] - 1) * current_size + l.p1[1]
                if not l.p2_close:
                    return (l.p2[0] + 1) * current_size + l.p2[1]
            if l.dir == 'd':
                if not l.p1_close:
                    return (l.p1[0] - 1) * current_size + (l.p1[1] - 1)
                if not l.p2_close:
                    return (l.p2[0] + 1) * current_size + (l.p2[1] + 1)

    # поиск победы в 3 хода
    for l in list_c_self:
        if l.length + 3 == IN_A_ROW and (not l.p1_close or not l.p2_close):
            if l.dir == 'h':
                if not l.p1_close:
                    return l.p1[0] * current_size + (l.p1[1] - 1)
                if not l.p2_close:
                    return l.p2[0] * current_size + (l.p2[1] + 1)
            if l.dir == 'v':
                if not l.p1_close:
                    return (l.p1[0] - 1) * current_size + l.p1[1]
                if not l.p2_close:
                    return (l.p2[0] + 1) * current_size + l.p2[1]
            if l.dir == 'd':
                if not l.p1_close:
                    return (l.p1[0] - 1) * current_size + (l.p1[1] - 1)
                if not l.p2_close:
                    return (l.p2[0] + 1) * current_size + (l.p2[1] + 1)

    # ход рядом с одним из прошлых ходов
    for i in range(0, current_size ** 2):
        if board[i] == COMPUTER:
            if i - 1 >= 0 and not i % current_size == 0 \
                    and is_free(i - 1, board):
                return i - 1
            if is_free(i + 1, board):
                return i + 1
            if i - current_size >= 0 and is_free(i - current_size, board):
                return i - current_size
            if is_free(i + current_size, board):
                return i + current_size

    # случайный ход в непонятной ситуации
    i = current_size ** 2 // 3
    while True:
        if is_free(i, board):
            return i
        i += random.randrange(-7, 7)
        if i < 0:
            i = 15


# начало программы
print_board(board)  # печать игрового поля
while not win_condition(player):  # проверка условия победы
    player = COMPUTER if move_counter % 2 == 1 else PLAYER  # выбор игрока
    last_move, board, current_size = move(player, board, current_size)
    print_board(board)  # печать игрового поля
    move_counter += 1  # увеличение счетчика ходов
print('Победил ' + player)  # вывод победителя
