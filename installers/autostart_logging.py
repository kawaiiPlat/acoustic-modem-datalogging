import RPi.GPIO as GPIO
import asyncio as asyncio

async def main():
    # read the button state for checkbutton    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3,GPIO.IN, pull_up_down=GPIO.PUD_UP) # the logging button
    
    bStates = asyncio.Queue()

    running = False
    button = asyncio.create_task(updateButton(bStates))

    while(True):
        await waitUntilButtonIs(GPIO.HIGH, bStates)
        running = True #start the next log

        if(running):
            print("starting a log")
            log_task = asyncio.create_task(log("filename"))
            while(running):
                    await waitUntilButtonIs(GPIO.LOW, bStates)
                    running = False
            log_task.cancel()
            await log_task
            print("finished a log\n\n")

                
async def log(logfile):
    try:
        while(True):
            await asyncio.sleep(1)
            print("logged something")
    except asyncio.CancelledError:
        print("Finishing Log")
        # save file?
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
    prevState = GPIO.LOW
    currState = GPIO.input(3)
    while(1):
        currState = GPIO.input(3)
        if(prevState != currState):
            prevState = currState
            await bStates.put(currState)
        await asyncio.sleep(0.1)


    
    
if __name__ == "__main__":
    asyncio.run(main())
