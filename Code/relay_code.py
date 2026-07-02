# This is a script to control a relay using a raspberry pi 400 GPIO pins
import RPi.GPIO as GPIO
import time

CHANNEL = 1
CHANNEL_PINS = {1: [4, 15], 2: [17, 22], 3: [24, 10], 4: [25, 11]} # put GPIO pins or smth here maybe?? something to help with switching

# connections:
# connect COM on all positive modules to positive terminal of PROVA
# connect NO on all positive module                          s to negative (right side usually) terminal of respective terminal
# GPIO - INPUT: 4-1, 15-2, 17-3, 22-4, 24-5, 10-6, 25-7,11-8 

def relay_setup():
    GPIO.setmode(GPIO.BCM)
    for channel, pin in CHANNEL_PINS.items():
        GPIO.setup(pin, GPIO.OUT)
        if channel == CHANNEL:
            GPIO.output(pin, GPIO.LOW)
        else:
            GPIO.output(pin, GPIO.HIGH)
        
def test_relay(channel = CHANNEL):
    relay_setup()
    
    try:
        # Run the loop function indefinitely
        while True:
            # Turn the relay ON (HIGH)
            for pin in CHANNEL_PINS[channel]:
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(2)  # Wait for 1 seconds

                # Turn the relay OFF (LOW)
                GPIO.output(pin, GPIO.LOW)
                time.sleep(2)  # Wait for 1 seconds

    except KeyboardInterrupt:
        # If the user presses Ctrl+C, clean up the GPIO configuration
        GPIO.cleanup()
        
def switch_relay(new_channel):
    global CHANNEL
    print("switching", CHANNEL, "to", new_channel)
    if new_channel in CHANNEL_PINS:
        # disconnectng the previous channel
        for pin in CHANNEL_PINS[CHANNEL]:
            GPIO.output(pin, GPIO.HIGH)
        
        # connecting the new channel 
        for pin in CHANNEL_PINS[new_channel]:
            GPIO.output(pin, GPIO.LOW)
        CHANNEL = new_channel
    else:
        print("ERROR: not a valid channel")
        
def turn_off():
    for channel, pin in CHANNEL_PINS.items():
        GPIO.output(pin, GPIO.HIGH)
        
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    relay_setup()
    switch_relay(3)
    time.sleep(3)
    switch_relay(4)
    time.sleep(3)
    switch_relay(5)
    time.sleep(3)
    switch_relay(1)
    time.sleep(3)
    switch_relay(1)


