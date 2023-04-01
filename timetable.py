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
import plotly.graph_objs as go


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

    ######################################################################
    # THE FOLLOWING FUNCTIONS ALL CONTRIBUTE TO OUTPUTTING THE TIMETABLE #
    ######################################################################
    def max_time(self) -> int:
        """
        Return the maximum time in a schedule. This will enable us get the length of our timetable.
        """
        big = 0
        for lectures in self.table:
            for sessions in self.table[lectures]:
                compare = sessions.end_time.hours
                if compare > big:
                    big = compare
        return big

    def time_block(self) -> list[str]:
        """
        This returns a list of time units to create our table with.
        """
        time_lst = ['']

        for i in range(9, self.max_time()):
            time_lst.append(str(i) + ' :00' + ' - ' + str(i + 1) + ' :00')  # this space needs to be here

        return time_lst

    def skeleton(self) -> tuple[list, list[list[str]]]:
        """ This will return a tuple containing a list of lecture hours and as many lists of lists as the number of
        lecture hours. Each list in the list of lists has max 5 entries (for 5 days of the week)
        Each list from index 1 to a maximum of 13 represents an hour (i.e 9:00 - 10:00). Index 0 represents day of the
        week. Each item in the list represents a lecture and lecture location arranged by order of days of the week.

        For example:(["", 9:00 - 10:00], [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        [math, chem, physics,"",""]] )

        This means math was taken on Monday, chem on Tuesday, physics on Wednesday all at the hours of 9-10 but on
        thursday and friday at the hours of 9-10, no classes were held.

        Essentially, this is the skeleton of our timetable which holds the information in the right order to be
        understood by plotly.

        Precondition:
        - 0 <= len(skeleton()[1]) <= 14
        - len(skeleton()[0]) == len(skeleton()[1])
        """

        result = [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']]

        some = len(self.time_block())
        index_time_check = self.time_block()

        for _ in range(0, some - 1):  # to produce as many columns as the maximum hour intervals
            result.append(["", "", "", "", ""])

        for i in range(0, some):  # index_1 in helper func
            if 'Monday' not in result[i]:
                for j in range(0, 5):  # every sublist must have max 5 things, j is index_2
                    for lect_code in self.table:
                        self.helper_func(result, i, j, index_time_check, lect_code)

        return index_time_check, result

    def helper_func(self, to_mutate: list, index1: int, index2: int, check: list, lect_code: str) -> None:
        """
        This helper function has the responsibility of breaking our code into sizeable chunks in order to get a list
        that will be used in the final output.

        - to_mutate is mutated by this code and is the returned list in get_table_information.
        - check is what this loop will essentially be checking to know if it's in a right spot to mutate the 'to_mutate'
        list
        """

        index_dict = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4}

        for session in self.table[lect_code]:
            if session.time_check(check[index1]):  # checking if in right time column
                day_index = index_dict[session.day]
                if index2 == day_index:
                    to_mutate[index1][index2] = lect_code + " " + "(" + session.location + ")"

    def output_timetable(self) -> None:
        """
        Output the generated timetable using plotly.
        """
        skeleton = self.skeleton()
        fig = go.Figure(data=[go.Table(
            header=dict(values=skeleton[0],
                        line_color='darkslategray',
                        fill_color='lightskyblue',
                        align='left'),
            cells=dict(values=skeleton[1],
                       line_color='darkslategray',
                       fill_color='lightcyan',
                       align='left'))
        ])

        fig.update_layout(width=2000, height=2000)
        fig.show()
