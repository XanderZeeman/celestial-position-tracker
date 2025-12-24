from flask import Flask, render_template, request
from src.astronomy import get_local_position, azimuth_to_direction, get_observer_location
from datetime import datetime
from skyfield.api import load

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        address = request.form.get("address")
        object_name = request.form.get("object")
        date_str = request.form.get("datetime")

        location = get_observer_location(address)
        if not location:
            error = "Could not determine location."
        else:
            user_lat, user_lon = location

            if date_str:
                try:
                    time_utc = datetime.strptime(
                        date_str, "%Y-%m-%d %H:%M:%S"
                    ).timetuple()[:6]
                except ValueError:
                    error = "Invalid datetime format."
                    time_utc = None
            else:
                ts = load.timescale()
                time_utc = ts.now().utc_datetime().timetuple()[:6]

            if time_utc and not error:
                position = get_local_position(
                    user_lat, user_lon, object_name, time_utc
                )

                if not position:
                    error = "Invalid celestial object."
                else:
                    altitude, azimuth = position
                    direction = azimuth_to_direction(azimuth)

                    result = {
                        "object": object_name,
                        "altitude": round(altitude, 2),
                        "azimuth": round(azimuth, 2),
                        "direction": direction,
                        "visible": altitude > 0
                    }

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
