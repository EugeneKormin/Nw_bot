# импортирование сторонних библиотек
import numpy as np
import math
import cv2

# импортирование собственных модулей
from Screen import Screen
from Utils.Keys import Keys
from Variables import WINDOW_NAME


# установка глобальных значений для всего модуля, чтобы была возможность сохранять их при удалении стека метода
# расчёта угла движения
OLD_X: float = 0.0
OLD_Y: float = 0.0


def empty(_):
    ...


class GatheringBot(object):
    def __init__(self, GATHERED_UNIT_TYPE: str) -> None:
        '''
        # TODO реализовать получение текущей точки маршрута
        # TODO Реализовать метод поворота бота.
        Класс для описания логики бота-собирателя
        Объявление переменных класса
        :param GATHERED_UNIT_TYPE: str: тип сбора
        '''
        # определяем тип сбора
        self.__GATHERED_UNIT_TYPE: str = GATHERED_UNIT_TYPE

        # создаём экземпляры классов
        self.__screen: Screen = Screen(WINDOW_NAME=WINDOW_NAME)
        self.__keys: Keys = Keys()

        # запуск основного скрипта
        self.__execute()

    def __angle_calculation(self, COORDS: dict) -> float:
        '''
        Метод для расчёта угла по декартовым координатам ('X' и 'Y')
        :param X: float: текущая координата местонахождения бота по оси 'X'
        :param Y: float: текущая координата местонахождения бота по оси 'Y'
        :return: float: угол между направлением на север и текущим направлением движения бота
        '''

        # объявление переменных глобальными, чтобы они оставались в памяти после удаления стека метода из памяти
        global OLD_X, OLD_Y

        # получение значений текущих координат
        X, Y = COORDS['x_pos'], COORDS['y_pos']

        # нахождение смещения координат при движении бота
        dx: float = X - OLD_X
        dy: float = Y - OLD_Y

        # если нет смещения, то бот не движется
        if dy == 0 and dx == 0:
            # возвращение значения. которое невозможно получить с помощью текущих получений.
            # Нельзя получить значения меньше 0 или больше 180 по модулю.
            # 360 просто выглядит прикольно, на самом деле можно выбрать любое из диапазона: 0 > x > |180|
            return 360

        # если бот движется
        else:
            # если смещение бота по оси 'Y' будет равно нулю, то при вычислении 'arctg' появится ошибка деления на ноль
            if dy == 0:
                dy = 0.00001

            # расчёт arctg для расчёт угла смещения
            ARCTG: float = math.atan(dx / dy)

            # перевод из радиан в градусы
            DEGREES: float = ARCTG * 180 / math.pi

            # Установка стандартного коэффициента
            COEFF = 0

            # Изменяем коэффициента согласно условию ниже
            if dy < 0:
                COEFF = 180 if dx >= 0 else -180

            # Применение полученного коэффициента к полученному значению
            DEGREES = DEGREES + COEFF

            # обновление координат
            OLD_X, OLD_Y = X, Y

            # возвращение расчитанного угла
            return DEGREES

    def __rotate_bot(self, MOVEMENT_ANGLE: float, destination_angle: float = 0) -> None:
        '''
        # TODO Реализовать метод поворота бота.
        Метод для поворта бота для корректировки движения по спотам с ресурсами
        :param moving_angle: float: словарь с текузей позицией бота
        :param destination_angle: float: словарь с текузей позицией бота
        :return: None
        '''

        if MOVEMENT_ANGLE == 360:
            print('bot is not moving')
        else:
            print(f"angle of movement: {MOVEMENT_ANGLE}")

    def __execute(self) -> None:
        '''
        Метод для запуска
        :return: None
        '''

        # запуск бесконечного цикла
        while True:
            # обновление нормализованного массива RGB от 0 до 1
            array: np.array = self.__screen.img

            cv2.imshow("center", array)

            # получение координат текущего местонахождения бота
            COORDS: dict = self.__screen.get_coords(array=array)

            MOVEMENT_ANGLE: float = self.__angle_calculation(COORDS=COORDS)

            self.__rotate_bot(MOVEMENT_ANGLE=MOVEMENT_ANGLE)
