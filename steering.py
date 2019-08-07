#!/usr/bin/env python3

import sys
import time
import pigpio

# Set constants
PWM_OFF = 0
MIN_PULSE_WIDTH = 1000
MAX_PULSE_WIDTH = 1900
AVERAGE_PULSE_WIDTH = (MIN_PULSE_WIDTH + MAX_PULSE_WIDTH) / 2
MIN_STEERING_ANGLE = -25
MAX_STEERING_ANGLE = 25
PULSE_WIDTH_RESOLUTION = (AVERAGE_PULSE_WIDTH - MIN_PULSE_WIDTH) / MAX_STEERING_ANGLE

# Set PWM pin used to control servo
SERVO_PWM_PIN = 17

# Convert a given angle in degrees to a pulse width for PWM
def angle2width(angle):
    return AVERAGE_PULSE_WIDTH + angle*PULSE_WIDTH_RESOLUTION

# Set instance of pigpio
pi = pigpio.pi()

# If error in pigpio, then display error message and exit
if not pi.connected:
    print("ERROR: please enabled pigpiod with 'sudo pigpiod'")
    exit()

if len(sys.argv) == 1:
    print("Please provide an argument with an angle value from {} to {}".format(MIN_STEERING_ANGLE, MAX_STEERING_ANGLE))
    
else:
    steering_angle = int(sys.argv[1])
    pulse_width = angle2width(steering_angle)

    if pulse_width < MIN_PULSE_WIDTH or pulse_width > MAX_PULSE_WIDTH:
        print("Please provide an argument with an angle value from {} to {}".format(MIN_STEERING_ANGLE, MAX_STEERING_ANGLE))
        
    else:
        pi.set_servo_pulsewidth(SERVO_PWM_PIN, pulse_width)
        time.sleep(0.4)

# Turn PWM off
pi.set_servo_pulsewidth(SERVO_PWM_PIN, PWM_OFF)

# Release pigpio resources
pi.stop()
