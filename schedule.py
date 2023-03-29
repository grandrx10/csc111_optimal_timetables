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
from session import Session
from timetable import Timetable
from time_h import Time

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
        # TODO Testing / Update lecture.conflict to deal with the case when root_lecture == DEFAULT_LECTURE(1st course)

        # Create a copy of 'lectures', with only lectures that do not have conflicts with current lecture
        lectures_copy = []
        for lecture in lectures:
            #  For each lecture,if it does not have a conflict, add it to the new list
            if not lecture.conflict(self.root_lecture):
                lectures_copy.append(lecture)

        # Base Case (We are at a leaf)
        if len(self.subtrees) == 0:
            # Add new schedules with their roots being the lectures
            for lecture in lectures_copy:
                self.subtrees[lecture.lect_code] = Schedule(lecture)

        else:

            # Otherwise, recurse into the subtrees
            for subtree in self.subtrees:
                if len(lectures_copy) != 0:
                    # Recursively call add_course into the subtrees, with the new list of lectures,
                    # if the list is non-empty
                    self.subtrees[subtree].add_course(lectures_copy)

    def get_valid_paths(self, courses_count: int) -> list[list[str]]:
        """
        Return all valid paths within the schedule (by course code)

        Implementation Notes:
        - if the path does not have the correct number of courses, do not add it to the list.
        - otherwise, add the lecture code (string) of the lectures to the list
        - for each new path, add a new list
        """
        paths = self._helper_get_paths(courses_count, 0)
        for i in range(len(paths)-1, 0, -1):
            if len(paths[i]) < courses_count:
                paths.pop(i)

        return paths

    def _helper_get_paths(self, depth_to_reach: int, curr_depth: int) -> list[list[str]]:
        """
        Helper method to recursively return all valid paths of at a certain depth of the schedule
        """
        if curr_depth == depth_to_reach:
            return [[self.root_lecture.lect_code]]
        else:
            paths = []
            for i in self.subtrees:
                # self.subtrees[i] refers to the schedule below this one in the recursive tree
                returned_list = self.subtrees[i]._helper_get_paths(depth_to_reach, curr_depth + 1)

                # Note, this is for the case that we are on the starting lecture (default lect)
                # We do not want to include the starting lecture in our returned list.
                if curr_depth != 0:
                    for c in range(len(returned_list)):
                        returned_list[c].insert(0, self.root_lecture.lect_code)
                paths.extend(returned_list)

            return paths

    def calculate_score(self, timetable: Timetable, path: list[str]) -> float:
        """
        With a given path, find the score that the path returns.

        Implementation Notes:
        - As you recurse, use the timetable to keep track of previous locations and times
        - Check distance between locations if they are back to back
        """
        # TODO IMPLEMENT

    def get_best_path(self, course_count: int) -> list[str]:
        """
        Given the correct number of courses to look for, find the path in the tree such that it returns the best
        possible timetable.
        """
        # TODO IMPLEMENT

    def get_timetable(self, path: list[str]) -> Timetable:
        """
        Given a path through the tree, construct a timetable and return it.

        If the path is not valid, then raise a value error.
        """
        path_copy = path.copy()
        path_copy.reverse()
        sessions = self._get_list_sessions_in_path(path_copy)
        return Timetable(sessions)

    def _get_list_sessions_in_path(self, path: list[str]) -> list[Session]:
        """
        A helper method that recurses and gets all the sessions in a schedule.
        """
        if len(path) == 0:
            sessions = []
            for session in self.root_lecture.sessions:
                sessions.append(session)

            return sessions
        else:
            sessions = []
            next_lect = path.pop()
            sessions.extend(self.subtrees[next_lect]._get_list_sessions_in_path(path))

            for session in self.root_lecture.sessions:
                sessions.append(session)

            return sessions
