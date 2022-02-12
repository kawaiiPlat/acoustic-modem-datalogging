#import RPi.GPIO as GPIO
import asyncio as asyncio

##GPS imports
import time
import board
import digitalio
import busio
import serial
import adafruit_gps

async def main():
    bStates = asyncio.Queue()
    running = False
    button = asyncio.create_task(updateButton(bStates))

    while(True):
        await waitUntilButtonIs(False, bStates)
        running = True #start the next log

        if(running):
            print("starting a log")
            log_task = asyncio.create_task(log("temp.log"))
            while(running):
                    await waitUntilButtonIs(True, bStates)
                    running = False
            log_task.cancel()
            await log_task
            print("finished a log\n\n")

async def getGPSData(gpsData):
        # data is a asyncio Queue
        #GPS Serial port
        uart = serial.Serial("/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_023280BD-if00-port0", baudrate=9600, timeout=10)
        gps = adafruit_gps.GPS(uart, debug=False)
        gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        gps.send_command(b"PMTK220,1000")
        
        #Modem Serial port
        ser = serial.Serial('/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0',
        baudrate = 19200,
        parity = serial.PARITY_NONE, 
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS)

        last_print = time.monotonic()

        while(True):
            try:
                gps.update()
                current = time.monotonic()
                if not gps.has_fix:
                    # Try again if we don't have a fix yet.
                    print("Waiting for fix...")
                    continue
                gps_separator = "=" * 40  # Print a separator line.
                gps_time = "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                                        gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                                        gps.timestamp_utc.tm_mday,  # struct_time object that holds
                                        gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                                        gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                                        gps.timestamp_utc.tm_min,  # month!
                                        gps.timestamp_utc.tm_sec )
                gps_latitude = "Latitude: {0:.6f} degrees".format(gps.latitude)
                gps_longitude = "Longitude: {0:.6f} degrees".format(gps.longitude)

                if ser is not None:
                    ser.write(str.encode(str(gps_separator)))
                    ser.write(str.encode("\n"))
                    ser.write(str.encode(str(gps_time)))
                    ser.write(str.encode(","))
                    ser.write(str.encode(str(gps_latitude)))
                    ser.write(str.encode(","))
                    ser.write(str.encode(str(gps_longitude)))
                    ser.write(str.encode("\n"))

                to_log = {"latitude": gps.latitude, "longitude": gps.longitude, "time": gps_time}
                await gpsData.put(to_log)

            except KeyboardInterrupt:
                print("interrupt")
            except asyncio.CancelledError:
                ser.close()
                break
            except Exception as e:
                print(e)
                print("error")
                continue
            finally:
                await asyncio.sleep(0.5)

async def log(logFilePath):
    f = open(logFilePath, "a") #append to the log
    f.write("Starting Log")
    gpsData = asyncio.Queue()
    gps_task = asyncio.create_task(getGPSData(gpsData))
    try:
        while(True):
            await asyncio.sleep(0.5)
            #log out the gps data in the queue
            while not(gpsData.empty()):
                gpsDatum = await gpsData.get()
                #print(gpsDatum)
                f.write(str(gpsDatum))
                f.write("\n")
                gpsData.task_done()
                print("logged something")
    except asyncio.CancelledError:
        gps_task.cancel()
        print("Finishing Log")
        f.write("Finishing Log\n")
        #raise

async def waitUntilButtonIs(state, bStates):
    waiting = True
    while(waiting):
        await asyncio.sleep(0.1) #let the button reader slip in here
        bState = await bStates.get()
        if(bState == state):
           waiting = False
        bStates.task_done()
    # clear the rest of the inputs
    while not(bStates.empty()):
        bState = await bStates.get()
        bStates.task_done()


async def updateButton(bStates):
    logButton = digitalio.DigitalInOut(board.D2)
    prevState = False
    currState = logButton.value
    while(1):
        currState = logButton.value
        if(prevState != currState):
            prevState = currState
            await bStates.put(currState)
        await asyncio.sleep(0.1)


    
    
if __name__ == "__main__":
    asyncio.run(main())
