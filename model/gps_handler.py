from gps3 import gps3
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import copy


def safe_float(value, default=float("inf")):

    try:
        return float(value)

    except (TypeError, ValueError):
        return default



class GPSHandler:


    def __init__(self):

        self.gps_list = []

        self.current_data = None


        self.normal_measure_time = 0.5
        self.long_measure_time = 5



    def gps_data_ms_to_km(self, gps_data):

        try:

            gps_data.speed = float(gps_data.speed) * 3.6

            gps_data.speed = round(
                gps_data.speed,
                3
            )

        except:

            gps_data.speed = None




    def gps_data_time_to_bp(self, gps_data):

        gps_time_str = gps_data.time


        if gps_time_str and gps_time_str != "n/a":

            try:

                gps_time = datetime.fromisoformat(
                    gps_time_str.replace(
                        "Z",
                        "+00:00"
                    )
                )


                gps_time = gps_time.astimezone(
                    ZoneInfo("Europe/Budapest")
                )


                gps_data.time = gps_time.isoformat(
                    timespec="seconds"
                )


            except:

                gps_data.time = None

        else:

            gps_data.time = None





    def get_current_position(self):

        return self.current_data





    def run(self, gps_data):


        gps_socket = gps3.GPSDSocket()

        data_stream = gps3.DataStream()



        gps_socket.connect(
            host="127.0.0.1",
            port=2947
        )


        gps_socket.watch(
            enable=True,
            gpsd_protocol="json"
        )



        last_measure = 0



        while True:


            for new_data in gps_socket:


                if not new_data:
                    continue



                data_stream.unpack(
                    new_data
                )


                tpv = data_stream.TPV



                lat = tpv.get("lat")
                lon = tpv.get("lon")

                speed = tpv.get("speed")

                gps_time = tpv.get("time")

                mode = tpv.get(
                    "mode",
                    0
                )



                error_lat = safe_float(
                    tpv.get("epy")
                )

                error_lon = safe_float(
                    tpv.get("epx")
                )



                if time.time() - last_measure >= self.normal_measure_time:


                    last_measure = time.time()



                    gps_data.latitude = lat

                    gps_data.longitude = lon

                    gps_data.latitude_error = error_lat

                    gps_data.longitude_error = error_lon


                    gps_data.speed = speed

                    gps_data.time = gps_time


                    gps_data.mode = (
                        f"fix:"
                        f"{'3D' if mode == 3 else '2D' if mode == 2 else 'no'}"
                    )



                    self.gps_data_ms_to_km(
                        gps_data
                    )


                    self.gps_data_time_to_bp(
                        gps_data
                    )



                    gps_data.measure_fixed = False



                    self.current_data = copy.deepcopy(
                        gps_data
                    )



                    self.gps_list.append(
                        copy.deepcopy(
                            gps_data
                        )
                    )



            time.sleep(0.01)
