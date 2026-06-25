# model/command_processor.py

import threading
import queue

class CommandProcessor:
    def __init__(self, drive, command_queue):
        self.drive = drive
        self.command_queue = command_queue

    def start(self):
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        print("Rover command thread started")
        while True:
            try:
                cmd = self.command_queue.get(timeout=0.1)
                print("CommandProcessor: ",cmd)
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
