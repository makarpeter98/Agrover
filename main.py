# main.py

import queue
import threading
import time

from model.rover_model import DriveModel
from model.navigation import Navigation
from model.point_service import PointService
from model.database import Database
from model.gps_handler import GPSHandler
from model.command_processor import CommandProcessor
from viewcontroller.web_ui_service import WebUIService
from model.gps_data import GPSData


class RoverSystem:
    def __init__(self):
        # --- közös adatréteg ---
        self.command_queue = queue.Queue()

        # --- adatbázis + pontkezelés ---
        self.database = Database()
        self.point_service = PointService(self.database)

        # --- GPS ---
        self.gps_data = GPSData()
        self.gps_handler = GPSHandler()

        self.gps_thread = threading.Thread(
            target=self.gps_handler.run,
            args=(self.gps_data,),   # <-- EZ A LÉNYEG
            daemon=True
        )


        # --- motorvezérlés ---
        self.drive = DriveModel()

        # --- command processor ---
        self.command_processor = CommandProcessor(
            self.drive,
            self.command_queue
        )
        self.command_thread = threading.Thread(
            target=self.command_processor.run,
            daemon=True
        )

        # --- navigáció ---
        self.navigation = Navigation(
            self.gps_handler,
            self.point_service,
            self.drive
        )

        # --- WebUI ---
        self.web_ui_service = WebUIService(
            self.command_queue,
            self.gps_handler,
            self.point_service,
            self.navigation
        )

    def start(self):
        print("Starting GPS thread...")
        self.gps_thread.start()

        print("Starting command processor...")
        self.command_thread.start()

        print("Starting Web UI...")
        self.web_ui_service.start()

        print("RoverSystem started. Running forever.")
        while True:
            time.sleep(1)


if __name__ == "__main__":
    RoverSystem().start()
