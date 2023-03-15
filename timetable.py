"""
March 12, 2023
--------------
This file contains the timetable class, which will be used by schedule to keep track of locations and times
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from typing import Optional, Any
from lecture import Lecture
from session import Session
from time_h import Time


class Timetable:
    """
    A class that will hold lecture locations and times.

    Instance Attributes:
        - table: a dictionary mapping days of the week to the locations of lectures at appropriate times.
    """
    table: dict[str, list[str]]

    def __init__(self) -> None:
        """
        Create an empty timetable. Each element of the list represents one hour.

        Note: Timetable starts at 8:00 AM and goes to 10:00 PM
        """
        self.table = dict()
        self.table["Mon"] = [''] * 18
        self.table["Tue"] = [''] * 18
        self.table["Wed"] = [''] * 18
        self.table["Thu"] = [''] * 18
        self.table["Fri"] = [''] * 18

    def get_time_slot(self, start_time: Time, end_time: Time) -> tuple[int, int]:
        """
        Given a start and end time, return the corresponding start and end index position

        Examples:
            - 8:00 to 9:00 should return (0, 1)
            - 12:00 to 15:00 should return (4, 7)
            - 1:00 to 8:00 should raise a value error, since that is outside the range of our timetable.
        """

    def add_session(self, session: Session) -> None:
        """
        Add the given session to the schedule.

        Implementation Notes:
        - Fill in the slots at the correct corresponding times.
        - since the actual position of the item in the list will keep track of the time, as the actual string, put the
        building location.
        """

    def add_lecture(self, lecture: Lecture) -> None:
        """
        Given a lecture, place the lecture's sessions into the table.
        """
