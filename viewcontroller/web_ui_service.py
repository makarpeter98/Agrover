# viewcontroller/web_ui_service.py

import threading
from viewcontroller.web_ui import WebUI
import logging


class WebUIService:
    def __init__(self, command_queue, gps_handler, point_service, navigation):
        self.command_queue = command_queue
        self.gps_handler = gps_handler
        self.point_service = point_service
        self.navigation = navigation

    def start(self):
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        ui = WebUI(
            self.command_queue,
            self.gps_handler,
            self.point_service.add_point,
            lambda: self.point_service.points,
            self.point_service.save_points,
            self.point_service.load_points,
            self.point_service.delete_points,
            self.navigation,
            True
        )
        ui.run()
