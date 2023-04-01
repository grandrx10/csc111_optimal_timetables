"""
March 12, 2023
--------------
This file contains the timetable class, which will be used by schedule to keep track of locations and times
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
import plotly.graph_objs as go
from lecture import Lecture
from session import Session
from google_maps_location import get_travel_time


class Timetable:
    """
    A class that will hold lecture locations and times.

    Instance Attributes:
        - table: a dictionary mapping lecture codes to the set of sessions that the lecture has
    """
    table: dict[str, set[Session]]

    def __init__(self, lectures: list[Lecture]) -> None:
        """
        Create a timetable with a given list of lectures
        """
        self.table = {}
        for lecture in lectures:
            # initialize an empty set for each lecture code
            self.table[lecture.lect_code] = set()
            # add all the sessions into the set
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
        Return a list of codes for all lectures in the timetable
        """
        lect_codes = []
        for lect_code in self.table:
            lect_codes.append(lect_code)
        return lect_codes

    def helper_get_score_travel(self, session: Session, other_session: Session, score: int | float) -> int | float:
        """
        A helper method for getting a score. This method will get the distance between two sessions and return
        a modified score based on the distance. This is to ensure that the optimal schedule has reduced walking time.
        """
        if session.location != "NA" and other_session.location != "NA":
            travel_time = get_travel_time(session.location, other_session.location)
            if travel_time > 10:
                score -= travel_time

        return score

    def get_score(self, exclusion_days: set[str], start_end_times: tuple[int, int]) -> int | float:
        """
        Calculate the timetable score from the given sessions. The parameters will include 2 items: exclusion_days
        and start_end_times.

        exclusion_days: days when the student doesn't want to go to school.
        start_end_times: the hour at which the student wants to start and end their day of school.

        Implementation Notes:
        - Start at a score of 100
        - For each imperfection in the timetable, subtract score
        - For each hour of classes outside the acceptable time range, subtract 5 points
        - Subtract score for amount of time it takes to walk between classes if it is more than 10 minutes walk (Do so
        only when the sessions are adjacent to one another.
        """
        score = 100
        sessions = self.get_sessions()
        sessions_copy = self.get_sessions()
        prefered_start_time, prefered_end_time = start_end_times

        # Compare each session to one another to look for them being adjacent
        for session in sessions:
            for other_session in sessions_copy:
                # if they are adjacent, then check the amount of time it takes to walk from one location to another
                if session.adjacent(other_session) and session != other_session:
                    score = self.helper_get_score_travel(session, other_session, score)

            if session.day in exclusion_days:
                score -= 10
            # Deduct points on how early in the day it starts compared to the prefered time
            if session.start_time.hours < prefered_start_time:
                score -= (prefered_start_time - session.start_time.hours) * 5
            # Deduct points on how late it ends compared to the prefered end time
            if session.end_time.hours > prefered_end_time:
                score -= (session.end_time.hours - prefered_end_time) * 5

            # To prevent 2 way score checking (we don't want to check distances between the same locations twice,
            # that would be a waste of both computing power and time from Google api)
            sessions_copy.remove(session)

        return score

    ######################################################################
    # THE FOLLOWING FUNCTIONS ALL CONTRIBUTE TO OUTPUTTING THE TIMETABLE #
    ######################################################################
    def max_time(self) -> int:
        """
        Return the maximum time in a set of sessions. This will enable us get the length of our timetable.
        """
        maximum = 0
        for lectures in self.table:
            for sessions in self.table[lectures]:
                compare = sessions.end_time.hours
                if compare > maximum:
                    maximum = compare
        return maximum

    def time_block(self) -> list[str]:
        """
        Return a list of time units to create the time-table with.
        """
        time_lst = ['']

        for i in range(9, self.max_time()):
            time_lst.append(str(i) + ' :00' + ' - ' + str(i + 1) + ' :00')

        return time_lst

    def skeleton(self) -> tuple[list[str], list[list[str]]]:
        """ Return a tuple containing a list of lecture hours and as many lists of lists as the number of
        lecture hours. Each list in the list of lists has max 5 entries (for 5 days of the week)
        Each list in the list of lists from index 1 to a maximum of 13 represents an hour (i.e 9:00 - 10:00). Index 0
        represents the days of the week. Each item in the list represents a lecture and lecture location arranged by
        order of days of the week.
        For example:(["", 9:00 - 10:00], [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        [math, chem, physics,"",""]] )
        This means math was taken on Monday, chem on Tuesday, physics on Wednesday all at the hours of 9-10 but on
        thursday and friday at the hours of 9-10, no classes were held.
        Essentially, this is the skeleton of our timetable which holds the information in the right order to be
        understood by plotly.
        Preconditions:
        - 0 <= len(self.skeleton()[1]) <= 14
        - len(self.skeleton()[0]) == len(self.skeleton()[1])
        - all([len(sublist) == 5 for sublist in self.skeleton()[1]])
        """

        result = [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']]

        # this is a list of times up to the maximum time in the produced set of sessions in a timetable class. We
        # check the indexes of this list with the time of the schedule to know if we are at the right spot.

        index_time_check = self.time_block()
        range_end = len(index_time_check)

        for _ in range(0, range_end - 1):  # to produce as many columns as the maximum hour intervals
            result.append(["", "", "", "", ""])

        for i in range(0, range_end):  # index_1 in helper func
            if 'Monday' not in result[i]:
                for j in range(0, 5):  # every sublist must have max 5 things, j is index_2 in helper_func
                    for lect_code in self.table:
                        self.helper_func(result, (i, j), index_time_check, lect_code)

        return index_time_check, result

    def helper_func(self, to_mutate: list, indexes: tuple[int, int], check: list, lect_code: str) -> None:
        """
        This helper function has the responsibility of breaking our code into sizeable chunks in order to get a result
        that will be used in the final output.
        - to_mutate: is the list mutated by this code and is the returned list in self.skeleton().
        - lect_code: is the lecture code that will be shown in our timetable.
        - check: is what this loop will essentially be checking to know if it's in a right spot to mutate the
        'to_mutate' list. It is a list of 1 hour lecture times up to the maximum lecture time in the produced
        set of sessions in a timetable class.
        - We are in a right spot when:
        1. check[index1] == the session's start to end time hour range or check[index1] is contained in the session's
        start - end time hour range (that is when the hour range of the session is longer than an hour)
        2. session.day corresponds to index2 in the sense that the days of the week all become numbers to check with
        index2. If they are the same, then we are at the right spot to add in time-table information.
        """
        index1, index2 = indexes
        index_dict = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4}  # if sesion.day corresponds checker

        for session in self.table[lect_code]:
            if session.time_check(check[index1]):  # checking if in right time column
                day_index = index_dict[session.day]
                if index2 == day_index:  # checking if in right day column
                    to_mutate[index1][index2] = lect_code + " " + "(" + session.location + ")"  # mutate!

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

        fig.update_layout(width=2500, height=2500)
        fig.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['lecture', 'session', 'google_maps_location', 'plotly.graph_objs'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
