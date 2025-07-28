"""Entrypoint for the Trash Collector game."""

from .game import Game


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
