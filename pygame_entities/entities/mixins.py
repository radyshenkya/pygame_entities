"""
Mixins for entities (Based on Entity class)
"""
from utils.drawable import BaseSprite
from utils.math import Vector2
from utils.collision_side import check_side, UP, DOWN, RIGHT, LEFT

from entities.entity import Entity

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

    def on_collide(self, entity, self_collider_rect: pygame.Rect, other_collider_rect: pygame.Rect):
        for method in self.on_collide_callbacks:
            method(entity, self_collider_rect, other_collider_rect)

    def on_trigger(self, entity, self_collider_rect: pygame.Rect, other_collider_rect: pygame.Rect):
        for method in self.on_trigger_callbacks:
            method(entity, self_collider_rect, other_collider_rect)

    def check_collisions(self, delta_time: float):
        if not self.is_check_collision:
            return

        for entity in self.game.enabled_entities.values():
            if not isinstance(entity, CollisionMixin) or entity.id == self.id:
                continue

            self_collider_rect = self.get_collider_rect()

            other_collider_rect = entity.get_collider_rect()

            if self_collider_rect.colliderect(other_collider_rect):
                if entity.is_trigger or self.is_trigger:
                    self.on_trigger(entity, self_collider_rect,
                                    other_collider_rect)
                    continue
                self.on_collide(entity, self_collider_rect,
                                other_collider_rect)

    def get_collider_rect(self) -> pygame.Rect:
        return pygame.Rect(
            (self.position - self.collider_size / 2).get_integer_tuple(),
            self.collider_size.get_integer_tuple(),
        )


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


class BlockingCollisionMixin(CollisionMixin):
    """
    Миксин, основанный на VelocityMixin CollisionMixin, при столкновении с каким-либо коллайдером возвращает сущность назад по velocity.
    """

    def collision_init(self, collider_size: Vector2, is_trigger=False):
        super().collision_init(collider_size, is_trigger, True)
        self.on_collide_callbacks.append(self.move_back_on_colliding)

    def move_back_on_colliding(self, entity: CollisionMixin, self_collider: pygame.Rect, other_collider: pygame.Rect):
        side = check_side(self_collider, other_collider)

        if side == UP:
            self_new_y = other_collider.top - (self_collider.height / 2)
            self.position = Vector2(self.position.x, self_new_y)
        elif side == DOWN:
            self_new_y = other_collider.bottom + (self_collider.height / 2)
            self.position = Vector2(self.position.x, self_new_y)
        elif side == RIGHT:
            self_new_x = other_collider.right + (self_collider.width / 2)
            self.position = Vector2(self_new_x, self.position.y)
        else:
            self_new_x = other_collider.left - (self_collider.width / 2)
            self.position = Vector2(self_new_x, self.position.y)


class MouseEventMixin(CollisionMixin):
    """
    Миксин для обработки нажатий на коллайдер сущности.
    Основан на CollisionMixin. Перед инициализацией этого миксина нужно вызвать self.collision_init(...)

    Добавляет коллбеки:
    on_mouse_down(mouse_button) - при нажатии кнопки над коллайдером
    on_mouse_up(mouse_button) - при отпускании кнопки над коллайдером
    on_mouse_motion - при движении мыши над коллайдером
    """

    def mouse_events_init(self):
        self.on_mouse_down = list()
        self.on_mouse_up = list()
        self.on_mouse_motion = list()
        self.on_update.append(self.mouse_events)

    def mouse_events(self, _):
        # Checking, is mouse pointer is over object
        mouse_world_position = self.game.from_screen_to_world_point(
            Vector2.from_tuple(pygame.mouse.get_pos()))

        if not self.get_collider_rect().collidepoint(mouse_world_position.get_tuple()):
            return

        for event in self.game.get_events():
            if event.type == pygame.MOUSEBUTTONDOWN:
                [f(event.button) for f in self.on_mouse_down]
            elif event.type == pygame.MOUSEBUTTONUP:
                [f(event.button) for f in self.on_mouse_up]
            elif event.type == pygame.MOUSEMOTION:
                [f() for f in self.on_mouse_motion]
