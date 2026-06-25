# model/map_point.py

from datetime import datetime
import uuid


class MapPoint:
    def __init__(
        self,
        latitude,
        longitude,
        point_id=None,
        point_time=None
    ):
        self.id = point_id
        self.uid = str(uuid.uuid4())

        self.latitude = float(latitude)
        self.longitude = float(longitude)

        self.visited = False

        if point_time:
            self.time = point_time
        else:
            self.time = datetime.now().strftime(
                "%Y_%m_%d_%H_%M_%S"
            )

        self.sequence = 0
        self.in_database = (point_id is not None)
