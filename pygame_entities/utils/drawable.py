"""
Classes for drawing sprites/sprite animations/etc
"""
from typing import List, Tuple

from game import Game
from utils.math import Vector2

import pygame
import pygame.math


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, layer=0, start_position=(0, 0)) -> None:
        pygame.sprite.Sprite.__init__(self)
        self._layer = layer

        self.original_image = image

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = start_position
        self.game = Game.get_instance()
        self.visibility = True

        # Transform vars
        self.rotation = 0.0

        # Registering sprite
        self.game.add_sprite(self)

    def set_center_position(self, position: Tuple[int, int]):
        self.rect.center = position

    def set_rotation(self, new_rotation: float):
        self.rotation = new_rotation
        self.image = pygame.transform.rotate(self.original_image, new_rotation)

    def get_rotation(self) -> float:
        return self.rotation

    def reset_image_to_original(self):
        self.image = self.original_image

    def update_image_transformation(self):
        self.reset_image_to_original()

        self.image = pygame.transform.rotate(self.image, self.rotation)

    def get_layer(self):
        return self._layer

    def set_layer(self, value):
        self.game.sprites.change_layer(self, value)

    def set_visible(self, is_visible: bool):
        if is_visible:
            self.show()
        else:
            self.hide()

    def hide(self):
        if not self.visibility:
            return
        self.visibility = False
        self.kill()

    def show(self):
        if self.visibility:
            return
        self.visibility = True
        self.game.add_sprite(self)


class SpriteWithCameraOffset(BaseSprite):
    def __init__(self, image, layer=0, start_position=(0, 0)) -> None:
        super().__init__(image, layer, start_position)

        self.base_position = start_position

    def update(self) -> None:
        super().update()

        self.rect.center = (
            Vector2(self.base_position[0], self.base_position[1])
            - self.game.camera_position
        ).get_integer_tuple()

    def set_center_position(self, position: Tuple[int, int]):
        self.base_position = position


class FontSprite(BaseSprite):
    def __init__(self, text: str, color: Tuple[int, int, int], font: pygame.font.Font, layer=0, start_position=(0, 0)) -> None:
        super().__init__(pygame.Surface((0, 0)), layer, start_position)
        self.font = font

        self.set_text(text, color)

    def set_text(self, new_text: str, new_color: Tuple[int, int, int]):
        # Getting size of surface
        text_size = self.font.size(new_text)

        # Creating new surface
        new_text_surface = pygame.Surface(text_size, pygame.SRCALPHA)
        new_text_surface.blit(self.font.render(
            new_text, 0, new_color), (0, 0))

        self.image = new_text_surface

    def set_font(self, new_font: pygame.font.Font):
        self.font = new_font


class FontSpriteWithCameraOffset(FontSprite, SpriteWithCameraOffset):
    def __init__(self, text: str, color: Tuple[int, int, int], font: pygame.font.Font, layer=0, start_position=(0, 0)) -> None:
        super().__init__(text, color, font, layer, start_position)


class AnimatedSprite(BaseSprite):
    def __init__(self, frames: List[pygame.Surface], frame_change_delay: float, layer=0, start_position=(0, 0)) -> None:
        super().__init__(frames[0], layer, start_position)

        self.frames = frames
        self.current_frame_index = 0
        self.frames_count = len(frames)
        self.frame_delay = frame_change_delay
        self.timer = 0.0

    def update(self) -> None:
        super().update()

        self.timer += self.game.delta_time

        if self.timer >= self.frame_delay:
            self.timer = 0.0
            self.current_frame_index = (
                self.current_frame_index + 1) % self.frames_count

            self.original_image = self.frames[self.current_frame_index]
            self.update_image_transformation()

    def set_frame_change_delay(self, new_delay: float) -> None:
        self.frame_delay = new_delay


class AnimatedSpriteWithCameraOffset(AnimatedSprite, SpriteWithCameraOffset):
    def __init__(self, frames: List[pygame.Surface], frame_change_delay: float, layer=0, start_position=(0, 0)) -> None:
        super().__init__(frames, frame_change_delay, layer, start_position)

        self.base_position = start_position

    def update(self) -> None:
        super().update()
