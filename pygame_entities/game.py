from types import FunctionType, MethodType
from typing import Any, Dict, List, Tuple, Union

from utils.math import Vector2

import pygame


class Game:
    _instance = None

    def __init__(self, screen_resolution: Tuple[int, int], frame_rate: float, void_color=(0, 0, 0)) -> None:
        if not Game._instance is None:
            raise Exception("Can not instantiate 2 Game objects.")

        pygame.init()

        self.void_color = void_color
        self.frame_rate = frame_rate
        self.screen_resolution = screen_resolution
        self.screen = pygame.display.set_mode(self.screen_resolution)
        self.clock = pygame.time.Clock()
        self.running = True

        self.sprites = pygame.sprite.LayeredUpdates()

        self.delta_time = 1 / self.frame_rate

        # Using dict, because with dict we can remove entities from game in O(1) time
        self.entity_counter = 0
        self.entities_for_delete = list()
        self.enabled_entities = dict()
        self.disabled_entities = dict()

        # For camera
        self.camera_follow_smooth_coefficient = 0.1
        self.camera_position = Vector2(0, 0)
        self.camera_follow_object = None

        # for event system
        self.subscribed_events: Dict[int, List[FunctionType]] = dict()

    def get_instance(screen_resolution=(0, 0), frame_rate=60) -> "Game":
        if Game._instance is None:
            Game._instance = Game(screen_resolution, frame_rate)

        return Game._instance

    def update_events(self):
        for event in pygame.event.get():
            for func in self.subscribed_events.get(event.type, []):
                func(event)

    def subsribe_for_event(self, function: Union[MethodType, FunctionType], event_type: int):
        subscribers = self.subscribed_events.get(event_type, [])
        subscribers.append(function)
        self.subscribed_events[event_type] = subscribers

    def set_framerate(self, new_framerate: int):
        self.frame_rate = new_framerate

    def set_screen(self, screen: pygame.Surface):
        self.screen = screen

    def run(self):
        while self.running:
            self.screen.fill(self.void_color)

            self.update_events()

            self.update_entities()

            self.sprites.update()

            self.delete_entities()

            self.camera_follow()

            self.sprites.draw(self.screen)
            pygame.display.flip()
            self.delta_time = self.clock.tick(self.frame_rate) / 1000

    def update_entities(self):
        for _, entity in self.enabled_entities.items():
            entity.update(self.delta_time)

    def camera_follow(self):
        if not self.camera_follow_object is None:
            self.camera_position = Vector2.lerp(
                self.camera_position,
                self.camera_follow_object.position
                - Vector2(
                    self.screen.get_width() /
                    2, self.screen.get_height() / 2
                ),
                self.camera_follow_smooth_coefficient,
            )

    def get_camera_center_position(self) -> Vector2:
        return self.camera_position + Vector2(
            self.screen.get_width() /
            2, self.screen.get_height() / 2
        )

    def add_sprite(self, sprite: pygame.sprite.Sprite):
        self.sprites.add(sprite)

    def add_entity(self, entity):
        self.enabled_entities[self.entity_counter] = entity
        entity.id = self.entity_counter
        self.entity_counter += 1

    def disable_entity(self, entity):
        if entity.id in self.enabled_entities.keys():
            self.disabled_entities[entity.id] = self.enabled_entities[entity.id]
            del self.enabled_entities[entity.id]

    def enable_entity(self, entity):
        if entity.id in self.disabled_entities.keys():
            self.enabled_entities[entity.id] = self.disabled_entities[entity.id]
            del self.disabled_entities[entity.id]

    def delete_entity(self, entity_id: int):
        if entity_id not in self.entities_for_delete:
            self.entities_for_delete.append(entity_id)

    def delete_entities(self):
        for entity_id in self.entities_for_delete:
            del self.enabled_entities[entity_id]

        self.entities_for_delete = list()
