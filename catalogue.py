"""
March 08, 2023
--------------
This file contains the Catalogue class which holds all the data from UoftSG courses.
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from typing import Optional, Any
import json
from course import Course
from lecture import Lecture
from session import Session
from time_h import Time
import csv


class Catalogue:
    """
    A class that holds all the data from CSC, STA, MAT courses of UofTSG in dictionaries.
    Instance Attributes:
        - data: the dictionary that maps cs courses to their corresponding information. (Example: "CSC111" is a key for
        the dictionary, and it will return a Course class.)
        - wanted_courses: a set that contains all the courses that the user wants to take.
        - building_codes: a dictionary going from building codes to actual addresses of uoft buildings
    Representation Invariants:
        - all(course in self.data for course in self.wanted_courses)
        - all(course[:3] == 'CSC' or course[:3] == 'MAT' or course[:3] == 'STA' in course for self.wanted_courses)
    """
    data: dict[str, Course]
    wanted_courses: set[str]
    building_codes: dict[str, str]

    def __init__(self, wanted_courses: set[str], term: str) -> None:
        """
        Given a set of courses that the user wants to take, find the data related to those courses (using JSON files)
        and put that information into self.data.
        Possible terms are:
        - S (winter)
        - F (fall) # This category includes Y (year-long) courses as well,
        since you can enrol in Y courses only during the Fall term.
        Preconditions:
        - term in {F, S} (Year-long courses are included in the 'F' category)
        - Courses in wanted_courses can be written in any of the following formats: 'CSC111', 'csc111', 'Csc111', etc.
        """
        self.wanted_courses = {course.upper() for course in wanted_courses}     # initializing the respective attributes
        self.data = {}
        self.building_codes = {}
        self.read_csv_building_code('building_names_and_addresses.csv')

        with open('all_data.json') as file:      # loading the data from dataset
            raw_data = json.load(file)

        # Either the input term is "F", in which case we're looking for the courses with
        # "F" and "Y" section codes, or the input term is "S", in which case we're looking
        # for the courses with "S" section code only.
        for course_name in raw_data:   # traversing each course in the dataset
            if course_name[:6] in self.wanted_courses and (course_name[9] == term or
                                                           (term == "F" and course_name[9] == 'Y')):
                course_info = raw_data[course_name]['meetings']
                lectures = []
                for lecture_name in course_info:   # traversing each lecture/tutorial in the current course
                    if lecture_name[:3] == 'LEC':   # excluding the "tutorials"
                        sessions_info = course_info[lecture_name]['schedule']
                        sessions = []
                        for session in sessions_info:      # traversing each session in the current lecture
                            if sessions_info[session]["meetingStartTime"] is not None:
                                start_time_hour = int(sessions_info[session]["meetingStartTime"][:2])
                                start_time_min = int(sessions_info[session]["meetingStartTime"][3:])
                                start_time = Time(start_time_hour, start_time_min)  # initializing the start time

                                end_time_hour = int(sessions_info[session]["meetingEndTime"][:2])
                                end_time_min = int(sessions_info[session]["meetingEndTime"][3:])
                                end_time = Time(end_time_hour, end_time_min)    # initializing the end time

                                day = sessions_info[session]["meetingDay"]  # extracting the day info
                                # TEMP
                                if sessions_info[session]["assignedRoom1"] is not None:
                                    location = self.uoft_building_to_address(
                                        sessions_info[session]["assignedRoom1"][:2])
                                else:
                                    location = "NA"

                                # initializing the Session() class with the relevant info
                                session = Session((start_time, end_time), day, location)
                                sessions += [session]   # adding it into the sessions list

                        if sessions:
                            # getting the right lecture code format for the Lecture() class
                            lect_code = f'{course_name[:6]} {lecture_name}'
                            # initializing the Lecture() class with the relevant info
                            lecture = Lecture(lect_code, sessions)
                            lectures += [lecture]

                if lectures:
                    # initializing the Course() class with the relevant info
                    self.data[course_name[:6]] = Course(lectures)

        # this branch shouldn't be reached as long as the preconditions are followed.
        # it checks if all courses in the input wanted_courses set could be found in the dataset.
        for course_name in self.wanted_courses:
            if course_name not in self.data:
                raise KeyError(f'{course_name} is not a valid course code or is not offered in {term} term')

    def get_possible_lect_sessions(self, course: str) -> list[Lecture]:
        """
        Given a course code, return a list of all possible lecture sections for that course.
        Preconditions:
        - course in self.data
        - term in {'F', 'W'}
        - course can be written in any of the following formats: 'CSC111', 'csc111', 'Csc111', etc.
        """
        return self.data[course.upper()].available_lectures

    def uoft_building_to_address(self, building_code: str) -> str:
        """
        Given a uoft building code, return an address that is usable by google maps.
        """
        if building_code in self.building_codes:
            return self.building_codes[building_code]
        else:
            return "NA"

    def read_csv_building_code(self, csv_file: str) -> None:
        """
        Read a csv file and update self.building_code.
        Match the building codes of uoft buildings to their actual addresses for google maps to use.
        """
        with open(csv_file) as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                for i in range(0, 1):
                    self.building_codes[str(row[i+1])] = str(row[i])


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
