# viewcontroller/web_ui.py

from flask import Flask, render_template, jsonify, request
import logging


class WebUI:
    def __init__(
        self,
        command_queue,
        gps_handler,
        add_point,
        get_points,
        save_points,
        load_points,
        clear_points,
        navigation,
        enable_flask_logs=False
    ):
        self.command_queue = command_queue
        self.gps_handler = gps_handler

        self.add_point = add_point
        self.get_points = get_points

        self.save_points = save_points
        self.load_points = load_points
        self.clear_points = clear_points

        self.navigation = navigation

        self.app = Flask(__name__)

        self.register_routes()
        
        self.enable_flask_logs = enable_flask_logs

    def register_routes(self):
        @self.app.route("/")
        def index():
            return render_template("manual.html")

        @self.app.route("/map")
        def map_page():
            return render_template("map.html")

        @self.app.route("/database")
        def database():
            return render_template("database.html")

        @self.app.route(
            "/command",
            methods=["POST"]
        )
        def command():
            cmd = request.json["command"]

            # manuális beavatkozás → azonnal álljon le az önjárás
            if self.navigation is not None:
                self.navigation.stop_navigation()

            self.command_queue.put(cmd)

            return jsonify({"ok": True})

        @self.app.route("/gps")
        def gps():
            data = (
                self.gps_handler
                .get_current_position()
            )

            if data is None:
                return jsonify(
                    {
                        "latitude": None,
                        "longitude": None
                    }
                )

            return jsonify(
                {
                    "latitude": data.latitude,
                    "longitude": data.longitude
                }
            )

        @self.app.route(
            "/map_point",
            methods=["POST"]
        )
        def map_point():
            data = request.json

            from model.map_point import MapPoint

            point = MapPoint(
                data["latitude"],
                data["longitude"]
            )

            self.add_point(point)

            return jsonify({"ok": True})

        @self.app.route("/points")
        def points():
            return jsonify(
                [
                    p.__dict__
                    for p in self.get_points()
                ]
            )

        @self.app.route(
            "/db/save",
            methods=["POST"]
        )
        def db_save():
            data = request.json or {}

            ids = data.get("ids")
            if ids is None:
                ids = data.get("indexes", [])

            self.save_points(ids)

            return jsonify({"ok": True})

        @self.app.route("/db/load")
        def db_load():
            self.load_points()
            return jsonify({"ok": True})

        @self.app.route(
            "/points/delete",
            methods=["POST"]
        )
        def delete_points():
            data = request.json or {}

            ids = data.get("ids")
            if ids is None:
                ids = data.get("indexes", [])

            self.clear_points(ids)

            return jsonify({"ok": True})

        @self.app.route(
            "/points/clear",
            methods=["POST"]
        )
        def clear():
            data = request.json or {}

            ids = data.get("ids")
            if ids is None:
                ids = data.get("indexes", [])

            self.clear_points(ids)

            return jsonify({"ok": True})

        # --- navigation endpoints ---

        @self.app.route(
            "/nav/start",
            methods=["POST"]
        )
        def nav_start():
            if self.navigation is not None:
                self.navigation.start_navigation()
            return jsonify({"ok": True})

        @self.app.route(
            "/nav/stop",
            methods=["POST"]
        )
        def nav_stop():
            if self.navigation is not None:
                self.navigation.stop_navigation()
            return jsonify({"ok": True})

        @self.app.route("/nav/status")
        def nav_status():
            if self.navigation is None:
                return jsonify(
                    {
                        "state": "disabled",
                        "target": None,
                        "distance": None,
                        "current_position": None
                    }
                )

            status = self.navigation.get_status()
            return jsonify(status)

    def run(self):
        import logging
        log = logging.getLogger('werkzeug')

        if not self.enable_flask_logs:
            log.setLevel(logging.ERROR)
        else:
            log.setLevel(logging.INFO)

        self.app.run(
            host="0.0.0.0",
            port=5000,
            debug=False,
            use_reloader=False
        )

