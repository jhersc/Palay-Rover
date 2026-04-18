import serial
import pynmea2

port = "/dev/serial0"
baud = 9600

try:
    ser = serial.Serial(port, baudrate=baud, timeout=1)
    print(f"Connected to {port} at {baud} baud.")
    print("Waiting for GPS data...")

    while True:
        line = ser.readline().decode('ascii', errors='replace').strip()

        if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
            try:
                msg = pynmea2.parse(line)

                if hasattr(msg, "latitude") and hasattr(msg, "longitude"):
                    if msg.latitude and msg.longitude:
                        print(f"Lat: {msg.latitude:.6f} | Lon: {msg.longitude:.6f}")
                    else:
                        print("No GPS fix yet")

            except pynmea2.ParseError:
                pass

        elif line.startswith('$'):
            print(f"NMEA: {line}")

except serial.SerialException as e:
    print(f"Serial error: {e}")

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()