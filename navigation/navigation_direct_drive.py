# navigation/navigation_direct_drive.py
import threading
import time


class NavigationDirectDrive:

    SCRIPT = [
        ("FORWARD", 5),
        ("RIGHT", 5),
        ("BACKWARD", 5),
    ]


    def __init__(
        self,
        gps_handler,
        point_service,
        drive_command,
        heading,
        database
    ):
        self.gps_handler = gps_handler
        self.point_service = point_service
        self.drive_command = drive_command
        self.heading = heading
        self.database = database

        self._active = False
        self._state = "idle"

        self._step_index = 0
        self._step_elapsed = 0.0

        self._stop_event = threading.Event()


    def _set_command(self, command):
        self.drive_command["value"] = command


    def start_navigation(self):
        
        print("Direct drive running!")
        
        if self._active:
            return
        
        if self._state == "done":
            self._step_index = 0
            self._step_elapsed = 0.0

        if self._step_index >= len(self.SCRIPT):
            self._state = "done"
            self._set_command("STOP")
            return

        self._active = True
        self._state = "running"

        self._stop_event.clear()


        threading.Thread(
            target=self._run_loop,
            daemon=True
        ).start()


    def stop_navigation(self):

        self._active = False
        self._stop_event.set()

        self._set_command("STOP")

        self._state = "idle"


    def _run_loop(self):

        print("Direct Drive started")

        while self._active:

            if self._step_index >= len(self.SCRIPT):
                self._active = False
                self._state = "done"
                self._set_command("STOP")
                break

            command, duration = self.SCRIPT[
                self._step_index
            ]

            remaining = (
                duration -
                self._step_elapsed
            )

            if remaining <= 0:
                self._step_index += 1
                self._step_elapsed = 0.0
                continue

            self._set_command(command)

            print(
                f"[DIRECT DRIVE] "
                f"step={self._step_index + 1}/"
                f"{len(self.SCRIPT)} "
                f"command={command} "
                f"remaining={remaining:.1f}s"
            )

            start_time = time.monotonic()

            while (
                self._active
                and self._step_elapsed < duration
            ):

                time.sleep(0.1)

                elapsed = (
                    time.monotonic() -
                    start_time
                )

                self._step_elapsed += elapsed

                start_time = time.monotonic()

            if not self._active:
                break

            self._step_index += 1
            self._step_elapsed = 0.0

        self._set_command("STOP")

        if self._step_index >= len(self.SCRIPT):
            self._state = "done"
            self._active = False

        print("Direct Drive stopped")


    def get_status(self):

        return {
            "state": self._state,

            "target": None,

            "distance": None,

            "current_position": None,

            "command": self.drive_command["value"],

            "heading": {
                "current": 0,
                "target": 0,
                "difference": 0
            }
        }
