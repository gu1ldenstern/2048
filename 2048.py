import pyxel
import numpy as np
from numpy import zeros, ones
from random import random, randint
from math import log

#############
# CONSTANTS #
#############
TABLE = zeros((4, 4), dtype=np.int)
MATRIX_OF_INDEXES = [[11, 25], [27, 25], [42, 25], [57, 25], [11, 40], [27, 40], [42, 40], [57, 40],
                     [11, 55], [27, 55], [42, 55], [57, 55], [11, 70], [27, 70], [42, 70], [57, 70]]
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 90
MUSIC = 1
SOUND_EFFECTS = 0
SCREEN_COLOR = 0
FIELD_COLOR = 13
DESIGN = -1
PALETTE = [0xe8e1ae, 0xF08080, 0xFFA07A, 0xFF8C00, 0xFFD700, 0xADFF2F, 0x00FF7F, 0x66CDAA,
           0x008B8B, 0xFFA300, 0xFFEC27, 0x00E436, 0x29ADFF, 0x83769C, 0xF08080, 0x000000]


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="2048", palette=PALETTE)
        pyxel.load("[pyxel_resource_file].pyxres")
        self.field = TABLE
        self.design = 1
        self.options = 1
        add_random(self.field)
        pyxel.playm(MUSIC, loop=True)
        self.reset()

        pyxel.run(self.update, self.draw)
        pyxel.sound(19).set(
            note="c3e3g3c4c4", tone="s", volume="7", effect=("n" * 4 + "f"), speed=7
        )
        pyxel.sound(29).set(
            note="f3 b2 f2 b1  f1 f1 f1 f1",
            tone="p",
            volume=("4" * 4 + "4321"),
            effect=("n" * 7 + "f"),
            speed=9,
        )

    def reset(self):
        self.design = -1
        self.options = 1

    ###########
    # updates #
    ###########
    def update(self):

        if pyxel.btn(pyxel.KEY_O):  # обработка выхода из программы
            self.options = -1

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btn(pyxel.KEY_1):
            self.design *= (-1)
        if pyxel.btn(pyxel.KEY_G):
            self.options = 1

        ####################
        # KEYS & MOVEMENTS #
        ####################
        if pyxel.btnp(pyxel.KEY_UP):  # IF USER PRESSES "UP"
            check = self.field.copy()
            move_up(self.field)
            if not np.equal(self.field, check).all():  # не ставлю новое число, если таблица осталась той же
                self.field = add_random(self.field)
            else:
                pyxel.play(3, 19)
        if pyxel.btnp(pyxel.KEY_1):
            self.design = self.design * (-1)

        if pyxel.btnp(pyxel.KEY_DOWN):  # IF USER PRESSES "DOWN"
            check = self.field.copy()
            move_down(self.field)
            if not np.equal(self.field, check).all():
                self.field = add_random(self.field)

        if pyxel.btnp(pyxel.KEY_RIGHT):  # IF USER PRESSES "RIGHT"
            check = self.field.copy()
            move_right(self.field)
            if not np.equal(self.field, check).all():
                self.field = add_random(self.field)

        if pyxel.btnp(pyxel.KEY_LEFT):  # IF USER PRESSES "LEFT"
            check = self.field.copy()
            move_left(self.field)
            if not np.equal(self.field, check).all():
                self.field = add_random(self.field)

    ###########
    # DRAWING #
    ###########
    def draw(self):
        # THAT'S WHERE I DRAW THE FIELD
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

            pyxel.text(33, 10, "2048!", pyxel.frame_count % 16)

            pyxel.line(25, 20, 25, 79, SCREEN_COLOR)
            pyxel.line(40, 20, 40, 79, SCREEN_COLOR)
            pyxel.line(55, 20, 55, 79, SCREEN_COLOR)

            pyxel.line(10, 35, 69, 35, SCREEN_COLOR)
            pyxel.line(10, 50, 69, 50, SCREEN_COLOR)
            pyxel.line(10, 65, 69, 65, SCREEN_COLOR)

            pyxel.text(0, 82, "press[o] for options", pyxel.frame_count % 15)

            # отрисовка новой таблицы с новыми значениями

            table1 = self.field
            table1 = table1.reshape(16, 1)
            count = 0
            for i in MATRIX_OF_INDEXES:
                if str(table1[count][0]) != '0':
                    pyxel.text(int(f'{i[0]}'), int(f'{i[1]}'), str(table1[count][0]), log(float(table1[count][0]), 2))
                count += 1
        else:
            pyxel.cls(15)
            pyxel.text(7, 7, "options:", pyxel.frame_count % 16)
            pyxel.text(7, 20, "press [Q] to exit", pyxel.frame_count % 16)
            pyxel.text(0, 33, "press[1](thoroughly)", pyxel.frame_count % 16)
            pyxel.text(7, 41, "to change design", pyxel.frame_count % 16)
            pyxel.text(7, 54, "press [2] to see", pyxel.frame_count % 16)
            pyxel.text(7, 62, "your progress", pyxel.frame_count % 16)
            pyxel.text(7, 77, "[G]-back to game", pyxel.frame_count % 16)


####################################
# NUMPY CALCULATIONS FOR MOVEMENTS #
####################################

def add_random(board):  # добавление числа (2 с вероятностью 85% или 4) на рандомную пустую клетку
    i, j = (board == 0).nonzero()
    if i.size != 0:
        rnd = randint(0, i.size - 1)
        board[i[rnd], j[rnd]] = 2 ** ((random() > 0.85) + 1)
        return board
    else:
        self.death_event()


def move_left(field):
    for i in range(len(field)):
        field[i] = movement(field[i])
    return field


# только функция move_left умеет нормально работать с movement, остальные должны сначала преобразоваться в
# сдвиг влево, потом сдвинуться влево, а потом трансформироваться в свой сдвиг (вправо, вниз etc)


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
    print(field)
    return field.transpose


def movement(board):  # сдвигает одну строчку влево со складыванием

    board = board[board != 0]  # убираю нули
    # я устала писать красиво так что буду писать просто - я рассматриваю каждый вариант длины и для него пишу
    # разные ифы, оно длинно для меня, но сравнительно просто и быстро для компа

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
    board = np.concatenate([board, np.zeros(4 - len(board), dtype=np.int)])  # добавляю нули в конец
    return board


App()
