"""
Mixins for entities (Based on Entity class)
"""
from pygame_entities.utils.drawable import BaseSprite
from pygame_entities.utils.vector import Vector2

from pygame_entities.entities.entity import Entity

import pygame


class SpriteMixin(Entity):
    """
    Миксин для отрисовки спрайтов.
    """

    def sprite_init(self, sprite: BaseSprite, sprite_position_offset=Vector2()) -> None:
        self.sprite_offset = sprite_position_offset
        self.sprite = sprite
        self.sprite.set_center_position(
            (self.position + self.sprite_offset).get_integer_tuple())
        self.on_update.append(self.sprite_update_position)
        self.on_destroy.append(self.kill_sprite)

    def sprite_update_position(self, delta_time: float):
        self.sprite.set_center_position(
            (self.position + self.sprite_offset).get_integer_tuple())

    def kill_sprite(self):
        self.sprite.kill()


class CollisionMixin(Entity):
    """
    Миксин для считывания коллизий.
    Функции коллбеков добавляются в список self.on_collide_callbacks / self.on_trigger_callbacks. Функции вызываются с аргументот entity: Entity
    """

    def collision_init(
        self, collider_size: Vector2, is_trigger=False, is_check_collision=False
    ):
        self.collider_size = collider_size
        self.is_trigger = is_trigger
        self.on_update.append(self.check_collisions)
        self.is_check_collision = is_check_collision
        self.on_collide_callbacks = list()
        self.on_trigger_callbacks = list()

    def on_collide(self, entity):
        for method in self.on_collide_callbacks:
            method(entity)

    def on_trigger(self, entity):
        for method in self.on_trigger_callbacks:
            method(entity)

    def check_collisions(self, delta_time: float):
        if not self.is_check_collision:
            return

        for entity in self.game.entities.values():
            if not isinstance(entity, CollisionMixin) or entity.id == self.id:
                continue

            self_collider_rect = pygame.Rect(
                (self.position - self.collider_size / 2).get_integer_tuple(),
                self.collider_size.get_integer_tuple(),
            )

            other_collider_rect = pygame.Rect(
                (entity.position - entity.collider_size / 2).get_integer_tuple(),
                entity.collider_size.get_integer_tuple(),
            )

            if self_collider_rect.colliderect(other_collider_rect):
                if entity.is_trigger or self.is_trigger:
                    self.on_trigger(entity)
                    continue
                self.on_collide(entity)


class VelocityMixin(Entity):
    """
    Миксин для плавного движения с помощью вектора ускорения. (self.velocity)
    Для изменения скорости нужно изменять вектор self.velocity
    """

    def velocity_init(self, is_kinematic=True, velocity_regress_strength=0.0):
        self.is_kinematic = is_kinematic

        self.velocity_regress_strength = velocity_regress_strength
        self.velocity = Vector2(0, 0)

        self.on_update.append(self.update_velocity_and_pos)

    def update_velocity_and_pos(self, delta_time: float):
        self.position += self.velocity

        if not self.is_kinematic:
            self.velocity = Vector2.lerp(
                self.velocity, Vector2(0, 0), self.velocity_regress_strength
            )
