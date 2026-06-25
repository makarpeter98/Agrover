from gpiozero import OutputDevice
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory

Device.pin_factory = LGPIOFactory()


class MotorDriver:
    def __init__(self):
        self.LF = OutputDevice(20)
        self.LB = OutputDevice(26)
        self.RF = OutputDevice(16)
        self.RB = OutputDevice(19)

    def stop_all(self):
        self.LF.off()
        self.LB.off()
        self.RF.off()
        self.RB.off()


class DriveModel:
    def __init__(self):
        self.hw = MotorDriver()

    def forward(self):
        print("rover_model: foward")
        self.hw.LF.on(); self.hw.LB.off()
        self.hw.RF.on(); self.hw.RB.off()

    def backward(self):
        print("rover_model: backward")
        self.hw.LF.off(); self.hw.LB.on()
        self.hw.RF.off(); self.hw.RB.on()

    def left(self):
        print("rover_model: left")
        self.hw.LF.off(); self.hw.LB.on()
        self.hw.RF.on(); self.hw.RB.off()

    def right(self):
        print("rover_model: right")
        self.hw.LF.on(); self.hw.LB.off()
        self.hw.RF.off(); self.hw.RB.on()

    def stop(self):
        print("rover_model: stop")
        self.hw.stop_all()
