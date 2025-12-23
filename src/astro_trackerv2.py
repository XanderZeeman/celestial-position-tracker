"""

   Name:   Xander Zeeman
   Student Number: 20466164
   Email:  23cyw2@queensu.ca
   Date: 2025-01-29

   I confirm that this assignment solution is my own work and conforms to
   Queen's standards of Academic Integrity
"""
import pygame as pg
import random as rand
from geopy.geocoders import Nominatim
from skyfield.api import load
from skyfield.api import wgs84
from datetime import datetime
def get_observer_location(address):
    """
    Description: This function will calculate the user's current longitude, latitude and alttude. 
    """
    geolocator = Nominatim(user_agent="celestial_tracker")
    location = geolocator.geocode(address, timeout = 10)
    if not location:
         print("Error: Unable to determine location")
         return None
    return location.latitude, location.longitude

def get_local_position(user_lat, user_lon, object_name, time_utc):
    """
    Description: This function will determine the positions of celestial objects as viewed from observer's position
    """
    planets = load('de421.bsp')
    earth = planets['earth'] 
    if object_name not in planets: 
        print(f"Error: '{object_name}' is not recognized. Try a planet, Moon or Sun.")
        return None
    target = planets[object_name]
    ts = load.timescale()
    observer = earth + wgs84.latlon(user_lat, user_lon)
    t = ts.utc(*time_utc)
    astrometric = observer.at(t).observe(target).apparent()
    alt, az, _ = astrometric.altaz()
    return alt.degrees, az.degrees

def azimuth_to_direction(azimuth):
    """
    Converts azimuth degrees into N/S/W/E directions.
    """
    directions = ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest"]
    index = round(azimuth / 45) % 8
    return directions[index]

def main():

    pg.init()
    screen = pg.display.set_mode((800,600))
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
               running = False
        BLACK = (0,0,0)
        GREEN = (0,51,0)
        screen.fill(BLACK)
        pg.draw.rect(screen, GREEN, (0, 375, 800, 250))
        for i in range(200):
            x = rand.randint(0,800)
            y = rand.randint(0,350)
            r = rand.randint(1,3)
            pg.draw.circle(screen, "white", (x,y), r)
        pg.display.flip()


        # Get user location
        print(load('de421.bsp'))
        address = input("Please input your current location (City, Country): ")
        location = get_observer_location(address)   
        if not location:
            return
        user_lat, user_lon = location

        # Get Object name
        object_name = input("Enter the celestial object you are looking for (e.g., 'Mars', 'Jupiter', 'Moon'): ")

        # Get date and time
        date_str = input("Enter your desired date and time in UTC (YYYY-MM-DD HH:MM:SS) or press enter for current time: ")
        if date_str.strip():
            try: 
                ts = load.timescale()
                time_utc = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").timetuple()[:6]
                #time_now = ts.now().utc_datetime().timetuple[:6]
                #if int(time_utc - time_now) > 0:
                      # moment = 1
                # elif (time_utc - time_now) < 0:
                     #           moment = -1
                # else:
                    # moment = 0
            
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD HH:MM:SS")
                return
    
        else:
            ts = load.timescale()
            time_utc = ts.now().utc_datetime().timetuple()[:6]
            #moment = 0

        # Get celestial object position
        position = get_local_position(user_lat, user_lon, object_name, time_utc)

        if not position:
            return

        altitude, azimuth = position
        direction = azimuth_to_direction(azimuth)

        # Display results:
        #if moment == 0:
        print(f"\n{object_name} is currently at: ")
        #elif moment == -1:
    #     print(f"\n{object_name} was at: ")
   # else:
    #    print(f"\n{object_name} will be at: ")

        print(f"  Altitude: {altitude:.2f}°")
        print(f"  Azimuth: {azimuth:.2f}° ({direction})")

        # Check visibility
        if altitude > 0:
            print(f"Look {direction} and {altitude:.2f}° above the horizon to find {object_name}.")
            running = False
        else:
            print(f"{object_name} is currently below the horizon and not visible.")
            running = False

if __name__ == "__main__":
    main()





