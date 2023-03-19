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
from timetable import Timetable

DEFAULT_LECTURE = Lecture('', [])


class Schedule:
    """
    A tree that holds many possible schedules. This is a recursive class that will store one course at each
    level.

    Instance Attributes:
        - root_lecture: the lecture at this level of the schedule
        - subtrees: the possible branching paths from this schedule
    """
    root_lecture: Lecture | None
    subtrees: dict[str, Schedule]

    def __init__(self, root_lecture: Lecture) -> None:
        self.root_lecture = root_lecture
        self.subtrees = {}

    def add_course(self, lectures: list[Lecture]) -> None:
        """
        Add a lecture to the schedule class.

        Implementation Notes:
        - If root_lecture is None, return
        - Make a copy of list lectures
        - If root_lecture conflicts with a lecture in lectures, remove that lecture from the copied list
        - Recurse into subtrees and add_course with copied list
        - Once there are no subtrees (you are at a leaf) then, add new schedules with their roots being the lectures.
        """

    def get_valid_paths(self, courses_count: int) -> list[list[str]]:
        """
        Return all valid paths within the schedule (by course code)

        Implementation Notes:
        - if the path does not have the correct number of courses, do not add it to the list.
        - otherwise, add the lecture code (string) of the lectures to the list
        - for each new path, add a new list
        """

    def calculate_score(self, timetable: Timetable, path: list[str]) -> float:
        """
        With a given path, find the score that the path returns.

        Implementation Notes:
        - As you recurse, use the timetable to keep track of previous locations and times
        - Check distance between locations if they are back to back
        """

    def find_travel_time(self, location1: str, location2: str) -> float | int:
        """
        Find the amount of time it takes to travel from one location to another using Google Maps API.
        """
        # TODO Hussain implement this

    def get_best_path(self, course_count: int) -> list[str]:
        """
        Given the correct number of courses to look for, find the path in the tree such that it returns the best
        possible timetable.
        """

    def get_timetable(self, path: list[str]) -> Timetable:
        """
        Given a path through the tree, construct a timetable and return it.

        If the path is not valid, then raise a value error.
        """
