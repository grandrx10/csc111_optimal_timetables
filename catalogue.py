"""
March 08, 2023
--------------
This file contains the Catalogue class which holds all of the data from UoftSG courses.
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
        self.wanted_courses = {course.upper() for course in wanted_courses}
        self.data = {}
        self.building_codes = {}
        self.read_csv_building_code('building_names_and_addresses.csv')

        with open('all_data.json') as file:
            raw_data = json.load(file)

        for course_name in raw_data:
            if course_name[:6] in self.wanted_courses and (course_name[9] == term or
                                                           (term == "F" and course_name[9] == 'Y')):
                course_info = raw_data[course_name]['meetings']
                lectures = []
                for lecture_name in course_info:
                    if lecture_name[:3] == 'LEC':
                        sessions_info = course_info[lecture_name]['schedule']
                        sessions = []
                        for session in sessions_info:
                            if sessions_info[session]["meetingStartTime"] is not None:
                                start_time_hour = int(sessions_info[session]["meetingStartTime"][:2])
                                start_time_min = int(sessions_info[session]["meetingStartTime"][3:])
                                start_time = Time(start_time_hour, start_time_min)

                                end_time_hour = int(sessions_info[session]["meetingEndTime"][:2])
                                end_time_min = int(sessions_info[session]["meetingEndTime"][3:])
                                end_time = Time(end_time_hour, end_time_min)

                                day = sessions_info[session]["meetingDay"]

                                if location_is_valid(sessions_info[session]["assignedRoom1"]):
                                    location = self.uoft_building_to_address(
                                        sessions_info[session]["assignedRoom1"][:2])
                                elif location_is_valid(sessions_info[session]["assignedRoom2"]):
                                    location = self.uoft_building_to_address(
                                        sessions_info[session]["assignedRoom2"][:2])
                                else:
                                    location = "NA"

                                session = Session((start_time, end_time), day, location)

                                sessions += [session]

                        if sessions:
                            lect_code = f'{course_name[:6]} {lecture_name}'
                            lecture = Lecture(lect_code, sessions)
                            lectures += [lecture]

                if lectures:
                    self.data[course_name[:6]] = Course(lectures)

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
        return self.building_codes[building_code]

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


def location_is_valid(location: str) -> bool:
    """Check if the given location is a valid building code at UofT"""
    if location is not None and location != '':
        if location[-1] in set(range(0, 10)):
            return True
    return False
