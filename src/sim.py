"""Sim module.

Contains the Sim class which represents a trash-collecting character.
"""

from __future__ import annotations

import pygame

from . import config
from .trash import Trash


class Sim:
    """A simple AI character that collects trash."""

    def __init__(self) -> None:
        self.pos = pygame.Vector2(50, config.HEIGHT // 2)
        self.speed = config.SIM_SPEED
        self.carrying: Trash | None = None
        self.currency = config.STARTING_CURRENCY

    def update(self, trash_list: list[Trash]) -> None:
        """Update the sim each frame."""
        target = self.carrying or self._nearest_trash(trash_list)
        if target:
            target_pos = self._target_position(target)
            self._move_toward(target_pos)
            if self.carrying:
                # Check if reached hole
                hole_rect = pygame.Rect(config.HOLE_X - config.HOLE_RADIUS,
                                        config.HOLE_Y - config.HOLE_RADIUS,
                                        config.HOLE_RADIUS * 2,
                                        config.HOLE_RADIUS * 2)
                if hole_rect.collidepoint(self.pos):
                    self.currency += 1
                    trash_list.remove(self.carrying)
                    self.carrying = None
            else:
                if self.get_rect().colliderect(target.get_rect()):
                    self.carrying = target
                    target.collected = True

    def _target_position(self, target: Trash) -> pygame.Vector2:
        if self.carrying:
            return pygame.Vector2(config.HOLE_X, config.HOLE_Y)
        return target.pos

    def _move_toward(self, target: pygame.Vector2) -> None:
        direction = (target - self.pos).normalize() if target != self.pos else pygame.Vector2()
        speed = config.CARRY_SPEED if self.carrying else self.speed
        self.pos += direction * speed

    def _nearest_trash(self, trash_list: list[Trash]) -> Trash | None:
        if not trash_list:
            return None
        return min(trash_list, key=lambda t: (t.pos - self.pos).length())

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the sim as a simple triangle."""
        points = [
            (self.pos.x, self.pos.y - 10),
            (self.pos.x - 10, self.pos.y + 10),
            (self.pos.x + 10, self.pos.y + 10),
        ]
        pygame.draw.polygon(surface, config.WHITE, points, 1)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos.x - 10, self.pos.y - 10, 20, 20)
