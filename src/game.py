"""Game module.

This module contains the Game class, which manages the game loop and state.
"""

from __future__ import annotations

import pygame

from . import config
from .sim import Sim
from .trash import Trash


def _spawn_trash(event_id: int) -> int:
    """Helper to create a new custom event for trash spawning."""
    spawn_event = pygame.USEREVENT + event_id
    pygame.time.set_timer(spawn_event, config.TRASH_SPAWN_INTERVAL)
    return spawn_event


class Game:
    """Main game class."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Trash Collector")
        self.clock = pygame.time.Clock()

        self.sim = Sim()
        self.trash_list: list[Trash] = []
        self.spawn_event = _spawn_trash(1)
        self.running = True

    def run(self) -> None:
        """Run the main game loop."""
        while self.running:
            self._handle_events()
            self.sim.update(self.trash_list)
            self._draw()
            self.clock.tick(60)
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.spawn_event:
                self.trash_list.append(Trash())

    def _draw(self) -> None:
        self.screen.fill(config.BLACK)
        # Draw hole
        pygame.draw.circle(self.screen, config.WHITE, (config.HOLE_X, config.HOLE_Y), config.HOLE_RADIUS, 1)
        for trash in self.trash_list:
            trash.draw(self.screen)
        self.sim.draw(self.screen)
        # Draw currency
        self._draw_currency()
        pygame.display.flip()

    def _draw_currency(self) -> None:
        font = pygame.font.SysFont("monospace", 20)
        text = font.render(f"$ {self.sim.currency}", True, config.WHITE)
        self.screen.blit(text, (10, 10))
