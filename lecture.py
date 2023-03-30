"""
March 08, 2023
--------------
This file contains the lecture class, which will contain information on lecture time and location.
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from typing import Optional, Any
from session import Session
from time_h import Time


class Lecture:
    """
    A class that represents a lecture section. Includes all classes (their times and locations) for that lecture
    section.

    Instance Attributes:
        - sessions: a list of sessions that must be taken in this lecture section.
        - lect_code: Combine the course code with the lecture code. (Example: "csc111 lec101")
    """
    lect_code: str
    sessions: list[Session]

    def __init__(self, lect_code: str, sessions: list[Session]) -> None:
        """
        Initialize a lecture with a list of sessions

        Test initialization:
        >>> s1 = Session(time=(Time(1, 15), Time(2, 30)), day="MON", location="THIS PLACE")
        >>> s2 = Session(time=(Time(1, 15), Time(20, 30)), day="TUES", location="THAT PLACE")
        >>> lecture = Lecture([s1, s2])
        >>> lecture.sessions[0].day
        'MON'
        """
        self.sessions = sessions
        self.lect_code = lect_code

    def conflict(self, other: Lecture) -> bool:
        """
        Return if this lecture section conflicts with another lecture section.
        """
        for i in range(len(self.sessions)):
            for c in range(len(other.sessions)):
                if self.sessions[i].conflict(other.sessions[c]):
                    return True

        return False
