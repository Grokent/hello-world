"""Trash module.

Defines the Trash class used in the game.
"""

from __future__ import annotations

import pygame
from random import randint
from typing import Tuple

from . import config


class Trash:
    """Represents a piece of trash."""

    def __init__(self) -> None:
        self.radius = 5
        self.pos = pygame.Vector2(randint(20, config.WIDTH - 100), randint(20, config.HEIGHT - 20))
        self.collected = False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw trash as a white circle."""
        pygame.draw.circle(surface, config.WHITE, self.pos, self.radius, 1)

    def get_rect(self) -> pygame.Rect:
        """Return bounding rect for collision checks."""
        return pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)
