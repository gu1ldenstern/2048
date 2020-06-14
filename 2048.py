import pyxel
import numpy as np
from random import random, randint
from math import log
import json
import argparse

#############
# CONSTANTS #
#############
TABLE = np.zeros((4, 4), dtype=np.int)
MATRIX_OF_INDEXES = [[11, 25], [27, 25], [42, 25], [57, 25], [11, 40],
                     [27, 40], [42, 40], [57, 40], [11, 55], [27, 55],
                     [42, 55], [57, 55], [11, 70], [27, 70], [42, 70],
                     [57, 70]]
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 90
MUSIC = 1
SOUND_EFFECTS = 0
SCREEN_COLOR = 0
FIELD_COLOR = 13
DESIGN = -1
wins = 0
PALETTE = [0x000000, 0xFF6347, 0xFF7F50, 0xFFA500, 0xEFD334,
           0xD1E231, 0xB2EC5D, 0x30BA8F, 0x6495ED, 0x9370DB, 0xCD5C5C,
           0x434750, 0xFFF8DC, 0xB0C4DE, 0x08457E, 0xE0B0FF]

# даю возможность сделать случайные цвета через аргпарс

#создаю объект парсера
parser = argparse.ArgumentParser()
#создаю аргумент palette, который отвечает за включение рандомных цветов
parser.add_argument("-p", "--palette", type=str,
                            help="'random' to use random color scheme and"
                                 " 'def' to use default colors", default='def')
args = parser.parse_args()
#на случай, если пользователь введет некорректное значение
if args.palette not in ('random', 'def'):
    print('incorrect platte value, starting with a default value')
