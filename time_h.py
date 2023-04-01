"""
March 08, 2023
--------------
This file contains the time class
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations


class Time:
    """
    This class holds the time.
    """
    hours: int
    minutes: int

    def __init__(self, hours: int, minutes: int):
        self.hours = hours
        self.minutes = minutes

    def __gt__(self, other) -> bool:
        if self.hours > other.hours:
            return True
        elif self.hours == other.hours and self.minutes > other.minutes:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.__gt__(other) or self.__eq__(other):
            return True
        return False

    def __le__(self, other):
        if self.__lt__(other) or self.__eq__(other):
            return True
        return False

    def __lt__(self, other) -> bool:
        if self.hours < other.hours:
            return True
        elif self.hours == other.hours and self.minutes < other.minutes:
            return True
        else:
            return False

    def __eq__(self, other) -> bool:
        if self.hours == other.hours and self.minutes == other.minutes:
            return True
        return False
