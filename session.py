"""
March 08, 2023
--------------
This file contains the session class
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from typing import Optional, Any
from time_h import Time


class Session:
    """
    A class that represents a single lecture session.

    Instance Attributes:
        - day: which day of the week does this lecture take place
        - start_time: at what time does this lecture start
        - end_time: at what time does this lecture end
        - location: the address where the lecture will take place
    """
    start_time: Time
    end_time: Time
    day: str
    location: str

    def __init__(self, time: tuple[Time, Time], day: str, location: str) -> None:
        """
        Initialize a session. The first element of the time tuple is the start time and
        the second element is the end time.

        Test intializer: session = Session(time=(Time(1, 15), Time(2, 30)), day="MON", location="THIS PLACE")
        """
        self.start_time = time[0]
        self.end_time = time[1]
        self.day = day
        self.location = location

    def conflict(self, other: Session) -> bool:
        """
        Return if this session conflicts with another session.
        >>> s1 = Session((Time(1, 40), Time(4, 20)), "MON", "Mining Building")
        >>> s2 = Session((Time(3, 0), Time(6, 0)), "MON", "Mining Building")
        >>> s1.conflict(s2)
        True
        >>> s3 = Session((Time(4, 30), Time(6, 0)), "MON", "Mining Building")
        >>> s1.conflict(s3)
        False
        """
        if self.day == other.day and self.start_time <= other.end_time and self.end_time >= other.start_time \
                and self.location == other.location:
            return True
        return False

    def adjacent(self, other: Session) -> bool:
        """
        Return if this session is directly adjacent to the other session (when this session ends, the other starts, or
        when this session starts is the end of the other session)
        >>> s1 = Session((Time(1, 40), Time(4, 20)), "MON", "Mining Building")
        >>> s2 = Session((Time(4, 20), Time(5, 20)), "MON", "Mining Building")
        >>> s1.adjacent(s2)
        True
        >>> s2.adjacent(s1)
        True
        """
        if self.day == other.day and (self.end_time == other.start_time or self.start_time == other.end_time):
            return True
