from PIL import Image
import os


def create_gif(num_of_pictures, num_task):
    """!@brief
        Функция для создания gif на основе сохраненных в ходе работы программы изображений.

        @arg pictures [list] — список для хранения изображений.
        @arg im [Image] — объект класса Image.

        @param int $num_of_pictures — количество изображений.
        @param int $num_task — номер решаемой задачи.
        """
    pictures = []
    im = Image.open('0.png')
    for picture in range(num_of_pictures):
        pictures.append(Image.open(f'{picture}.png'))

    im.save(f'gifs/out_task_{num_task}.gif', save_all=True, append_images=pictures, duration=2000, loop=0)


def delete_pictures(num_of_pictures):
    """!@brief
        Функция для удаления сохраненных в ходе работы программы изображений.

        @param int $num_of_pictures — количество изображений.
        """
    for picture in range(num_of_pictures):
        os.remove(f'{picture}.png')


def check_num(num):
    """!@brief
        Функция для проверки корректности введенного пользователем числа вершин.

        @param int $num — число введенных пользователем вершин.

        @retval True — введено корректное число вершин.
        @retval False — введено некорректное число вершин.
        """
    if not num.isnumeric():
        return False

    elif int(num) < 2:
        return False

    else:
        return True
