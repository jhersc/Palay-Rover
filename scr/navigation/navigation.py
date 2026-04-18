from pymavlink import mavutil


class Navigation():

    def __init__(self):
        self.master = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600)
        self.master.wait_heartbeat()
        print("Connected to Pixhawk")

    def get_direction(self):
        msg = self.master.recv_match(type='VFR_HUD', blocking=True)
        if msg:
            heading = msg.heading  # 0–360 degrees

            print(f"Heading: {heading}°")
            return heading
    
    @staticmethod
    def get_direction(deg):
        if deg < 22.5 or deg >= 337.5:
            return "N"
        elif deg < 67.5:
            return "NE"
        elif deg < 112.5:
            return "E"
        elif deg < 157.5:
            return "SE"
        elif deg < 202.5:
            return "S"
        elif deg < 247.5:
            return "SW"
        elif deg < 292.5:
            return "W"
        else:
            return "NW"

        
