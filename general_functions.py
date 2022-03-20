from PIL import Image
import os


def create_gif(num_of_pictures, num_task):
    pictures = []
    im = Image.open('0.png')
    for picture in range(num_of_pictures):
        pictures.append(Image.open(f'{picture}.png'))

    im.save(f'gifs/out_task_{num_task}.gif', save_all=True, append_images=pictures, duration=2000, loop=0)


def delete_pictures(num_of_pictures):
    for picture in range(num_of_pictures):
        os.remove(f'{picture}.png')


def check_num(num):
    if not num.isnumeric():
        return False

    elif int(num) < 2:
        return False

    else:
        return True
