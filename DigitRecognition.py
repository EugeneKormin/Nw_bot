# импортирование сторонних библиотек
import numpy as np


class DigitRecognition(object):
    def __init__(self):
        '''
        Класс для распознавания цифр из массива np.ndarray
        '''
        # Загрузка шаблонов для распознавания по порядку от 0 до 9
        self.__samples: list[np.ndarray] = [
            np.load("samples/0.npy"),
            np.load("samples/1.npy"),
            np.load("samples/2.npy"),
            np.load("samples/3.npy"),
            np.load("samples/4.npy"),
            np.load("samples/5.npy"),
            np.load("samples/6.npy"),
            np.load("samples/7.npy"),
            np.load("samples/8.npy"),
            np.load("samples/9.npy")
        ]

    def array_to_digit(self, Array: np.ndarray) -> str:
        '''
        Метод для перевод массива RGB в число (не работает на более светлом фоне, чем сами цифры)
        :param Array: np.ndarray: массив с цифрой
        :return: str: цифра в виде строки (чтобы было проще собирать в массив)
        '''

        # создаёи м список для сравнения ошибок
        sample_errors: list = []

        # Создаём цикл, чтобы проверить насколько текущая цифра отличается от заранее подготовленного шаблона
        for INDEX, Sample in enumerate(self.__samples):
            # расчёт расхождения текущей цифры и заранее подготовленного шаблона
            diff_array: np.ndarray = abs(Sample - Array)
            # сбор списка с ошибками, чем меньше. тем меньше цифра отличается от шаблона, тем больше вероятность,
            # что эта цифра и является цифрой с шаблона
            sample_errors.append(diff_array.sum() / 1e6)

        # получение числа с минимальной ошибкой
        DIGIT: str = str(np.argmin(sample_errors))

        # возвращение в вызывающий метод предполагаемой цифры. На данный момент точность близка к 100%
        return DIGIT
