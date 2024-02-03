import cv2
import time
import RPi.GPIO as GPIO

# Define the GPIO pin for the LED
led_pin = 23  # Change this to the actual GPIO pin you are using
switch_pin = 22  # Adjust the pin number as per your connection

num = 0

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
        # print("Switch pressed - LED ON")
        # GPIO.output(led_pin, GPIO.HIGH)

        if len(frame.shape) == 3 and frame.shape[2] == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imwrite(f"/home/rasp/Desktop/HandS_Braille/captured_img/test_cap_img{num}.jpg", frame)
        print("image captured")

        # time.sleep(5)
        num += 1

    else:
        print("Switch not pressed - LED OFF")
    #    GPIO.output(led_pin, GPIO.LOW)

    # Add a small delay to avoid unnecessary CPU usage
    time.sleep(0.1)


    # Display the frame
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