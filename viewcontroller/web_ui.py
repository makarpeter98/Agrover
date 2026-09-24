# viewcontroller/web_ui.py

from flask import Flask, render_template, jsonify, request
from database.map_point import MapPoint
import logging


class WebUI:

    def __init__(
        self,
        drive_command,
        gps_handler,
        add_point,
        get_points,
        save_points,
        load_points,
        clear_points,
        navigation,
        navigation_direct_drive, 
        set_visited,
        get_setting,
        set_setting,
        enable_flask_logs=False
    ):

        self.drive_command = drive_command
        self.gps_handler = gps_handler

        self.add_point = add_point
        self.get_points = get_points

        self.save_points = save_points
        self.load_points = load_points
        self.clear_points = clear_points
        self.set_visited = set_visited

        self.get_setting = get_setting
        self.set_setting = set_setting

        self.navigation = navigation
        self.navigation_direct_drive = navigation_direct_drive

        self.enable_flask_logs = enable_flask_logs

        self.app = Flask(__name__)

        self.register_routes()


    def register_routes(self):

        # ---------------------------------------------------------
        # PAGES
        # ---------------------------------------------------------

        @self.app.route("/")
        def index():

            return render_template(
                "manual.html"
            )


        @self.app.route("/map")
        def map_page():

            return render_template(
                "map.html"
            )


        @self.app.route("/database")
        def database():

            return render_template(
                "database.html"
            )


        @self.app.route("/settings")
        def settings():

            return render_template(
                "settings.html"
            )


        # ---------------------------------------------------------
        # SETTINGS
        # ---------------------------------------------------------

        @self.app.route(
            "/settings/<setting_name>",
            methods=["GET"]
        )
        def get_setting(setting_name):

            value = self.get_setting(
                setting_name
            )

            if value is None:

                return jsonify({
                    "ok": False,
                    "error": "Setting not found"
                }), 404


            return jsonify({
                "ok": True,
                "setting_name": setting_name,
                "value": value
            })


        @self.app.route(
            "/settings/<setting_name>",
            methods=["POST"]
        )
        def set_setting(setting_name):

            data = request.json or {}

            if "value" not in data:

                return jsonify({
                    "ok": False,
                    "error": "Missing value"
                }), 400


            self.set_setting(
                setting_name,
                data["value"]
            )


            return jsonify({
                "ok": True,
                "setting_name": setting_name,
                "value": data["value"]
            })


        # ---------------------------------------------------------
        # MANUAL CONTROL
        # ---------------------------------------------------------

        @self.app.route(
            "/command",
            methods=["POST"]
        )
        def command():

            cmd = request.json["command"]

            if self.navigation:
                self.navigation.stop_navigation()

            self.drive_command["value"] = cmd

            return jsonify({
                "ok": True,
                "command": cmd
            })


        # ---------------------------------------------------------
        # GPS
        # ---------------------------------------------------------

        @self.app.route("/gps")
        def gps():

            data = (
                self.gps_handler
                .get_current_position()
            )

            if data is None:

                return jsonify({
                    "latitude": None,
                    "longitude": None
                })


            return jsonify({
                "latitude": data.latitude,
                "longitude": data.longitude
            })


        # ---------------------------------------------------------
        # MAP POINTS
        # ---------------------------------------------------------

        @self.app.route(
            "/map_point",
            methods=["POST"]
        )
        def map_point():

            data = request.json

            point = MapPoint(
                data["latitude"],
                data["longitude"]
            )

            self.add_point(point)

            print(
                "NEW MAP POINT:",
                point.latitude,
                point.longitude
            )

            return jsonify({
                "ok": True
            })


        @self.app.route("/points")
        def points():

            return jsonify([
                p.__dict__
                for p in self.get_points()
            ])


        # ---------------------------------------------------------
        # DATABASE
        # ---------------------------------------------------------

        @self.app.route(
            "/db/save",
            methods=["POST"]
        )
        def db_save():

            data = request.json or {}

            ids = data.get("ids")

            if ids is None:
                ids = data.get(
                    "indexes",
                    []
                )

            self.save_points(ids)

            return jsonify({
                "ok": True
            })


        @self.app.route("/db/load")
        def db_load():

            self.load_points()

            return jsonify({
                "ok": True
            })


        @self.app.route(
            "/db/visited",
            methods=["POST"]
        )
        def db_visited():

            data = request.json or {}

            point_uid = data.get("id")
            visited = data.get("visited")

            if point_uid is None or visited is None:

                return jsonify({
                    "ok": False,
                    "error": "Missing id or visited"
                }), 400


            self.set_visited(
                point_uid,
                bool(visited)
            )


            return jsonify({
                "ok": True
            })


        @self.app.route(
            "/points/delete",
            methods=["POST"]
        )
        def delete_points():

            print("delete point: ")

            data = request.json or {}

            ids = data.get("ids")

            if ids is None:
                ids = data.get(
                    "indexes",
                    []
                )

            self.clear_points(ids)

            return jsonify({
                "ok": True
            })


        @self.app.route(
            "/points/clear",
            methods=["POST"]
        )
        def clear():

            data = request.json or {}

            ids = data.get("ids")

            if ids is None:
                ids = data.get(
                    "indexes",
                    []
                )

            self.clear_points(ids)

            return jsonify({
                "ok": True
            })


        # ---------------------------------------------------------
        # NAVIGATION
        # ---------------------------------------------------------

        @self.app.route(
            "/nav/start",
            methods=["POST"]
        )
        @self.app.route(
            "/nav/start",
            methods=["POST"]
        )
        def nav_start():

            direct_drive_enabled = (
                self.get_setting(
                    "direct_drive_enabled"
                ) == "1"
            )

            if direct_drive_enabled:

                if self.navigation:
                    self.navigation.stop_navigation()

                if self.navigation_direct_drive:
                    self.navigation_direct_drive.start_navigation()

            else:

                if self.navigation_direct_drive:
                    self.navigation_direct_drive.stop_navigation()

                if self.navigation:
                    self.navigation.start_navigation()

            return jsonify({
                "ok": True
            })


        @self.app.route(
            "/nav/stop",
            methods=["POST"]
        )
        def nav_stop():

            if self.navigation:
                self.navigation.stop_navigation()

            if self.navigation_direct_drive:
                self.navigation_direct_drive.stop_navigation()

            return jsonify({
                "ok": True
            })


        @self.app.route("/nav/status")
        def nav_status():

            direct_drive_enabled = (
                self.get_setting(
                    "direct_drive_enabled"
                ) == "1"
            )

            if direct_drive_enabled:

                if self.navigation_direct_drive is None:

                    return jsonify({
                        "state": "disabled",
                        "target": None,
                        "distance": None,
                        "current_position": None,
                        "command": self.drive_command["value"]
                    })

                return jsonify(
                    self.navigation_direct_drive.get_status()
                )


            if self.navigation is None:

                return jsonify({
                    "state": "disabled",
                    "target": None,
                    "distance": None,
                    "current_position": None,
                    "command": self.drive_command["value"]
                })


            return jsonify(
                self.navigation.get_status()
            )

        # ---------------------------------------------------------
        # COMMAND STATUS
        # ---------------------------------------------------------

        @self.app.route("/command/status")
        def command_status():

            return jsonify({
                "command":
                    self.drive_command["value"]
            })


    def run(self):

        log = logging.getLogger(
            "werkzeug"
        )

        if self.enable_flask_logs:

            log.setLevel(
                logging.INFO
            )

        else:

            log.setLevel(
                logging.ERROR
            )


        self.app.run(
            host="0.0.0.0",
            port=5000,
            debug=False,
            use_reloader=False
        )
