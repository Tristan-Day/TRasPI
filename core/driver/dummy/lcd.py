import os
from core.sys.constants import Constant

_clear_sys_ = "cls" if Constant.platform == "NT" else "clear"
__image = [[2 for x in range(Constant.width)] for y in range(Constant.height)]

def setup():
    for y in __image:
        for x in range(Constant.width):
            y[x] = 2

def clear():
    for y in __image:
        for x in range(Constant.width):
            y[x] = 0

def show():
    os.system(_clear_sys_)
    for y in __image:
        print("".join("#" if i else " " for i in y))

def set_pixel(x: int, y: int, value: int):
    __image[y][x] = value