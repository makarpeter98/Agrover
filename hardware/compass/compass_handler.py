# hardware/compass/compass_handler.py

import time
import math

import board
import busio
import adafruit_qmc5883p


class CompassHandler:

    def __init__(self, heading):
        self.heading = heading

    def run(self):

        while True:

            i2c = None

            try:

                time.sleep(0.2)

                i2c = busio.I2C(
                    board.SCL,
                    board.SDA
                )

                while not i2c.try_lock():
                    time.sleep(0.01)

                try:

                    devices = i2c.scan()

                finally:

                    i2c.unlock()

                print(
                    "I2C devices:",
                    [hex(device) for device in devices]
                )

                if 0x2c not in devices:

                    print(
                        "QMC5883P NOT FOUND at 0x2c"
                    )

                    time.sleep(2)
                    continue

                print(
                    "QMC5883P found at 0x2c"
                )

                sensor = adafruit_qmc5883p.QMC5883P(
                    i2c,
                    address=0x2c
                )

                sensor.mode = (
                    adafruit_qmc5883p.MODE_CONTINUOUS
                )

                sensor.data_rate = (
                    adafruit_qmc5883p.ODR_50HZ
                )

                sensor.range = (
                    adafruit_qmc5883p.RANGE_8G
                )

                mag_x, mag_y, mag_z = sensor.magnetic

                heading = math.degrees(
                    math.atan2(
                        mag_y,
                        mag_x
                    )
                )
                
                heading = heading - 180
                heading = heading % 360

                print(
                    f"Heading: {heading:6.1f}°"
                )

                self.heading["value"] = round(
                    heading
                )

                time.sleep(1)

            except Exception as e:

                print(
                    "I2C/Compass error:",
                    repr(e)
                )

            finally:

                if i2c is not None:

                    try:

                        i2c.deinit()

                    except Exception:
                        pass

            time.sleep(1)
