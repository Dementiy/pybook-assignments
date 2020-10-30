import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)

    def draw_lines(self) -> None:
        # Copy from previous assignment
        pass

    def draw_grid(self) -> None:
        # Copy from previous assignment
        pass

    def run(self) -> None:
        # Copy from previous assignment
        pass
