# control/command_porcessor.py

import time

class CommandProcessor:

    def __init__(self, drive, drive_command):
        self.drive = drive
        self.drive_command = drive_command

        self.last_command = None


    def run(self):

        print("Command processor started!")

        while True:

            command = self.drive_command["value"].upper()

            # csak változás esetén dolgozunk
            if command != self.last_command:

                print("New command:", command)

                self.execute(command)

                self.last_command = command

            time.sleep(0.05)


    def execute(self, command):

        if command == "FORWARD":
            self.drive.forward()


        elif command == "BACKWARD":
            self.drive.backward()


        elif command == "LEFT":
            self.drive.left()


        elif command == "RIGHT":
            self.drive.right()


        elif command == "STOP":
            self.drive.stop()


        else:
            print("Unknown command:", command)
            self.drive.stop()
