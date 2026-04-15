from gpiozero import PWMOutputDevice, DigitalOutputDevice

class DualMotorController:
    def __init__(self,
                 left_pwm=17, left_dir=27,
                 right_pwm=18, right_dir=22,
                 frequency=100):

        # LEFT MOTOR
        self.left_pwm = PWMOutputDevice(left_pwm, frequency=frequency)
        self.left_dir = DigitalOutputDevice(left_dir)

        # RIGHT MOTOR
        self.right_pwm = PWMOutputDevice(right_pwm, frequency=frequency)
        self.right_dir = DigitalOutputDevice(right_dir)

    # --- LOW LEVEL CONTROL ---
    def set_left(self, speed):
        self.left_dir.value = 0
        self.left_pwm.value = speed

    def set_right(self, speed):
        self.right_dir.value = 0
        self.right_pwm.value = speed

    # --- HIGH LEVEL CONTROL ---
    def forward(self, speed=0.2):
        self.set_left(speed)
        self.set_right(speed)

    def stop(self):
        self.set_left(0)
        self.set_right(0)

    def turn_left(self, speed=0.2):
        self.set_left(0)
        self.set_right(speed)

    def turn_right(self, speed=0.2):
        self.set_left(speed)
        self.set_right(0)

    def backward(self, speed=0.2):
        # reverse depends on your driver wiring
        self.left_dir.value = 1
        self.right_dir.value = 1
        self.set_left(speed)
        self.set_right(speed)