"""
March 29, 2023
--------------
This is the main file which, when run, will create an optimal schedule for you.
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from typing import Optional, Any
from lecture import Lecture
from catalogue import Catalogue
from schedule import Schedule
from timetable import Timetable
from google_maps_location import get_travel_time

DEFAULT_LECTURE = Lecture('', [])

print("Hello! Welcome to UofT course builder!")
user_input = ""
courses = set()

print("Which term do you want a schedule for? (Please enter F, S, Y)")
term = input().upper()

while term not in {"F", "S", "Y"}:
    print("Please enter F, S, Y to indicate which term you want the schedule for.")
    term = input().upper()

print("Please enter what courses you want one by one below. Type 'end' when you are done with your wanted courses.")
# Ask the user for the courses they want
while user_input.lower() != "end":
    user_input = input("Enter course " + str(len(courses) + 1) + ": ")
    if user_input != "end":
        courses.add(user_input)

print("Please enter which days you don't want to take classes below. Days are MO, TU, WE, TH, FR.")
print("Type 'end' when you are finished.")
exclusion_days = set()
user_input = ""
while user_input.lower() != "end":
    user_input = input("Enter day that you want to exclude: ")
    if user_input != "end" and user_input in {"MO", "TU", "WE", "TH", "FR"}:
        exclusion_days.add(user_input.upper())

# Initialize the catalogue and schedule tree
print("Creating timetable...")
catalogue = Catalogue(courses, term)
schedule = Schedule(DEFAULT_LECTURE)

# Add the appropriate courses to the schedule tree
for course in courses:
    lect_list = catalogue.get_possible_lect_sessions(course)
    schedule.add_course(lect_list)

# Display the best timetable
print("Finding best timetable...")
best_timetable = schedule.get_best_timetable(len(courses), exclusion_days)
print(best_timetable.get_lecture_codes())  # This is temporary until we get output working
# print("Displaying timetable...")
# best_timetable.output_timetable()