#navigation/navigation_math.py

import math


class NavigationMath:


    @staticmethod
    def distance_m(lat1, lon1, lat2, lon2):

        R = 6371000

        p1 = math.radians(lat1)
        p2 = math.radians(lat2)

        dp = math.radians(lat2 - lat1)
        dl = math.radians(lon2 - lon1)

        a = (
            math.sin(dp / 2) ** 2
            +
            math.cos(p1)
            * math.cos(p2)
            * math.sin(dl / 2) ** 2
        )

        return R * 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )


    @staticmethod
    def bearing(lat1, lon1, lat2, lon2):

        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        dl = math.radians(lon2 - lon1)

        x = math.sin(dl) * math.cos(lat2)

        y = (
            math.cos(lat1) * math.sin(lat2)
            -
            math.sin(lat1)
            * math.cos(lat2)
            * math.cos(dl)
        )

        return (
            math.degrees(math.atan2(x, y))
            + 360
        ) % 360


    @staticmethod
    def normalize_angle(angle):

        return (angle + 180) % 360 - 180
