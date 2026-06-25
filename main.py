# main.py

import time
import queue

from model.gps_handler import GPSHandler
from model.gps_data import GPSData
from model.rover_model import DriveModel
from model.database import Database

from model.gps_service import GPSService
from model.command_processor import CommandProcessor
from model.point_service import PointService
from viewcontroller.web_ui_service import WebUIService


class RoverSystem:
    def __init__(self):
        self.command_queue = queue.Queue()

        # Hardver
        self.gps_data = GPSData()
        self.gps_handler = GPSHandler()
        self.drive = DriveModel()

        # DB + pontok
        self.database = Database()
        self.point_service = PointService(self.database)

        # Szolgáltatások
        self.gps_service = GPSService(self.gps_handler, self.gps_data)
        self.command_processor = CommandProcessor(self.drive, self.command_queue)
        self.web_ui_service = WebUIService(
            self.command_queue,
            self.gps_handler,
            self.point_service
        )

    def start(self):
        self.gps_service.start()
        self.command_processor.start()
        self.web_ui_service.start()

        print("Rover system running")

        while True:
            time.sleep(1)


if __name__ == "__main__":
    RoverSystem().start()
