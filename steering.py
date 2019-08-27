#!/usr/bin/env python3

import time

# Set constants
PWM_OFF = 0
MIN_PULSE_WIDTH = 1000
MAX_PULSE_WIDTH = 1900
AVERAGE_PULSE_WIDTH = (MIN_PULSE_WIDTH + MAX_PULSE_WIDTH) / 2
MIN_STEERING_ANGLE = -25
MAX_STEERING_ANGLE = 25
PULSE_WIDTH_RESOLUTION = (AVERAGE_PULSE_WIDTH - MIN_PULSE_WIDTH) / MAX_STEERING_ANGLE
POSITION_ZERO = 25
ZERO_DEGREES = 0
DELAY = 0.5

# Set PWM pin used to control servo
SERVO_PWM_PIN = 17

class Steering:
	
    ####################################################################
    # PROPERTIES                                                       #
    ####################################################################
    _pigpio = None

    ####################################################################
    # METHODS                                                          #
    ####################################################################
    def __init__(self, pigpio):
        # Set instance of pigpio
        self._pigpio = pigpio

        # If error in pigpio, then display error message and exit
        if not self._pigpio.connected:
            print("ERROR: please enabled pigpiod with 'sudo pigpiod'")
            exit()
                        
    # Convert a given angle in degrees to a pulse width for PWM
    def angle2width(self, angle):
        return AVERAGE_PULSE_WIDTH + angle*PULSE_WIDTH_RESOLUTION

    def steer(self, steering_angle):
        pulse_width = self.angle2width(steering_angle - POSITION_ZERO)

        if pulse_width < MIN_PULSE_WIDTH or pulse_width > MAX_PULSE_WIDTH:
            print("Please provide an argument with an angle value from {} to {}".format(MIN_STEERING_ANGLE, MAX_STEERING_ANGLE))
            
        else:
            self._pigpio.set_servo_pulsewidth(SERVO_PWM_PIN, pulse_width)
            # Maybe a delay will be required here 0.4

    def turn_off(self):
        self._pigpio.set_servo_pulsewidth(SERVO_PWM_PIN, self.angle2width(ZERO_DEGREES))
        time.sleep(DELAY)   # Delay that allows time to return to zero before turn off
        self._pigpio.set_servo_pulsewidth(SERVO_PWM_PIN, PWM_OFF)
