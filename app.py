from flask import Flask, render_template, request
from src.astronomy import get_local_position, azimuth_to_direction, get_observer_location
from datetime import datetime
from skyfield.api import load


from flask import jsonify
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/position", methods=["POST"])
def api_position():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400


    address = data.get("address")
    object_name = data.get("object")
    date_str = data.get("datetime")

    if not address or not object_name:
        return jsonify({"error": "Address and object are required"}), 400

    location = get_observer_location(address)
    if not location:
        return jsonify({"error": "Could not determine location"}), 400

    user_lat, user_lon = location

    if date_str:
        try:
            time_utc = datetime.strptime(
                date_str, "%Y-%m-%d %H:%M:%S"
            ).timetuple()[:6]
        except ValueError:
            return jsonify({"error": "Invalid datetime format"}), 400
    else:
        ts = load.timescale()
        time_utc = ts.now().utc_datetime().timetuple()[:6]

    position = get_local_position(user_lat, user_lon, object_name, time_utc)
    if not position:
        return jsonify({"error": "Invalid celestial object"}), 400

    altitude, azimuth = position
    direction = azimuth_to_direction(azimuth)
    altitude = float(altitude)
    azimuth = float(azimuth)
    visible = altitude > 0


    return jsonify({
        "object": object_name,
        "latitude": float(user_lat),
        "longitude": float(user_lon),
        "altitude": round(altitude, 2),
        "azimuth": round(azimuth, 2),
        "direction": direction,
        "visible": visible
    })

if __name__ == "__main__":
    app.run(debug=True)
