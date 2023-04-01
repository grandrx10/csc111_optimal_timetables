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

from timetable import convert_to_lst
import plotly.graph_objs as go
from session import Session

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
courses_not_valid = True
while courses_not_valid:
    courses_not_valid = False
    print("Please enter what courses you want one by one below. Type 'end' when you are done with your wanted courses.")
    # Ask the user for the courses they want
    courses = set()
    while user_input.lower() != "end":
        user_input = input("Enter course " + str(len(courses) + 1) + ": ")
        if user_input != "end":
            courses.add(user_input)

    # create the catalogue, from which the schedule will be built using.
    try:
        catalogue = Catalogue(courses, term)
    except KeyError:
        print("One or more of the entered courses were not valid.")
        courses_not_valid = True
        user_input = ""

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

# Initialize the catalogue and schedule tree
print("Creating timetable...")
schedule = Schedule(DEFAULT_LECTURE)

# Add the appropriate courses to the schedule tree
for course in courses:
    lect_list = catalogue.get_possible_lect_sessions(course)
    schedule.add_course(lect_list)

# Display the best timetable
print("Finding best timetable...")
best_timetable = schedule.get_best_timetable(len(courses), exclusion_days, (start_hour, end_hour))
print(best_timetable.get_lecture_codes())  # This is temporary until we get output working
for key in best_timetable.table:
    for session in best_timetable.table[key]:
        print(session.location)
# print("Displaying timetable...")
# best_timetable.output_timetable()


def max_time() -> int:
    """
    Return the maximum time in a schedule. This will enable us get the length of our timetable.
    """
    big = 0
    for lectures in best_timetable.table:
        for sessions in best_timetable.table[lectures]:
            compare = sessions.end_time.hours
            if compare > big:
                big = compare
    return big


def schedule_to_primitive() -> dict:
    """
    Convert a schedule to its primitive form, letting us see explicitly the attributes of the schedule. This is for
    testing purposes.
    """
    test_dict = {}
    for x in best_timetable.table:
        for y in best_timetable.table[x]:
            if x not in test_dict:
                test_dict[x] = [convert_to_lst(y)]
            else:
                test_dict[x].append(convert_to_lst(y))

    return test_dict


def time_block() -> list[str]:
    """
    This returns a list of time units to create our table with.
    """

    time_lst = ['']

    for i in range(9, max_time()):
        time_lst.append(str(i) + ' :00' + ' - ' + str(i + 1) + ' :00')  # this space needs to be here

    return time_lst


def skeleton() -> tuple[list, list[list[str]]]:
    """ This will return a tuple containing a list of lecture hours and as many lists of lists as the number of lecture
    hours. Each list in the list of lists has max 5 entries (for 5 days of the week)
    Each list from index 1 to a maximum of 13 represents an hour (i.e 9:00 - 10:00). Index 0 represents day of the week.
    Each item in the list represents a lecture and lecture location arranged by order of days of the week.

    For example:(["", 9:00 - 10:00], [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    [math, chem, physics,"",""]] )

    This means math was taken on Monday, chem on Tuesday, physics on Wednesday all at the hours of 9-10 but on
    thursday and friday at the hours of 9-10, no classes were held.

    Essentially, this is the skeleton of our timetable which holds the information in the right order to be understood
    by plotly.

    Precondition:
    - 0 <= len(skeleton()[1]) <= 14
    - len(skeleton()[0]) == len(skeleton()[1])
    """

    result = [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']]

    some = len(time_block())
    index_time_check = time_block()

    for _ in range(0, some - 1):  # to produce as many columns as the maximum hour intervals
        result.append(["", "", "", "", ""])

    for i in range(0, some):  # index_1 in helper func
        if 'Monday' in result[i]:  # This could have been Tuesday, Wednesday etc
            pass  # do nothing, the code should not end, but skip to the next element
        else:
            for j in range(0, 5):  # every sublist must have max 5 things, j is index_2
                for lectures in best_timetable.table:
                    helper_func(result, best_timetable.table[lectures], i, j, index_time_check, lectures)

    return (index_time_check, result)


def helper_func(to_mutate: list, info: set[Session], index1: int, index2: int, check: list, lec: str) -> None:
    """
    This helper function has the responsibility of breaking our code into sizeable chunks in order to get a list that
    will be used in the final output.

    - to_mutate is mutated by this code and is the returned list in get_table_information.
    - check is what this loop will essentially be checking to know if it's in a right spot to mutate the 'to_mutate'
    list
    """

    index_dict = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4}

    for sessions in info:
        if time_check(sessions, check[index1]):  # checking if in right time column
            day_index = index_dict[sessions.day]
            if index2 == day_index:
                to_mutate[index1][index2] = lec + " " + "(" + sessions.location + ")"
            else:
                pass  # wrong spot, move to the next day of the week
        else:
            pass  # wrong spot, move to the next time column


def time_check(session: Session, compare: str) -> bool:
    """
    Compare is a string in the form xy :00 - rz :00 where y and r may or may not be 0. Given the start and end time
    of the session, this function aims to tell us if the time is the same as the string or if the string is contained
    in the range between the start and end time.

    Precondition:
    - rx - xy in compare is == 1
    """

    compare_again = str.split(compare)

    if session.start_time.hours <= int(compare_again[0]) and session.end_time.hours >= int(compare_again[3]):
        return True
    else:
        return False


def output_timetable() -> None:
    """
    Output the generated timetable using plotly.
    """

    print(skeleton())
    fig = go.Figure(data=[go.Table(
        header=dict(values=skeleton()[0],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=skeleton()[1],
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='left'))
    ])

    fig.update_layout(width=2000, height=2000)
    fig.show()


# testing()  call this if you want to see the timetable in primitive form
output_timetable()
