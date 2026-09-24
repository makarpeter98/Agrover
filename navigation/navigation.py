# navigation/navigation.py

from navigation.navigation_math import NavigationMath

import threading
import time


class Navigation:

    def __init__(self, gps_handler, point_service, drive_command, heading, database):
        self.gps_handler = gps_handler
        self.point_service = point_service
        self.drive_command = drive_command
        self.heading = heading

        self._target_point = None
        self._active = False
        self._state = "idle"
        self._distance_to_target = None

        self.current_heading = 0
        self.target_heading = 0
        self.heading_difference = 0

        self.arrival_distance_limit = 1
        self.heading_tolerance = 20
        
        self.database = database

        self._stop_event = threading.Event()


    def _set_command(self, cmd):
        self.drive_command["value"] = cmd


    def start_navigation(self):
        if self._active:
            return

        self.arrival_distance_limit = float(
            self.database.get_setting(
                "arrival_distance_limit"
            )
        )

        self.heading_tolerance = float(
            self.database.get_setting(
                "heading_tolerance"
            )
        )
        
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
        
        nav_math = NavigationMath()
        
        while True:
            
            if self._active == False:
                state = "idle"
                self._set_command("STOP")
                break
            
            ##Atnezve, mukodik
            state = self._state
            
            gps_position = self.gps_handler.get_current_position()
            gps_target_position = self._target_point
            current_heading = self.current_heading = self.heading['value']
            
            target_distance = self._distance_to_target = nav_math.distance_m(
                gps_position.latitude,
                gps_position.longitude,
                gps_target_position.latitude,
                gps_target_position.longitude
            )
            
            target_heading = self.target_heading = nav_math.bearing(
                gps_position.latitude,
                gps_position.longitude,
                gps_target_position.latitude,
                gps_target_position.longitude
            )
            
            target_heading_difference = self.heading_difference  = nav_math.heading_difference(
                current_heading, 
                target_heading
            )
            
            heading_tolerance = self.heading_tolerance     
            arrival_distance_limit = self.arrival_distance_limit 
            
            print("+Navigation+")
            print(f"    Navigation process started")
            print(f"    [gps target position] lat:{gps_target_position.latitude} lon: {gps_target_position.longitude}")
            print(f"    [gps actual position] lat:{gps_position.latitude} lon: {gps_position.longitude}")
            print(f"    [current heading] {current_heading:.0f}")
            print(f"    [target  heading] {target_heading:.0f}")
            print(f"    [target  heading difference] {target_heading_difference:.0f}")
            print(f"    [heading tolerance] {heading_tolerance}")
            print(f"    [distance] {target_distance:.0f}m")
            print(f"    [arrival distance limit] {arrival_distance_limit:.0f}m")
            print(f"    [navigation state] {state}")

            self._turning_into_the_direction_of_the_target(target_heading_difference, heading_tolerance)
            
            if abs(target_heading_difference) <= heading_tolerance:
            
                if target_distance <= arrival_distance_limit:
                    self._arrived()
                else:
                    print("    [OPERATION] FORWARD")
                    self._set_command("FORWARD")
                
            print("-Navigation-")
            time.sleep(0.5)

    def _turning_into_the_direction_of_the_target(self, target_heading_difference, heading_tolerance):
        
        #print(f"[drive command] {self.drive_command}")
        if target_heading_difference > heading_tolerance and self.drive_command["value"] != "RIGHT":
            print("    +Turning+")
            print(f"        [OPERATION] RIGHT")
            self._set_command("RIGHT")
            print("    -Turning-")
        if target_heading_difference < -heading_tolerance and self.drive_command["value"] != "LEFT":
            print("    +Turning+")
            print(f"        [OPERATION] LEFT")
            self._set_command("LEFT")
            print("    -Turning-")
        if abs(target_heading_difference) <= heading_tolerance and self.drive_command["value"] != "STOP":
            print("    +Turning+")
            print(f"        [OPERATION] STOP")
            self._set_command("STOP")
            print("    -Turning-")
    
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
