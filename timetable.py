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
from google_maps_location import get_travel_time
import pygame
from pygame.locals import *


class Timetable:
    """
    A class that will hold lecture locations and times.

    Instance Attributes:
        - table: a dictionary mapping days of the week to the locations of lectures at appropriate times.
        - lecture_codes: a list of all lectures to register for
    """
    table: dict[str, set[Session]]

    def __init__(self, lectures: list[Lecture]) -> None:
        """
        Create an empty timetable. Each element of the list represents one hour.

        Note: Timetable starts at 8:00 AM and goes to 10:00 PM
        """
        self.table = dict()
        for lecture in lectures:
            self.table[lecture.lect_code] = set()
            for session in lecture.sessions:
                self.table[lecture.lect_code].add(session)

    def get_sessions(self) -> set[Session]:
        """
        Return a set of all sesssions in the timetable
        """
        sessions = set()
        for lect_code in self.table:
            for session in self.table[lect_code]:
                sessions.add(session)

        return sessions

    def get_lecture_codes(self) -> list[str]:
        """
        Return a list of all lecture codes
        """
        lect_codes = []
        for lect_code in self.table:
            lect_codes.append(lect_code)
        return lect_codes

    def get_score(self, exclusion_days: set[str], start_end_times: tuple[int, int]) -> int | float:
        """
        Calculate the timetable score from the given sessions.
        """
        score = 100
        sessions = self.get_sessions()
        sessions_copy = self.get_sessions()
        prefered_start_time, prefered_end_time = start_end_times

        # Compare each session to one another to look for them being adjacent
        for session in sessions:
            for other_session in sessions_copy:
                # if they are adjacent, then check the amount of time it takes to walk from one location to another
                if session.adjacent(other_session) and session != other_session and session.location != "NA" \
                        and other_session.location != "NA":
                    travel_time = get_travel_time(session.location, other_session.location)
                    if travel_time > 10:
                        score -= travel_time

            if session.day in exclusion_days:
                score -= 10

            if session.start_time.hours < prefered_start_time:
                score -= 10
            if session.end_time.hours > prefered_end_time:
                score -= 10

            # To prevent 2 way score checking (we don't want to check distances between the same locations twice,
            # that would be a waste of both computing power and time from Google api)
            sessions_copy.remove(session)

        return score

    def output_timetable(self) -> None:
        """
        Use Plotly to output all sessions on the timetable into a chart
        """

#######################################################################
# TEST FUNCTION

def convert_to_lst(session: Session) -> list:
    """ This function was made for testing purposes in order to compare the resulting outputted time-table with the
     actual information. In case of errors. This converts a session to a primitive list form in order to directly
     see the information. It can be used in the main_file for example"""

    lst = [session.day, str(session.start_time.hours) + ':' + str(session.start_time.minutes) + '0',
           str(session.end_time.hours) + ':' + str(session.end_time.minutes) + '0', session.location]

    return lst
    
