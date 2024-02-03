import cv2
import RPi.GPIO as GPIO
import time

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the LED
led_pin = 23  # Change this to the actual GPIO pin you are using

# Setup the GPIO pin as an output
GPIO.setup(led_pin, GPIO.OUT)

# Create a VideoCapture object
cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera (you can also use a file path)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Loop to continuously capture and display frames
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    GPIO.output(led_pin, GPIO.HIGH)
    print("LED is ON")

    # Check if the frame was read successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the frame
    cv2.imshow('Video', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        GPIO.output(led_pin, GPIO.LOW)
        print("LED is OFF")
        GPIO.cleanup()
        break

# Release the VideoCapture and close the OpenCV window
cap.release()
GPIO.cleanup()
cv2.destroyAllWindows()