#собственно устанавливаю случайную палтру цветов
elif args.palette == 'random':
    PALETTE = np.random.permutation(PALETTE)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="1024",
                   palette=PALETTE)
        pyxel.load("2048.pyxres")
        self.field = TABLE.copy()
        self.design = 1
        self.wins = 0
        self.options = 1
        self.death = False
        self.win = False
        # звук когда игрок долго жмет на одну кнопку)))
        pyxel.sound(19).set(
            note="c3e3g3c4c4", tone="s", volume="7", effect=("n" * 4 + "f"),
            speed=7
        )
        # звук смерти
        pyxel.sound(29).set(
            note="f3 b2 f2 b1  f1 f1 f1 f1",
            tone="p",
            volume=("4" * 4 + "4321"),
            effect=("n" * 7 + "f"),
            speed=9,
        )
        add_random(self.field)
        pyxel.playm(MUSIC, loop=True)

        pyxel.run(self.update, self.draw)

    ###########
    # updates #
    ###########
    # кнопка R - обновление игры (т.е. смерти и выигрыша больше нет,
    # таблица очищается и туда ставится первое число

    def update(self):

        if pyxel.btn(pyxel.KEY_R):
            self.death = False
            self.win = False
            self.field = TABLE.copy()
            self.field = add_random(self.field)
            pyxel.stop()
            pyxel.playm(MUSIC, loop=True)

        # открытие меню настроек
        if pyxel.btn(pyxel.KEY_O):
            self.options = -1

        # обработка выхода из программы
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        # смена дизайна на первый или второй
        if pyxel.btn(pyxel.KEY_1):
            self.design = 1
        if pyxel.btn(pyxel.KEY_2):
            self.design = -1
        if pyxel.btn(pyxel.KEY_ENTER):
            pyxel.playm(MUSIC, loop=True)
        if pyxel.btn(pyxel.KEY_SPACE):
            pyxel.stop()
        # выход из меню настроек
        if pyxel.btn(pyxel.KEY_G):
            self.options = 1

        ####################
        # KEYS & MOVEMENTS #
        ####################
        # при нажатии кнопок движения таблица сдвигается в
        # соответствующую сторону

        if pyxel.btnp(pyxel.KEY_UP):  # IF USER PRESSES "UP"
            check = self.field.copy()
            move_up(self.field)
            # не ставлю новое число, если таблица осталась той же
            if not np.equal(self.field, check).all():
                self.field = add_random(self.field)
            else:
                pyxel.play(3, 19)
                if 0 not in self.field:
                    if death_event(self.field) == 0:
                        pyxel.play(3, 29)
                        self.death = True

        if pyxel.btnp(pyxel.KEY_DOWN):  # IF USER PRESSES "DOWN"
            check = self.field.copy()
            move_down(self.field)
            if not np.equal(self.field, check).all():
                self.field = add_random(self.field)
            else:
                pyxel.play(3, 19)
                if 0 not in self.field:
                    if death_event(self.field) == 0:
                        pyxel.play(3, 29)
                        self.death = True

        if pyxel.btnp(pyxel.KEY_RIGHT):  # IF USER PRESSES "RIGHT"
            check = self.field.copy()
            move_right(self.field)
            if not np.equal(self.field, check).all():
                self.field = add_random(self.field)
            else:
                pyxel.play(3, 19)
                if 0 not in self.field:
                    if death_event(self.field) == 0:
                        pyxel.play(3, 29)
                        self.death = True

        if pyxel.btnp(pyxel.KEY_LEFT):  # IF USER PRESSES "LEFT"
            check = self.field.copy()
            move_left(self.field)
            if not np.equal(self.field, check).all():
                self.field = add_random(self.field)
            else:
                pyxel.play(3, 19)
                if 0 not in self.field:
                    if death_event(self.field) == 0:
                        pyxel.play(3, 29)
                        self.death = True

    ###########
    # DRAWING #
    ###########

    def draw(self):
        # THAT'S WHERE I DRAW THE
        if not self.win:
            if not self.death:
                if self.options != -1:
                    if self.design == 1:
                        pyxel.cls(SCREEN_COLOR)
                        pyxel.blt(0, 0, 2, 0, 0, 30, 26)
                        pyxel.blt(55, 0, 2, 0, 0, 38, 26)
                        pyxel.rect(10, 20, 60, 60, FIELD_COLOR)
                    else:
                        pyxel.cls(15)
                        pyxel.blt(5, 5, 0, 0, 0, 20, 16)
                        pyxel.blt(60, 5, 0, 0, 0, 38, 16)
                        pyxel.rect(10, 20, 60, 60, 12)

                    pyxel.text(33, 10, "1024!", pyxel.frame_count % 16)

                    pyxel.line(25, 20, 25, 79, SCREEN_COLOR)
                    pyxel.line(40, 20, 40, 79, SCREEN_COLOR)
                    pyxel.line(55, 20, 55, 79, SCREEN_COLOR)

                    pyxel.line(10, 35, 69, 35, SCREEN_COLOR)
                    pyxel.line(10, 50, 69, 50, SCREEN_COLOR)
                    pyxel.line(10, 65, 69, 65, SCREEN_COLOR)

                    pyxel.text(0, 82, "press[o] for options",
                               pyxel.frame_count % 15)

                    # отрисовка новой таблицы с новыми значениями

                    table1 = self.field
                    table1 = table1.reshape(16, 1)
                    count = 0
                    for i in MATRIX_OF_INDEXES:
                        if table1[count][0] != 0:
                            pyxel.text(int(f'{i[0]}'), int(f'{i[1]}'),
                                       str(table1[count][0]),
                                       int(log(int(table1[count][0]), 2)))
                            if table1[count][0] == 1024:
                                self.win = True
                                pyxel.playm(7, loop=False)
                                filename = 'record.json'
                                try:
                                    with open(filename, 'r') as file:
                                        k = str(int(json.load(file)) + 1)
                                    with open(filename, 'w') as file:
                                        json.dump(k, file)
                                except FileNotFoundError:
                                    k = 1
                                    with open(filename, 'w') as file:
                                        json.dump(k, file)
                                self.wins = set_record()

                        count += 1
                else:
                    pyxel.cls(15)
                    pyxel.text(7, 7, "options:", pyxel.frame_count % 16)
                    pyxel.text(7, 20, "press [Q] to exit",
                               pyxel.frame_count % 16)
                    pyxel.text(7, 33, "press[1] or [2]",
                               pyxel.frame_count % 16)
                    pyxel.text(7, 41, "to choose design",
                               pyxel.frame_count % 16)
                    pyxel.text(7, 48, "press [space]",
                               pyxel.frame_count % 16)
                    pyxel.text(7, 54, "to stop msc",
                               pyxel.frame_count % 16)
                    pyxel.text(7, 62, "press [enter] ",
                               pyxel.frame_count % 16)
                    pyxel.text(7, 69, "to resume msc",
                               pyxel.frame_count % 16)
                    pyxel.text(7, 82, "[G]-back to game",
                               pyxel.frame_count % 16)
            else:
                pyxel.cls(0)
                pyxel.text(7, 7, "SRY YOU DIED", pyxel.frame_count % 16)
                pyxel.blt(25, 25, 1, 0, 0, 38, 26)
                pyxel.text(7, 62, "press [Q] to exit", pyxel.frame_count % 16)
                pyxel.text(0, 77, "press [R] to restart",
                           pyxel.frame_count % 16)
        else:
            pyxel.cls(0)
            pyxel.text(7, 7, "CONGRATS YOU WON ", pyxel.frame_count % 16)
            pyxel.text(7, 14, self.wins, pyxel.frame_count % 16)
            pyxel.blt(25, 25, 2, 0, 0, 38, 26)
            pyxel.text(7, 67, "press [Q] to exit", pyxel.frame_count % 16)
            pyxel.text(0, 77, "press [R] to restart", pyxel.frame_count % 16)


