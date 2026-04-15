import os

class DualMotorController:
    def __init__(self,
                 left_pwm=17, left_dir=27,
                 right_pwm=18, right_dir=22,
                 frequency=100):

        # Detect Raspberry Pi automatically
        self.simulation = not os.path.exists("/proc/device-tree/model")

        if self.simulation:
            print("🧪 SIMULATION MODE (Ubuntu - no GPIO)")
            return

        from gpiozero import PWMOutputDevice, DigitalOutputDevice

        # LEFT MOTOR
        self.left_pwm = PWMOutputDevice(left_pwm, frequency=frequency)
        self.left_dir = DigitalOutputDevice(left_dir)

        # RIGHT MOTOR
        self.right_pwm = PWMOutputDevice(right_pwm, frequency=frequency)
        self.right_dir = DigitalOutputDevice(right_dir)

    # ------------------------
    # LOW LEVEL CONTROL
    # ------------------------

    def set_left(self, speed, direction=0):
        if self.simulation:
            print(f"[SIM] Left -> speed:{speed}, dir:{direction}")
            return
        self.left_dir.value = direction
        self.left_pwm.value = speed

    def set_right(self, speed, direction=0):
        if self.simulation:
            print(f"[SIM] Right -> speed:{speed}, dir:{direction}")
            return
        self.right_dir.value = direction
        self.right_pwm.value = speed

    # ------------------------
    # HIGH LEVEL CONTROL
    # ------------------------

    def forward(self, speed=0.3):
        self.set_left(speed, 0)
        self.set_right(speed, 0)

    def stop(self):
        self.set_left(0)
        self.set_right(0)

    def backward(self, speed=0.3):
        self.set_left(speed, 1)
        self.set_right(speed, 1)

    def turn_left(self, speed=0.3):
        self.set_left(0)
        self.set_right(speed, 0)

    def turn_right(self, speed=0.3):
        self.set_left(speed, 0)
        self.set_right(0)