import RPi.GPIO as GPIO
import time

# Define GPIO pins for switch and LED
switch_pin = 17  # Adjust the pin number as per your connection
led_pin = 23     # Adjust the pin number as per your connection

# Set up GPIO mode and initial state
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)

try:
    while True:
        # Check if the switch is pressed
        if GPIO.input(switch_pin) == GPIO.LOW:
            print("Switch pressed - LED ON")
            GPIO.output(led_pin, GPIO.HIGH)
        else:
            print("Switch not pressed - LED OFF")
            GPIO.output(led_pin, GPIO.LOW)

        # Add a small delay to avoid unnecessary CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    # Cleanup GPIO on program exit
    GPIO.cleanup()