
from flask import (
    Blueprint,
    render_template,
    jsonify,
    request
)

from model.map_point import MapPoint


def map_routes(
    gps_handler,
    add_point_callback,
    points_provider
):

    bp = Blueprint("map", __name__)

    @bp.route("/map")
    def map_page():
        return render_template("map.html")

    @bp.route("/gps")
    def gps():

        data = gps_handler.get_current_position()

        if data is None:
            return jsonify({
                "latitude": None,
                "longitude": None
            })

        return jsonify({
            "latitude": data.latitude,
            "longitude": data.longitude
        })

    @bp.route("/map_point", methods=["POST"])
    def map_point():

        data = request.json

        point = MapPoint(
            data["latitude"],
            data["longitude"]
        )

        add_point_callback(point)

        return jsonify({"saved": True})

    @bp.route("/points")
    def points():

        result = []

        for p in points_provider():

            result.append({
                "latitude": p.latitude,
                "longitude": p.longitude,
                "visited": p.visited,
                "time": p.time,
                "sequence": p.sequence,       # HOZZÁADVA
                "in_database": p.in_database  # HOZZÁADVA
            })

        return jsonify(result)

    return bp
