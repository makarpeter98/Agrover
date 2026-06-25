# main.py

import threading
import time
import queue

from model.gps_handler import GPSHandler
from model.gps_data import GPSData
from model.rover_model import DriveModel
from model.database import Database

from viewcontroller.web_ui import WebUI


class RoverSystem:
    def __init__(self):
        self.command_queue = queue.Queue()
        self.points = []
        self.gps_data = GPSData()
        self.gps_handler = GPSHandler()
        self.drive = DriveModel()
        self.database = Database()

    def start(self):
        threading.Thread(
            target=self.gps_thread,
            daemon=True
        ).start()

        threading.Thread(
            target=self.rover_thread,
            daemon=True
        ).start()

        threading.Thread(
            target=self.web_thread,
            daemon=True
        ).start()

        print("Rover system running")

        while True:
            time.sleep(1)

    def gps_thread(self):
        print("GPS thread started")
        self.gps_handler.run(self.gps_data)

    def rover_thread(self):
        while True:
            try:
                cmd = self.command_queue.get(timeout=0.1)

                if cmd == "forward":
                    self.drive.forward()
                elif cmd == "backward":
                    self.drive.backward()
                elif cmd == "left":
                    self.drive.left()
                elif cmd == "right":
                    self.drive.right()
                elif cmd == "stop":
                    self.drive.stop()

            except queue.Empty:
                pass
    
    def normalize_sequences(self):

        # rendezés sequence szerint
        self.points.sort(key=lambda p: p.sequence)

        # újraszámozás 1-től
        for i, p in enumerate(self.points, start=1):
            p.sequence = i

    
    def add_point(self, point):

        # új pont hozzáadása
        self.points.append(point)

        # sorrend újraszámolása
        self.normalize_sequences()

        print(
            "NEW POINT",
            point.latitude,
            point.longitude,
            point.sequence
        )


    def save_points(self, uids):
        selected = [
            p for p in self.points
            if p.uid in uids
        ]

        self.database.save_points(selected)

    def load_points(self):

        loaded = self.database.load_points()

        existing = {p.id: p for p in self.points if p.id is not None}

        for p in loaded:
            if p.id in existing:
                old = existing[p.id]
                old.latitude = p.latitude
                old.longitude = p.longitude
                old.time = p.time
                old.visited = p.visited
                old.sequence = p.sequence
                old.in_database = True
            else:
                self.points.append(p)

        # DB betöltés után újraszámozás
        self.normalize_sequences()


    def delete_points(self, uids):
        sql_delete = []
        new_list = []

        for p in self.points:
            if p.uid in uids:
                if p.id is not None:
                    sql_delete.append(p.id)
            else:
                new_list.append(p)

        if sql_delete:
            self.database.delete_points(sql_delete)

        self.points = new_list

        # törlés után újraszámozás
        self.normalize_sequences()

    def web_thread(self):

        ui = WebUI(
            self.command_queue,
            self.gps_handler,
            self.add_point,
            lambda: self.points,
            self.save_points,
            self.load_points,
            self.delete_points
        )

        ui.run()

if __name__ == "__main__":
    RoverSystem().start()
