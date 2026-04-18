from pymavlink import mavutil

master = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600)
# Wait for heartbeat
master.wait_heartbeat()
print("Connected to Pixhawk")


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

        


while True:
    msg = master.recv_match(type='VFR_HUD', blocking=True)
    if msg:
        heading = msg.heading  # 0–360 degrees

        # print(f"Heading: {heading}°")
        print(f"Heading: {heading}° ({get_direction(heading)})")



