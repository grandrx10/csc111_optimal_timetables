"""
March 30, 2023
--------------
This file includes the rectangles that will output by Timetable
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from typing import Optional, Any
from time_h import Time
import pygame
from pygame.locals import *


class ScheduleRect:
    """
    A class that represents a single lecture session.

    Instance Attributes:
        - x: the x location of the center of the rectangle
        - y: the y location of the center of the rectangle
        - length: the length of the rectangle
        - width: the width of the rectangle
        - text: a list of text to display inside of this rectangle
    """
    x: int
    y: int
    length: int
    width: int
    text: list[str]

    def __init__(self, x: int, y: int, length: int, width: int, text: list[str]):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.text = text

    def display(self, surface) -> None:
        """
        Display this schedule rectangle on the screen.
        """
        black = (0, 0, 0)
        pygame.draw.rect(surface, black, pygame.Rect(self.x - self.length/2, self.y - self.width/2,
                                                     self.length, self.width), 3)

        # write text
        font = pygame.font.SysFont("Arial", 18)
        # TODO make it so that multiple lines of text can be displayed. currently only 1 line can be displayed.
        for i in range(len(self.text)):
            text = font.render(self.text[i], True, black)
            text_rect = text.get_rect(center=(self.x, self.y))
            surface.blit(text, text_rect)
