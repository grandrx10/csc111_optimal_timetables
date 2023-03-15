"""
March 09, 2023
--------------
This file contains the course class
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from typing import Optional, Any
from session import Session
from time_h import Time
from lecture import Lecture


class Course:
    """
    A class that represents a lecture section. Includes all classes (their times and locations) for that lecture
    section.

    Instance Attributes:
        - available_lectures: a list of all possible lectures offered for this course
    """
    available_lectures: list[Lecture]

    def __init__(self, available_lectures: list[Lecture]) -> None:
        """
        Initialize a course with a list of available lectures for that course

        Test initialization:

        """
        self.available_lectures = available_lectures

    def get_available_lectures(self) -> list[Lecture]:
        """
        Returns all available lectures
        """
        return self.available_lectures
