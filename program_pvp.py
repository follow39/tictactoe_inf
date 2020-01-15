FREE = '·'  # символ пустой клетки
PLAYER1 = 'O'  # символ первого игрока
PLAYER2 = 'X'  # символ второго игрока
IN_A_ROW = 5  # число клеток, необходимое для победы
BASIC_SIZE = 7  # начальный размер стороны поля

current_size = BASIC_SIZE
move_counter = 1  # счетчик ходов
player = ''  # переменная для хранения текущего игрока
last_move = 0  # переменная для хранения прошлого хода

board = [FREE for i in
         range(0, BASIC_SIZE ** 2)]  # переменная для хранения поля игры


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
    n, board, current_size = input_move(board,
                                        current_size)  # ввод номера клетки

    while not is_free(n, board):  # пока не введена свободная клетка
        print(
            'Эта клетка уже занята, выберите другую!\n'
            'Для продолжения нажмите любую клавишу...')  # вывод сообщения
        input()  # ожидание нажатия клавиши
        n, board, current_size = input_move(board, current_size)

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

    # цикл для копирования элементов из старого поля
    for i in range(1, current_size ** 2):
        # если номер ячейки кратен размеру стороны старого поля
        if i % current_size == 0:
            shift += new_side
        new_board[i % current_size + shift - 1] = board[
            i - 1]  # копирования i-1 значения из старого поля в новое

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


# начало программы
print_board(board)  # печать игрового поля
while not win_condition(player):  # проверка условия победы
    player = PLAYER1 if move_counter % 2 == 1 else PLAYER2  # выбор игрока
    print('\nХод игрока ' + player)
    last_move, board, current_size = move(player, board,
                                          current_size)  # ход игрока
    print_board(board)  # печать игрового поля
    move_counter += 1  # увеличение счетчика ходов
print('Победил ' + player)  # вывод победителя
