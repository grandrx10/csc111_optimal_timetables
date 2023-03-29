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
    table: set[Session]

    def __init__(self) -> None:
        """
        Create an empty timetable. Each element of the list represents one hour.

        Note: Timetable starts at 8:00 AM and goes to 10:00 PM
        """
        self.sessions = set()

    def add_session(self, session: Session) -> None:
        """
        Add the given session to the schedule.

        Implementation Notes:
        - Fill in the slots at the correct corresponding times.
        - since the actual position of the item in the list will keep track of the time, as the actual string, put the
        building location.
        """
        self.sessions.add(session)

    def add_lecture(self, lecture: Lecture) -> None:
        """
        Given a lecture, place the lecture's sessions into the table.
        """
        for i in range(len(lecture.sessions)):
            self.sessions.add(lecture.sessions[i])

    def output_timetable(self) -> None:
        """
        Use Plotly or Pygame to output all sessions on the timetable into a chart
        """
        # HANNAH TODO

    def get_timetable_score(self) -> int | float:
        """
        Calculate the timetable score from the given sessions.
        """
        score = 100

        sessions_copy = self.sessions.copy()
        for session in self.sessions:
            for other_session in sessions_copy:
                if session.adjacent(other_session) and session != other_session:
                    travel_time = get_travel_time(session.location, other_session.location)
                    if travel_time > 10:
                        score -= travel_time

            # To prevent 2 way score checking (we don't want to check distances between the same locations twice,
            # that would be a waste of both computing power and time from Google api)
            sessions_copy.remove(session)

        return score


def get_travel_time(l1: str, l2: str) -> int | float:
    """
    return travel time
    """
    # TODO
