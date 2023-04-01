"""
March 29, 2023
--------------
This file contains the get_travel_time method which'll be used to get the amount of time it takes to walk betwen
two places.
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

import googlemaps
import datetime
API_KEY = 'AIzaSyDmhjbDyLYlW-2OQyvcLt0qjOYKDozhUt8'
gmaps = googlemaps.Client(key=API_KEY)


def get_travel_time(start_location: str, end_location: str) -> int:
    """
    Return the time taken to travel between two addresses in minutes
    """
    direction = gmaps.directions(start_location, end_location, mode="walking", departure_time=datetime.datetime.now())
    time = direction[0]['legs'][0]['duration']['value']

    return time // 60


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })
