import cv2
import time
import RPi.GPIO as GPIO
import os, time
from braille_contour_center import *
from output_6bit import *
from translate_braille2string import *

# Define the GPIO pin for the LED
led_pin = 23  # Change this to the actual GPIO pin you are using
switch_pin = 22  # Adjust the pin number as per your connection

num = 1

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Setup the GPIO pin as an output
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(led_pin, GPIO.LOW)

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

    # Check if the frame was read successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Check if the switch is pressed
    if GPIO.input(switch_pin) == GPIO.LOW:
        cv2.imwrite(f"/home/rasp/Desktop/HandS_Braille/src/img_capture/cap_img{num}.jpg", frame)
        print("image captured")

        cropped, binary = preprocess_img(f'/home/rasp/Desktop/HandS_Braille/src/img_capture/cap_img{num}.jpg')
        contour = find_contour_center(binary)

        six_bit = dot2braille(contour)
        string = translate(six_bit)
        print(string)
        os.system(f"espeak -v ko '{string}'")

        num += 1

    else:
        print("Switch not pressed - LED OFF")
    #    GPIO.output(led_pin, GPIO.LOW)

    # Add a small delay to avoid unnecessary CPU usage
    time.sleep(0.1)


    # Display the frame for testing
    # cv2.imshow('Video', frame)

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