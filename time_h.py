"""
March 08, 2023
--------------
This file contains the time class
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from typing import Optional, Any


class Time:
    """
    This class holds the time.
    """
    hours: int
    minutes: int

    def __init__(self, hours: int, minutes: int):
        self.hours = hours
        self.minutes = minutes
