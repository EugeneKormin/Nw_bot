from PIL.Image import open as open_image
from uuid import uuid4
from os import listdir


class Image_(object):
    def __init__(self):
        self.__image = None
        self.__unique_filename = ''

    def set_image_name(self, file_name: str) -> None:
        self.__image = open_image(rf'images\{file_name}')

    def __set_unique_filename(self) -> None:
        self.__unique_filename: str = fr'images\full_spot_imgs\{str(uuid4())}.jpg'

    def cut_into_samples(self, *args) -> None:
        for num, _ in enumerate(args):
            w: int = args[num][0]
            h: int = args[num][1]
            for x in range(0, 1024-(int(1024/4)), int(1024/12)):
                for y in range(0, 768-(int(768/4)), int(768/12)):
                    cropped_image = self.__image.crop((x, y, x+w, y+h))
                    self.__set_unique_filename()
                    cropped_image.save(self.__unique_filename)


image = Image_()

for img_name in listdir(r'D:\MyProjects\NW_bot\images'):
    if '.' in img_name and 'full' in img_name:
        image.set_image_name(file_name=img_name)
        image.cut_into_samples([int(1024/4), int(768/4)])
