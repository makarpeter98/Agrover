# model/gps_service.py

import threading

class GPSService:
    def __init__(self, gps_handler, gps_data):
        self.gps_handler = gps_handler
        self.gps_data = gps_data

    def start(self):
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        print("GPS thread started")
        self.gps_handler.run(self.gps_data)
