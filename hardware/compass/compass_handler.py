#hardware/compass/compass_handler.py

import time
import math

import board
import busio
import adafruit_qmc5883p


class CompassHandler:

    def __init__(self, heading):
        self.heading = heading

        # --- I2C inicializálás ---
        self.i2c = busio.I2C(
            board.SCL,
            board.SDA
        )

        # --- Compass inicializálás ---
        self.sensor = adafruit_qmc5883p.QMC5883P(
            self.i2c
        )

        # --- Konfiguráció ---
        self.sensor.mode = adafruit_qmc5883p.MODE_CONTINUOUS
        self.sensor.data_rate = adafruit_qmc5883p.ODR_50HZ
        self.sensor.range = adafruit_qmc5883p.RANGE_8G


    def run(self):
        print("Compass handler started!")

        while True:
            try:
                mag_x, mag_y, mag_z = self.sensor.magnetic

                # Irány számítása
                heading = round(
					math.atan2(
						mag_y,
						mag_x
					) * (180 / math.pi)
				)

                # 0-360 fok közé normalizálás
                if heading < 0:
                    heading += 360

                # Közös adat frissítése
                self.heading["value"] = heading

            except Exception as e:
                print("Compass error:", e)

            # 50Hz helyett nem kell ennyire sűrűn,
            # a rover navigációhoz bőven elég
            time.sleep(1)
