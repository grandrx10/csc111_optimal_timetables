"""
March 29, 2023
--------------
This is the main file which, when run, will create an optimal schedule for you.
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from lecture import Lecture
from catalogue import Catalogue
from schedule import Schedule

DEFAULT_LECTURE = Lecture('', [])

print("Hello! Welcome to UofT course builder!")
user_input = ""

# Ask the user for which semester they are planning for
print("Which term do you want a schedule for? (Please enter F or S)")
term = input().upper()
while term not in {"F", "S"}:
    print("Please enter F or S to indicate which term you want the schedule for.")
    term = input().upper()

# This loop gets what courses the user wants. To catch courses that may be invalid, it will loop until
# all courses are valid.
courses = ...
catalogue = ...
schedule = ...
courses_not_valid = True
while courses_not_valid:
    user_input = ""
    courses_not_valid = False
    print("Please enter what courses you want one by one below. Type 'end' when you are done with your wanted courses.")
    # Ask the user for the courses they want
    courses = set()
    while user_input.lower() != "end" or len(courses) < 1:
        user_input = input("Enter course " + str(len(courses) + 1) + ": ")
        if user_input != "end":
            courses.add(user_input)

    # create the catalogue, from which the schedule will be built using.
    try:
        catalogue = Catalogue(courses, term)
    except KeyError:
        print("One or more of the entered courses were not valid.")
        courses_not_valid = True

    # Initialize the tree
    if courses_not_valid is False:
        schedule = Schedule(DEFAULT_LECTURE)
        # Add the appropriate courses to the schedule tree
        for course in courses:
            lect_list = catalogue.get_possible_lect_sessions(course)
            schedule.add_course(lect_list)
        # If the courses are completely conflicting with one another, then there is no possible timetable.
        if not schedule.get_valid_paths(len(courses)):
            courses_not_valid = True
            print("One or more of the entered courses completely conflict with one another!")

# Ask the user for which days they would prefer not to have school. This does NOT mean that it's guaranteeed.
print("Please enter which days you don't want to take classes below. Days are MO, TU, WE, TH, FR.")
print("Type 'end' when you are finished.")
exclusion_days = set()
user_input = ""
while user_input.lower() != "end":
    user_input = input("Enter day that you want to exclude: ")
    if user_input != "end" and user_input in {"MO", "TU", "WE", "TH", "FR"}:
        exclusion_days.add(user_input.upper())

# Ask the user for when they would prefer to start/end classes
print("Please enter at what hour you would prefer to start classes. (Earliest class is at 9, latest is at 22)")
user_input = input()
while not user_input.isnumeric() or not 9 <= int(user_input) <= 22:
    print("Please enter a valid hour.")
    user_input = input()
start_hour = int(user_input)

# Ask the user for when they would prefer to start/end classes
print("Please enter at what hour you would prefer to end classes. (Earliest class is at 9, latest is at 22)")
user_input = input()
while not user_input.isnumeric() or not 9 <= int(user_input) <= 22:
    print("Please enter a valid hour.")
    user_input = input()
end_hour = int(user_input)

# Display the best timetable
print("Finding best timetable...")
best_timetable = schedule.get_best_timetable(len(courses), exclusion_days, (start_hour, end_hour))
print("Displaying timetable...")
best_timetable.output_timetable()
