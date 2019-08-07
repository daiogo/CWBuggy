#!/usr/bin/env python3

import sys
import time
import pigpio

# Set constants
HIGH = 1
LOW = 0
PWM_OFF = 0
PULSE_WIDTH_RESOLUTION = 10000
MIN_PULSE_WIDTH = 0
MAX_PULSE_WIDTH = 100
PWM_FREQUENCY = 25

# Set pins used to control motor
MOTOR_PWM_PIN = 18
IN3 = 23
IN4 = 24

# Set instance of pigpio
pi = pigpio.pi()

# If error in pigpio, then display error message and exit
if not pi.connected:
    print("ERROR: please enabled pigpiod with 'sudo pigpiod'")
    exit()

if len(sys.argv) == 1:
    print("Please provide an argument with a pulse width value from {} to {}".format(MIN_PULSE_WIDTH, MAX_PULSE_WIDTH))
    
else:
    # Get pulse width value from args
    pulse_width = int(sys.argv[1])
    
    # Get direction and change sign if necessary
    if pulse_width < 0:
        pi.write(IN3, HIGH)
        pi.write(IN4, LOW)
        pulse_width *= -1
    else:
        pi.write(IN3, LOW)
        pi.write(IN4, HIGH)
        
    if pulse_width < MIN_PULSE_WIDTH or pulse_width > MAX_PULSE_WIDTH:
        print("Please provide an argument with a pulse width value from {} to {}".format(MIN_PULSE_WIDTH, MAX_PULSE_WIDTH))
        
    else:        
        # Multiply pulse width by resolution
        pulse_width *= PULSE_WIDTH_RESOLUTION
        
        # Start PWM
        pi.hardware_PWM(MOTOR_PWM_PIN, PWM_FREQUENCY, pulse_width)
        time.sleep(5)
        pi.hardware_PWM(MOTOR_PWM_PIN, PWM_FREQUENCY, PWM_OFF)
        
# Release pigpio resources
pi.stop()
