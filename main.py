#main.py

import threading
import time

from hardware.rover.rover_model import DriveModel
from navigation.navigation import Navigation
from navigation.point_service import PointService
from database.database import Database
from hardware.gps.gps_handler import GPSHandler
from hardware.gps.gps_data import GPSData
from hardware.compass.compass_handler import CompassHandler
from control.command_processor import CommandProcessor
from viewcontroller.web_ui_service import WebUIService


class RoverSystem:
    def __init__(self):

        # --- aktuális vezérlési parancs ---
        # egyszerre mindig csak egy lehet
        self.drive_command = {
            "value": "STOP"
        }


        # --- adatbázis + pontkezelés ---
        self.database = Database()

        self.point_service = PointService(
            self.database
        )


        # --- GPS ---
        self.gps_data = GPSData()

        self.gps_handler = GPSHandler()

        self.gps_thread = threading.Thread(
            target=self.gps_handler.run,
            args=(self.gps_data,),
            daemon=True
        )


        # --- iránytű ---
        self.heading = {
            "value": 0.0
        }

        self.compass_handler = CompassHandler(
            self.heading
        )

        self.compass_thread = threading.Thread(
            target=self.compass_handler.run,
            daemon=True
        )


        # --- motorvezérlés ---
        self.drive = DriveModel()


        # --- command processor ---
        self.command_processor = CommandProcessor(
            self.drive,
            self.drive_command
        )

        self.command_thread = threading.Thread(
            target=self.command_processor.run,
            daemon=True
        )


        # --- navigáció ---
        self.navigation = Navigation(
            self.gps_handler,
            self.point_service,
            self.drive_command,
            self.heading
        )


        # --- Web UI ---
        self.web_ui_service = WebUIService(
            self.drive_command,
            self.gps_handler,
            self.point_service,
            self.navigation
        )


        # --- debug ---
        self.debug_thread = threading.Thread(
            target=self.debug_loop,
            daemon=True
        )


    def debug_loop(self):

        print("Debug thread started!")

        while True:

            print("----------------------------")
            print(
                "Command:",
                self.drive_command["value"]
            )

            print(
                "Heading:",
                self.heading["value"]
            )

            print(
                "GPS latitude:",
                self.gps_data.latitude
            )

            print(
                "GPS longitude:",
                self.gps_data.longitude
            )

            print("----------------------------")

            time.sleep(2)



    def start(self):

        print("Starting GPS thread...")
        self.gps_thread.start()


        print("Starting Compass thread...")
        self.compass_thread.start()


        print("Starting command processor...")
        self.command_thread.start()


        print("Starting debug thread...")
        self.debug_thread.start()


        print("Starting Web UI...")
        self.web_ui_service.start()


        print("RoverSystem started. Running forever.")


        while True:
            time.sleep(1)



if __name__ == "__main__":
    RoverSystem().start()
