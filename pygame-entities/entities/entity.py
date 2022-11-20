from utils.drawable import DrawableSprite
from utils.vector import Vector2
from game import Game

import pygame


class Entity:
    def __init__(self, position: Vector2) -> None:
        self.position = position

        self.on_update = list()
        self.on_destroy = list()

        # Registering entity
        self.id = 0
        self.game = Game.get_instance()
        self.game.add_entity(self)

    def update(self, delta_time: float):
        for method in self.on_update:
            method(delta_time)

    def destroy(self):
        for method in self.on_destroy:
            method()
        Game.get_instance().delete_entity(self.id)
