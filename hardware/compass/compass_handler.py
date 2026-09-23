import time
import math

import board
import busio
import adafruit_qmc5883p


# Compass kalibráció
OFFSET_X = 0.274
OFFSET_Y = 0.030

# A szenzor fizikai orientációja miatt szükséges korrekció
HEADING_OFFSET = 180.0


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

                # Kalibrációs offsetek eltávolítása
                calibrated_x = mag_x - OFFSET_X
                calibrated_y = mag_y - OFFSET_Y

                # Heading számítása
                heading = math.degrees(
                    math.atan2(
                        calibrated_y,
                        calibrated_x
                    )
                )

                # Szenzor fizikai orientációjának korrigálása
                heading -= HEADING_OFFSET

                # Normalizálás 0-360 fok közé
                heading %= 360

                print(
                    f"| compass_handler-> Compass heading: {heading:6.1f}°"
                )

                self.heading["value"] = round(
                    heading
                )

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
