"""
March 08, 2023
--------------
This file contains the Catalogue class which holds all of the data from UoftSG courses.
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from typing import Optional, Any
from lecture import Lecture
from time_h import Time
from session import Session


class Catalogue:
    """
    A class that holds all of the data from UoftSG courses in dictionaries.

    Instance Attributes:
        - data: the dictionary that maps cs courses to their corresponding information. (Example: "CSC110" is a key for
        the dictionary, and it will return a Course class.
        - wanted_courses: a set that contains all of the courses that the user wants to take.
        - building_codes: a dictionary going from building codes to actual addresses of uoft buildings

    Representation Invariants:
        - all(wanted_course in data for wanted_course in wanted_courses)

    """
    data: dict[str, Lecture]
    wanted_courses: set[str]
    building_codes: dict[str, str]

    def __init__(self, wanted_courses: set[str], term: str) -> None:
        """
        Given a set of courses that the user wants to take, find the data related to those courses (using JSON files)
        and put that information into data.

        Possible terms are:
        - Y (year)
        - S (winter)
        - F (fall)

        Implementation Notes:
            - make sure that data takes string keys (the course code) and returns a list of possible lectures
        """
        self.wanted_courses = wanted_courses

    def get_possible_lect_sessions(self, course: str, term: str) -> list[Lecture]:
        """
        Given a course code, return a list of all possible lecture sections for that course.
        """
        # TODO Riyad please implement this.

    def uoft_building_to_address(self, building_code: str) -> str:
        """
        Given a uoft building code, return an address that is usable by google maps.
        """
        # TODO HANNAH IMPLEMENT THIS

    def read_csv_building_code(self, csv_file: str) -> None:
        """
        Read a csv file and update self.building_code.
        Match the building codes of uoft buildings to their actual addresses for google maps to use.
        """
        # TODO Hannah implement this