####################################
# NUMPY CALCULATIONS FOR MOVEMENTS #
####################################

# добавление числа (2 с вероятностью 85% или 4) на рандомную пустую клетку
def add_random(board):
    i, j = (board == 0).nonzero()
    if i.size != 0:
        rnd = randint(0, i.size - 1)
        board[i[rnd], j[rnd]] = 2 ** ((random() > 0.85) + 1)
        return board
    else:
        death_event(board)


# сдвиг влево - последовательный сдвиг всех 4 строк влево


def move_left(field):
    for i in range(len(field)):
        field[i] = movement(field[i])
    return field


"""
только функция move_left умеет нормально работать
с movement, остальные должны сначала преобразоваться в
сдвиг влево, потом сдвинуться влево, а потом трансформироваться
в свой сдвиг (вправо, вниз etc)
"""


def move_right(field):
    for i in range(len(field)):
        field[i] = movement(field[i][::-1])
        field[i] = field[i][::-1]
    return field


def move_down(field):
    field = move_right(field.transpose())
    return field.transpose


def move_up(field):
    field = move_left(field.transpose())
    return field.transpose


"""
тут я проверяю, умер игрок или нет.
если движение ни в одном направлении не дает
новую таблицу - умер
"""


def death_event(board):
    count = 0
    directions = ['move_up(check)', 'move_down(check)', 'move_right(check)',
                  'move_left(check)']
    for i in directions:
        check = board.copy()
        exec(i)
        # не ставлю новое число, если таблица осталась той же
        if np.equal(board,
                    check).all():
            count += 1
    if count == 4:
        return 0
    else:
        return 1


def set_record():
    filename = 'record.json'
    try:
        with open(filename) as file:
            k = json.load(file)
            k = "you won " + str(k) + ' times'
            return k
    except FileNotFoundError:
        return "you haven't won yet"


def movement(board):  # сдвигает одну строчку влево со складыванием

    """
    я устала писать красиво так что буду писать просто
    - я рассматриваю каждый вариант длины и для него пишу
    разные ифы, соответствующие разным вариантам перестановок
    и сложений. оно длинно для меня, но сравнительно
    просто и быстро для компа
    """
    board = board[board != 0]  # убираю нули
    length = len(board)  # пляшу от возможной длины массива без нулей

    if length == 2:
        if board[0] == board[1]:
            board[0] = board[1] + board[0]
            board[1] = 0
    elif length == 3:
        if board[0] == board[1]:
            board[0] = board[1] + board[0]
            board[1] = 0
        elif board[1] == board[2]:
            board[1] = board[1] + board[2]
            board[2] = 0
    elif length == 4:
        if board[0] == board[1]:
            board[0] = board[1] + board[0]
            board[1] = 0
            if board[2] == board[3]:
                board[2] = board[2] + board[3]
                board[3] = 0
        elif board[1] == board[2]:
            board[1] = board[1] + board[2]
            board[2] = 0
        elif board[2] == board[3]:
            board[2] = board[2] + board[3]
            board[3] = 0

    board = board[board != 0]  # снова убираю нули
    # добавляю нули в конец
    board = np.concatenate([board, np.zeros(4 - len(board),
                                            dtype=np.int)])
    return board


App()
