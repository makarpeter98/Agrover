# navigation/navigation_math.py

import math

class NavigationMath:

    EARTH_RADIUS_M = 6_371_000

    def distance_m(self, lat1, lon1, lat2, lon2):

        R = 6_371_000

        p1 = math.radians(lat1)
        p2 = math.radians(lat2)

        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)

        a = (
            math.sin(d_lat / 2) ** 2
            + math.cos(p1)
            * math.cos(p2)
            * math.sin(d_lon / 2) ** 2
        )

        return R * 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

    def bearing(self, lat1, lon1, lat2, lon2):

        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        d_lon = math.radians(lon2 - lon1)

        x = math.sin(d_lon) * math.cos(lat2)

        y = (
            math.cos(lat1) * math.sin(lat2)
            - math.sin(lat1)
            * math.cos(lat2)
            * math.cos(d_lon)
        )

        return (
            math.degrees(math.atan2(x, y)) + 360
        ) % 360

    def heading_difference(self, actual_heading, target_heading):
        return (target_heading - actual_heading + 180) % 360 - 180
