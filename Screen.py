# импортирование сторонних библиотек
import mss                                      # библиотека для получения фрейсов для дальнейшего анализа
from win32gui import GetWindowRect              # библиотека для получения положения изображения для анализа
from ctypes import windll                       # библиотека для нахождения окна по его имена
import numpy as np
import cv2
import hashlib
import datetime

# импортирование собственных модулей
from Variables import DIGIT_WIDTH, DISTANCE_BETWEEN_DIGITS_COORDS, SHIFT, SCALING_FACTOR, DIGIT_HEIGHT, UPPER_LINE
from DigitRecognition import DigitRecognition


# объявление класса Screen
class Screen(object):
    '''
    Все методы, связанные с обработкой изображений
    '''
    def __init__(self, WINDOW_NAME: str) -> None:
        '''
        Объявление переменных класса
        :param WINDOW_NAME: str: имя окна с игрой
        '''
        # имя окна с игрой
        self.__WINDOW_NAME = WINDOW_NAME
        # создание экземпляра класса для распознавания координат
        self.__digit_recognition = DigitRecognition()

    @staticmethod
    def __save_screen(Array: np.ndarray):
        now: str = str(datetime.datetime.now())
        HASH_NAME: str = hashlib.md5(now.encode()).hexdigest()
        np.save(f"./images/{HASH_NAME}", Array)

    @staticmethod
    def __grab(X: int, Y: int, W: int, H: int) -> np.ndarray:
        '''
        Получение фрейма для дальнейшего анализа
        :param X: int: координата верхней границы окна WINDOW_NAME
        :param Y: int: координата левой границы окна WINDOW_NAME
        :param W: int: ширина окна WINDOW_NAME
        :param H: int: высота окна WINDOW_NAME
        :return: ndarray: массив ndarray, отображающей фрейм для анализа
        '''
        # получение изображения в формате RGBA. Не особо понимаю, чего внутри библиотеки mss происходит ;-(
        with mss.mss() as sct:
            monitor: dict = {"top": Y, "left": X, "width": W, "height": H}
            # получаем массив np.ndarray в формате RGBA
            img_array: np.array = np.array(sct.grab(monitor))
            # конвертируем BGRA в BGR
            rgb_image_array: np.ndarray = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
            # возвращение значений
            return rgb_image_array

    def __getWindowRect(self, WINDOW_NAME: str) -> np.ndarray:
        '''
        Метод для получения местонахождения окна с именем WINDOW_NAME
        :param WINDOW_NAME: str: название окна для получения его местонахождения
        :return: None
        '''
        # получение номера окна с игрой
        HWND: int = windll.user32.FindWindowW(0, WINDOW_NAME)

        # получение координат с игрой
        rect: tuple[int, int, int, int] = GetWindowRect(HWND)

        # парсинг данных
        RECT_X: int = rect[0]
        RECT_Y: int = rect[1]
        RECT_W: int = rect[2]
        RECT_H: int = rect[3]
        array: np.ndarray = self.__grab(X=RECT_X, Y=RECT_Y, W=RECT_W, H=RECT_H)
        return array

    def get_coords(self, array: np.ndarray) -> dict:
        '''
        Получение координат с экрана для определения текущего положения бота и корректировки его движения
        :param array: np.ndarray: нормализованный от 0 до 1 np.ndarray массив в формате RGB
        :return: dict: словарь с ккординатами 'X' и 'Y'
        '''
        # создание/обновление переменных для записи соответствующих координат
        X_COORD: list = []
        Y_COORD: list = []

        # Обрезаем, чтобы остались только координаты 'X' и 'Y'
        coordinates_cropped: dict = self.__crop_coords(array_to_crop=array)

        for INDEX in range(14):
            # определение изображения кооррдинаты из словаря
            COORD: str = ['x' if INDEX // 7 == 0 else 'y'][0]
            INDEX: int = (INDEX - ((INDEX // 7) * 7)) + 1

            # увеличение изображения в n раз
            coord_image_resized: np.array = self.__enlarge_image(
                array=coordinates_cropped[COORD][(INDEX - ((INDEX // 7) * 7)) + 1]
            )

            # создание фильтров для более точного определения границ цифр координат бота
            lower_orange: np.ndarray = np.array([0, 150, 150])
            upper_orange: np.ndarray = np.array([255, 255, 255])

            # создание изображения, используя фильтры
            mask = cv2.inRange(coord_image_resized, lower_orange, upper_orange)
            cv2.waitKey(1)
            
            # распознавание цифр из изображений с координатами
            TEXT_FROM_IMAGE: str = self.__digit_recognition.array_to_digit(Array=mask)

            # распределение и создание координаты X и координаты Y
            if COORD == 'x':
                X_COORD.append(TEXT_FROM_IMAGE)
            else:
                Y_COORD.append(TEXT_FROM_IMAGE)

        # Пересбор цифр. По какой-то причине первая координата распечатывается последним
        X_COORD_NUM: float = float(f"{X_COORD[6]}{X_COORD[0]}{X_COORD[1]}{X_COORD[2]}"
                                   f".{X_COORD[3]}{X_COORD[4]}{X_COORD[5]}")
        Y_COORD_NUM: float = float(f"{Y_COORD[6]}{Y_COORD[0]}{Y_COORD[1]}{Y_COORD[2]}"
                                   f".{Y_COORD[3]}{Y_COORD[4]}{Y_COORD[5]}")

        # Создание словаря с координатами
        COORDS: dict = {
            'x_pos': X_COORD_NUM,
            'y_pos': Y_COORD_NUM
        }

        # Возвращение координат
        return COORDS

    @staticmethod
    def __enlarge_image(array: np.ndarray) -> np.ndarray:
        '''
        Увеличивание изобрадений в SCALING_FACTOR раз
        :param array: np.ndarray: массив, отображающий цифры текущейго положения игрока
        :param SCALING_FACTOR: int: коэффициент скалирования, отображающий во сколько раз будет увеличено изображение
        :return: np.ndarray: массив, отображающий увеличенное изображение
        '''
        # Размеры до изменений
        ORIGINAL_HEIGHT: int = array.shape[0]
        ORIGINAL_WIDTH: int = array.shape[1]

        # скалирование изображение средствами библиотеки opencv
        resized_image: np.ndarray = cv2.resize(
            array,
            (ORIGINAL_WIDTH*SCALING_FACTOR, ORIGINAL_HEIGHT*SCALING_FACTOR),
            interpolation=cv2.INTER_CUBIC)

        # возвращение скалированного изображения
        return resized_image

    def __crop_coords(self, array_to_crop: np.ndarray) -> dict:
        '''
        Получение словаря из массивов ndarray, каждый из значений которого - это массив, который является цифрой.
        :param array_to_crop: массив ndarray для анализа
        :return: dict: словарь с 14 цифрами. 7 для кооринаты 'X', ****.***, аналогично для 'Y'
        '''
        # создание координаты 'X' для правой границы цифры получения цифр текущей позиции
        X_RIGHT_MAIN: int = 776

        # создание координаты 'X' для левой границы цифры получения цифр текущей позиции
        X_LEFT_MAIN: int = X_RIGHT_MAIN + DIGIT_WIDTH

        # создание списка для обработки обоих координат за один вызов метода
        coord_list: list = ['x', 'y']

        # создание словаря для сбора массивов ndarray
        coordinates: dict = {}

        # цикл для обработки всех координат
        for COORDINATE in coord_list:

            # если мы начинаем получать координату 'Y', то необходимо сдвинуться на SHIFT пикселей,
            # получение обеих координат аналогично
            if COORDINATE == 'y':
                X_RIGHT_MAIN += SHIFT
                X_LEFT_MAIN: int = X_RIGHT_MAIN + DIGIT_WIDTH

            # создание словаря для каждой их координат aka coordinates['x']/coordinates['y']
            coordinates.update({COORDINATE: {}})

            # создание цикла для получения всех цифр, составляющих одну координату
            for INDEX in range(7):
                if INDEX == 3:
                    COEFF: int = 9
                else:
                    COEFF: int = 0

                # обновление словаря. Первая координата - вертикаль, вторая - горизонталь
                coordinates[COORDINATE].update({INDEX+1: array_to_crop[
                                                         UPPER_LINE:UPPER_LINE+DIGIT_HEIGHT,
                                                         X_RIGHT_MAIN:X_LEFT_MAIN
                                                         ]})

                # сдвиг для получения дополнительных цифр
                X_RIGHT_MAIN += DISTANCE_BETWEEN_DIGITS_COORDS + COEFF
                X_LEFT_MAIN: int = X_RIGHT_MAIN + DIGIT_WIDTH

        # возвращение собранного словаря
        return coordinates

    @property
    def img(self) -> np.ndarray:
        '''
        :return: np.ndarray: возвращение необработанного фрейма для дальнейшей обработки и анализа
        '''
        # получение нормализованного от 0 до 1 np.ndarray массив в формате RGB
        array: np.ndarray = self.__getWindowRect(WINDOW_NAME=self.__WINDOW_NAME)

        # возвращение полученного массива
        return array
