import googlemaps
import datetime
API_KEY = 'AIzaSyDmhjbDyLYlW-2OQyvcLt0qjOYKDozhUt8'
gmaps = googlemaps.Client(key=API_KEY)

def get_travel_time(start_location: str, end_location:str) -> int:
    """
    Return the time taken to travel between two addresses in minutes
    """
    dir = gmaps.directions(start_location, end_location, mode= "walking", departure_time = datetime.datetime.now())
    time = dir[0]['legs'][0]['duration']['value']

    return time // 60
