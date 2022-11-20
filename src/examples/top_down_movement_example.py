from game import Game
from utils.drawable import DrawableSprite, CameraOffsetDrawableSprite
from utils.vector import Vector2
from utils.math import clamp
from entities.entity import Entity
from entities.mixins import SpriteMixin, CollisionMixin, VelocityMovableMixin

import pygame


class Player(Entity, SpriteMixin, CollisionMixin, VelocityMovableMixin):
    SPEED = 100
    MAX_SPEED = 5
    VELOCITY_REGRESS = 0.1

    def __init__(
        self,
        position: Vector2,
        drawable_sprite: DrawableSprite,
        collider_size: Vector2,
        is_trigger=False,
    ) -> None:
        super().__init__(position)

        self.on_update.append(self.player_move)
        self.velocity_init(False, Player.VELOCITY_REGRESS)
        self.collision_init(collider_size, is_trigger, True)
        self.sprite_init(drawable_sprite)

        self.on_collide_callbacks.append(lambda entity: entity.destroy())

    def player_move(self, delta_time: float):
        keys = pygame.key.get_pressed()

        direction = Vector2(0, 0)

        if keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_w]:
            direction.y -= 1

        self.velocity += direction.normalized() * Player.SPEED * delta_time
        self.velocity = Vector2(
            clamp(self.velocity.x, -Player.MAX_SPEED, Player.MAX_SPEED),
            clamp(self.velocity.y, -Player.MAX_SPEED, Player.MAX_SPEED),
        )

        self.sprite.set_center_position(self.position.get_integer_tuple())


def main():
    game = Game.get_instance((800, 800), 60)

    surface = pygame.Surface((32, 32))
    surface.fill((0, 255, 0))

    Player(Vector2(0, 0), CameraOffsetDrawableSprite(surface), Vector2(32, 32))

    game.run()


if __name__ == "__main__":
    main()
