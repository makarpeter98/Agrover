# model/navigation.py

import threading
import time
import math


class Navigation:
    def __init__(self, gps_handler, point_service, drive):
        self.gps_handler = gps_handler
        self.point_service = point_service
        self.drive = drive

        self._active = False
        self._state = "idle"
        self._target_point = None
        self._distance_to_target = None

        self._thread = None
        self._stop_event = threading.Event()

        # érkezési küszöb
        self.arrival_threshold = 1.3

        # GPS zaj kezelés
        self.prev_distances = []

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------

    def start_navigation(self):
        if self._active:
            return

        target = self.point_service.get_next_unvisited_point()
        if target is None:
            self._state = "no_target"
            return

        self._target_point = target
        self._active = True
        self._state = "navigating"
        self._stop_event.clear()

        self.prev_distances = []

        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop_navigation(self):
        self._active = False
        self._stop_event.set()
        self.drive.stop()
        self._state = "idle"

    def get_status(self):
        pos = self.gps_handler.get_current_position()

        current_pos = None
        if pos:
            current_pos = {"latitude": pos.latitude, "longitude": pos.longitude}

        target = None
        if self._target_point:
            target = {
                "latitude": self._target_point.latitude,
                "longitude": self._target_point.longitude,
                "sequence": getattr(self._target_point, "sequence", None),
                "visited": getattr(self._target_point, "visited", None),
            }

        return {
            "state": self._state,
            "target": target,
            "distance": self._distance_to_target,
            "current_position": current_pos
        }

    # ---------------------------------------------------------
    # MAIN LOOP
    # ---------------------------------------------------------

    def _run_loop(self):
        while not self._stop_event.is_set():
            pos = self.gps_handler.get_current_position()

            if pos is None or self._target_point is None:
                time.sleep(1)
                continue

            # távolság számítás
            dist = self._compute_distance_m(
                pos.latitude,
                pos.longitude,
                self._target_point.latitude,
                self._target_point.longitude
            )
            self._distance_to_target = dist

            # érkezés
            if dist <= self.arrival_threshold:
                self.drive.stop()
                self._target_point.visited = True
                self._state = "arrived"
                self._active = False

                # következő pont
                next_point = self.point_service.get_next_unvisited_point()
                if next_point:
                    self._target_point = next_point
                    self._active = True
                    self._state = "navigating"
                    self.prev_distances = []
                    continue
                else:
                    self._state = "done"
                    return

            # GPS zaj kezelés – ha 3 egymás utáni mérés nő → rossz irány
            self.prev_distances.append(dist)
            if len(self.prev_distances) > 3:
                self.prev_distances.pop(0)

                if (
                    self.prev_distances[1] < self.prev_distances[0] and
                    self.prev_distances[2] < self.prev_distances[1]
                ):
                    # még közeledik → ok
                    pass
                else:
                    # távolodik → állj meg
                    self.drive.stop()
                    self._state = "distance_increasing"
                    self._active = False
                    return

            # nincs iránytű → mindig előre
            self.drive.forward()

            time.sleep(1)

        self.drive.stop()

    # ---------------------------------------------------------
    # MATH
    # ---------------------------------------------------------

    @staticmethod
    def _compute_distance_m(lat1, lon1, lat2, lon2):
        R = 6371000.0
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = (
            math.sin(dphi / 2.0) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
        )
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return R * c
