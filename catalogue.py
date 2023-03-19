"""
March 08, 2023
--------------
This file contains the Catalogue class which holds all of the data from UoftSG courses.
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from typing import Optional, Any


class Catalogue:
    """
    A class that holds all of the data from UoftSG courses in dictionaries.

    Instance Attributes:
        - data: the dictionary that maps cs courses to their corresponding information. (Example: "CSC110" is a key for
        the dictionary, and it will return a Course class.
        - wanted_courses: a set that contains all of the courses that the user wants to take.

    Representation Invariants:
        - all(wanted_course in data for wanted_course in wanted_courses)

    """
    data: dict[str, Any]
    wanted_courses: set[str]

    def __init__(self, wanted_courses: set[str]) -> None:
        """
        Given a set of courses that the user wants to take, find the data related to those courses (using JSON files)
        and put that information into data.

        Implementation Notes:
            - make sure that data takes string keys (the course code) and returns a list of possible lectures
        """
        self.wanted_courses = wanted_courses

    def get_possible_lect_sessions(self, course: str) -> list[Any]:
        """
        Given a course code, return a list of all possible lecture sections for that course.
        """
        # TODO Riyad please implement this.
