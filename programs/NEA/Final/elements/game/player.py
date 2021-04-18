import random

import core
from app import App
from core import Vector
from game.library import lib
from generation.common import align
from PIL import Image as PIL


class Player:

    def __init__(self, height, speed: float):
        self.y = height
        self.speed = speed

        if App.var.playerskin is None:
            type_id = lib.fetch_typeid("texture", "player-skin")
            lib.databases["textures"].c.execute(
                "SELECT image_id FROM texture WHERE type_id = ?", [type_id])
            image_id = random.choice(lib.databases["textures"].c.fetchall())[0]
            App.var.playerskin = image_id
        self.sprite = lib.fetch_image(App.var.playerskin)

        self.x_offset = align(self.sprite, "X", "C")
        self.y_offset = align(self.sprite, "Y", "B")
        self.x = (self.sprite.width // 2)

    def render(self, frame):
        frame.alpha_composite(self.sprite, dest=(
            self.x + self.x_offset,
            self.y + self.y_offset))
        return frame

    def increment(self):
        if self.x != 128 - (self.sprite.width // 2): # Keep Sprite Onscreen
            self.x += self.speed
            print(self.x)

    def decrement(self):
        if self.x != 0 + (self.sprite.width // 2):
            self.x -= self.speed

    def set_position(self, position):
        self.x = position + self.x_offset
