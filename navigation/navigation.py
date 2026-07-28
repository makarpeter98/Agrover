# navigation/navigation.py

from navigation.navigation_math import NavigationMath
from navigation.navigation_controller import NavigationController

import threading
import time


class Navigation:

    def __init__(self, gps_handler, point_service, drive_command, heading):
        self.gps_handler = gps_handler
        self.point_service = point_service
        self.drive_command = drive_command
        self.heading = heading

        self.controller = NavigationController()

        self._target_point = None
        self._active = False
        self._state = "idle"
        self._distance_to_target = None

        self.current_heading = 0
        self.target_heading = 0
        self.heading_difference = 0

        self.arrival_threshold = 3

        self._stop_event = threading.Event()


    def _set_command(self, cmd):
        self.drive_command["value"] = cmd


    def start_navigation(self):
        if self._active:
            return

        target = self.point_service.get_next_unvisited_point()

        if not target:
            self._state = "no_target"
            self._set_command("STOP")
            return

        self._target_point = target
        self._active = True
        self._state = "navigating"

        threading.Thread(
            target=self._run_loop,
            daemon=True
        ).start()


    def stop_navigation(self):
        self._active = False
        self._set_command("STOP")
        self._state = "idle"


    def _run_loop(self):

        print("Navigation started")

        while self._active:

            pos = self.gps_handler.get_current_position()

            if not pos:
                self._set_command("STOP")
                time.sleep(1)
                continue


            self._distance_to_target = NavigationMath.distance_m(
                pos.latitude,
                pos.longitude,
                self._target_point.latitude,
                self._target_point.longitude
            )


            if self._distance_to_target <= self.arrival_threshold:
                self._arrived()
                return


            self.current_heading = self.heading["value"]

            self.target_heading = NavigationMath.bearing(
                pos.latitude,
                pos.longitude,
                self._target_point.latitude,
                self._target_point.longitude
            )

            self.heading_difference = NavigationMath.normalize_angle(
                self.target_heading - self.current_heading
            )


            command = self.controller.calculate_command(
                self.heading_difference
            )

            self._set_command(command)

            self._debug(command)

            time.sleep(1)


        self._set_command("STOP")


    def _arrived(self):

        print("Target reached")

        self._set_command("STOP")
        self._target_point.visited = True
        self._state = "arrived"

        next_point = self.point_service.get_next_unvisited_point()

        if next_point:
            self._target_point = next_point
            self._state = "navigating"
            return

        self._state = "done"
        self._active = False


    def _debug(self, command):
        print(
            f"[NAV] "
            f"Dist:{self._distance_to_target:.1f}m | "
            f"Head:{self.current_heading:.0f}° | "
            f"Target:{self.target_heading:.0f}° | "
            f"Diff:{self.heading_difference:.0f}° | "
            f"CMD:{command}"
        )


    def get_status(self):

        pos = self.gps_handler.get_current_position()

        return {
            "state": self._state,

            "target": None if not self._target_point else {
                "latitude": self._target_point.latitude,
                "longitude": self._target_point.longitude,
                "visited": getattr(
                    self._target_point,
                    "visited",
                    None
                )
            },

            "distance": self._distance_to_target,

            "current_position": None if not pos else {
                "latitude": pos.latitude,
                "longitude": pos.longitude
            },

            "command": self.drive_command["value"],

            "heading": {
                "current": round(self.current_heading, 1),
                "target": round(self.target_heading, 1),
                "difference": round(self.heading_difference, 1)
            }
        }
