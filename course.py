"""
March 09, 2023
--------------
This file contains the course class
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from lecture import Lecture


class Course:
    """
    A class that represents a lecture section. Includes all classes (their times and locations) for that lecture
    section.

    Instance Attributes:
        - available_lectures: a list of all possible lectures offered for this course
    """
    available_lectures: list[Lecture]

    def __init__(self, available_lectures: list[Lecture]) -> None:
        """
        Initialize a course with a list of available lectures for that course

        Test initialization:

        """
        self.available_lectures = available_lectures

    def get_available_lectures(self) -> list[Lecture]:
        """
        Returns all available lectures
        """
        return self.available_lectures


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
