
from geopy.geocoders import Nominatim
from skyfield.api import load, wgs84


planets = load('de421.bsp')
earth = planets['earth']
ts = load.timescale()

def get_observer_location(address):
    geolocator = Nominatim(user_agent="celestial_tracker")
    location = geolocator.geocode(address, timeout=10)
    if not location:
        return None
    return location.latitude, location.longitude


def get_local_position(user_lat, user_lon, object_name, time_utc):
    if object_name not in planets:
        mapping = {
            "Jupiter": "Jupiter barycenter",
            "Saturn": "Saturn barycenter",
            "Uranus": "Uranus barycenter",
            "Neptune": "Neptune barycenter",
            "Pluto": "Pluto barycenter"
        }
        object_name = mapping.get(object_name.capitalize())
        if not object_name:
            return None

    target = planets[object_name]
    observer = earth + wgs84.latlon(user_lat, user_lon)
    t = ts.utc(*time_utc)

    astrometric = observer.at(t).observe(target).apparent()
    alt, az, _ = astrometric.altaz()
    return alt.degrees, az.degrees

def azimuth_to_direction(azimuth):
    directions = [
        "North", "Northeast", "East", "Southeast",
        "South", "Southwest", "West", "Northwest"
    ]
    index = round(azimuth / 45) % 8
    return directions[index]