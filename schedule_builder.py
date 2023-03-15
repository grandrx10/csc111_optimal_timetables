"""
March 12, 2023
--------------
This file contains the schedule class, which will be used by schedule_builder
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from typing import Optional, Any
from lecture import Lecture
from catalogue import Catalogue
from schedule import Schedule

DEFAULT_LECTURE = Lecture('', [])


class ScheduleBuilder:
    """
    A class that will intake a few courses and build a full tree (Schedule) class out of it. This class will be
    responsible for getting the appropriate course codes and times.
    """
    catalogue: Catalogue

    def __init__(self):
        """
        Initialize the schedule builder Nothing really needs to be done here.
        """

    def run_builder(self) -> None:
        """
        When this function is called, it should take user input, make a catalogue, then set self.catalogue to that
        catalogue.

        At the end of this function, the schedule builder should output a schedule/timetable display.
        """

    def ask_user_for_courses(self) -> set[str]:
        """
        This function will ask the user (in console) for what courses they want to take. They should type the
        course codes in one at a time.

        Example:

            Enter your course codes below:
            CSC111
            Next course code:
            MAT137
            Next course code:
            ...

        You are free to change how the course codes are recieved. Just make sure to return a set of the courses.
        """

    def construct_schedule(self, wanted_courses: set[str]) -> Schedule:
        """
        With a given set of courses that are wanted, construct a Schedule Class and return it.

        Implementation Notes:
        - Make sure the catalogue is properly set before this function is called
        - Schedule should have all possible lecture sections for each course added to it in a tree pattern
        - This allows for the best schedule to be determined by calling Schedule.get_best_timetable()
        """
