# This is a script to control a relay using a raspberry pi 400 GPIO pins
import RPi.GPIO as GPIO
import time

CHANNEL = 1
CHANNEL_PINS = [12] # put GPIO pins or smth here maybe?? something to help with switching

# connections:
# connect COM on all positive modules to positive terminal of PROVA
# connect NO on all positive modules to negative (right side usually) terminal of respective terminal

# setup the relay GPIO pins, initally making all relays closed
def relay_setup():
    GPIO.setmode(GPIO.BCM)
    for pin in CHANNEL_PINS:
        GPIO.setup(pin, GPIO.OUT)
        
def test_relay(channel = CHANNEL):
    relay_setup()
    
    try:
        # Run the loop function indefinitely
        while True:
            # Turn the relay ON (HIGH)
            GPIO.output(CHANNEL_PINS[channel-1], GPIO.HIGH)
            time.sleep(1)  # Wait for 1 seconds

            # Turn the relay OFF (LOW)
            GPIO.output(CHANNEL_PINS[channel-1], GPIO.LOW)
            time.sleep(1)  # Wait for 1 seconds

    except KeyboardInterrupt:
        # If the user presses Ctrl+C, clean up the GPIO configuration
        GPIO.cleanup()
        
def switch_relay(new_channel):
    GPIO.output(CHANNEL_PINS[CHANNEL-1], GPIO.LOW)
    GPIO.output(CHANNEL_PINS[new_channel-1], GPIO.HIGH)
    CHANNEL = new_channel

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHANNEL_PINS[CHANNEL-1], GPIO.OUT)
    GPIO.output(CHANNEL_PINS[CHANNEL-1], GPIO.LOW) # turn relay off
    GPIO.output(CHANNEL_PINS[CHANNEL-1], GPIO.HIGH) # turn relay on
