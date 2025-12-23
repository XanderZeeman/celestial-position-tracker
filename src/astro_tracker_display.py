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
        if object_name == "Jupiter" or object_name == "jupiter":
            object_name = "Jupiter barycenter"
        elif object_name == "Saturn" or object_name == "saturn":
            object_name = "Saturn barycenter"
        elif object_name == "Uranus" or object_name == "uranus":
            object_name = "Uranus barycenter"
        elif object_name == "Neptune" or object_name == "neptune":
            object_name = "Neptune barycenter"
        elif object_name == "Pluto" or object_name == "pluto":
            object_name = "Pluto barycenter"
        else:
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

def question_phase_where():
    pg.init()
    screen = pg.display.set_mode((1250,200))
    clock = pg.time.Clock()
    font = pg.font.SysFont(None, 30)
    address_text = "Please input your current location (City, Country). Click the screen to begin, and press ENTER to submit your response: "
    input_active = False
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
               running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                input_active = True
                address_text = ""
            elif event.type == pg.KEYDOWN and input_active:
                if event.key == pg.K_RETURN:
                    input_active = False
                    return address_text
                    running = False
                elif event.key == pg.K_BACKSPACE:
                    address_text = address_text[:-1]
                else:
                    address_text += event.unicode

            screen.fill(80)
            text_surf = font.render(address_text, True, (255,255,200))
            screen.blit(text_surf, text_surf.get_rect(center = screen.get_rect().center))
            pg.display.flip()

def question_phase_what():
    pg.init()
    screen = pg.display.set_mode((1250,200))
    clock = pg.time.Clock()
    font = pg.font.SysFont(None, 30)
    object_text = "Enter the celestial object you are looking for (e.g.,'Mars','Jupiter','Moon'). Click the screen to begin: "
    input_active = False
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
               running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                input_active = True
                object_text = ""
            elif event.type == pg.KEYDOWN and input_active:
                if event.key == pg.K_RETURN:
                    input_active = False
                    return object_text
                    running = False
                elif event.key == pg.K_BACKSPACE:
                    object_text = object_text[:-1]
                else:
                    object_text += event.unicode

            screen.fill(80)
            text_surf = font.render(object_text, True, (255,255,200))
            screen.blit(text_surf, text_surf.get_rect(center = screen.get_rect().center))
            pg.display.flip()

def question_phase_when():
    pg.init()
    screen = pg.display.set_mode((1250,200))
    clock = pg.time.Clock()
    font = pg.font.SysFont(None, 30)
    date_text = "Enter your desired date and time in UTC (YYYY-MM-DD HH:MM:SS) or press Enter for current time. Click the screen to begin: "
    input_active = False
    running = True
    #textbox = pg.textfield((100,100))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
               running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                input_active = True
                date_text = ""
            elif event.type == pg.KEYDOWN and input_active:
                if event.key == pg.K_RETURN:
                    return date_text
                    input_active = False
                    running = False
                elif event.key == pg.K_BACKSPACE:
                    date_text = date_text[:-1]
                else:
                    date_text += event.unicode

            screen.fill(80)
            text_surf = font.render(date_text, True, (255,255,200))
            screen.blit(text_surf, text_surf.get_rect(center = screen.get_rect().center))
            pg.display.flip()
        
def display_greatness(planet, altitude, direction):
    pg.init()
    screen = pg.display.set_mode((800,600))
    running = True
    fella = pg.image.load("big_fella.png")
    fella = pg.transform.scale(fella, (250,250))
    if 0 <= altitude <= 10:
        assistant = pg.image.load("Assistant.png")
    #elif 10 < altitude <= 20:
        #assis
    #assistant = pg.transform.scale(assistant, (180, 200))
    if planet == "moon" or planet == "Moon":
        object = pg.image.load("moon.webp")
        object = pg.transform.scale(object, (80,80))
    if planet == "mars"or planet == "Mars":
        object = pg.image.load("3D_Mars.png")
        object = pg.transform.scale(object, (80,80))
    if planet == "mercury" or planet == "Mercury":
        object = pg.image.load("3D_Mercury.png")
        object = pg.transform.scale(object, (80,80))
    if planet == "venus" or planet == "Venus":
        object = pg.image.load("Venus.png")
        object = pg.transform.scale(object, (80,80))
    if planet == "jupiter" or planet == "Jupiter":
        object = pg.image.load("Jupiter.png")
        object = pg.transform.scale(object, (80,80))
    if planet == "saturn" or planet == "Saturn":
        object = pg.image.load("Saturnx.png")
        object = pg.transform.scale(object, (80,80))
    if planet == "uranus" or planet == "Uranus":
        object = pg.image.load("uranus.webp")
        object = pg.transform.scale(object, (80,80))    
    if planet == "neptune" or planet == "Neptune":
        object = pg.image.load("neptune.webp")
        object = pg.transform.scale(object, (80,80))
    if planet == "pluto" or planet == "Pluto":
        object = pg.image.load("pluto.webp")
        object = pg.transform.scale(object, (80,80))


    BLACK = (0,0,0)
    GREEN = (0,51,0)
    screen.fill(BLACK)
    pg.draw.rect(screen, GREEN, (0, 375, 800, 250))
    for i in range(200):
        x = rand.randint(0,800)
        y = rand.randint(0,370)
        r = rand.randint(1,3)            
        pg.draw.circle(screen, "white", (x,y), r)
    screen.blit(fella,(110,325))
    #screen.blit(assistant,(230, 390))
    screen.blit(object, (600,100))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
               running = False
        
        
        pg.display.flip()
        
        


    
def main():
        # Get user location
        #print(load('de421.bsp'))
        address = question_phase_where() #input("Please input your current location (City, Country): ")
        location = get_observer_location(address)   
        if not location:
            return
        user_lat, user_lon = location

        # Get Object name
        object_name = question_phase_what() #input("Enter the celestial object you are looking for (e.g., 'Mars', 'Jupiter', 'Moon'): ")

        # Get date and time
        date_str = question_phase_when() #input("Enter your desired date and time in UTC (YYYY-MM-DD HH:MM:SS) or press enter for current time: ")
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
            display_greatness(object_name,altitude,direction)
           
        else:
            print(f"{object_name} is currently below the horizon and not visible.")
            


        
if __name__ == "__main__":
    main()





