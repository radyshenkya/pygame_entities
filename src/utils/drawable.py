"""
Classes for drawing sprites/sprites animations/etc
"""
from typing import Tuple

from game import Game
from utils.vector import Vector2

import pygame
import pygame.math


class DrawableSprite(pygame.sprite.Sprite):
    def __init__(self, image, start_position=(0, 0)) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = start_position
        self.game = Game.get_instance()

        # Registering sprite
        self.game.add_sprite(self)

    def set_center_position(self, position: Tuple[int, int]):
        self.rect.center = position


class CameraOffsetDrawableSprite(DrawableSprite):
    def __init__(self, image, start_position=(0, 0)) -> None:
        super().__init__(image, start_position)

        self.base_position = start_position

    def update(self) -> None:
        super().update()

        self.rect.center = (
            Vector2(self.base_position[0], self.base_position[1])
            - self.game.camera_position
        ).get_integer_tuple()

    def set_center_position(self, position: Tuple[int, int]):
        self.base_position = position
