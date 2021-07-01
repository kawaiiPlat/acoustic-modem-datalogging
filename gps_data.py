#! /usr/bin/env python
import serial 
import time 
from datetime import datetime

import board
import busio

import adafruit_gps


def main(args):
        location = 'data'
        filename = 'sender.csv'
        filename = location + '/' + filename
        ser = serial.Serial('/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0',
        baudrate = 19200,
        parity = serial.PARITY_NONE, 
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS)

        uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
        gps = adafruit_gps.GPS(uart, debug=False)
        gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        gps.send_command(b"PMTK220,1000")
        last_print = time.monotonic()

  #time.sleep(5*60)
        while(True):
            try:
                gps.update()
                current = time.monotonic()
                gps_separator = "=" * 40  # Print a separator line.
                gps_latitude = "Latitude: {0:.6f} degrees".format(gps.latitude)
                gps_longitude = "Longitude: {0:.6f} degrees".format(gps.longitude)
                if gps.speed_knots is not None:
                    gps_speed = "Speed: {} knots".format(gps.speed_knots)

                ser.write(str.encode(str(gps_separator)))
                ser.write(str.encode("\n"))

                ser.write(str.encode(str(gps_latitude)))
                ser.write(str.encode("\n"))

                ser.write(str.encode(str(gps_longitude)))
                ser.write(str.encode("\n"))

                ser.write(str.encode(str(gps_speed)))
                ser.write(str.encode("\n"))

                time.sleep(1)

            except KeyboardInterrupt:
                print("Exiting program now")
            except:
                continue
            finally:
                ser.close()
                pass
            return 0

if __name__ == '__main__':
        import sys
        sys.exit(main(sys.argv))
