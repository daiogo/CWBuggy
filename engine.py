#!/usr/bin/env python3

# Set constants
HIGH = 1
LOW = 0
PWM_OFF = 0
PULSE_WIDTH_RESOLUTION = 10000
MIN_PULSE_WIDTH = 0
MAX_PULSE_WIDTH = 100
PWM_FREQUENCY = 25
REVERSE_OFFSET = 100
ENGINE_OFF = 100

# Set pins used to control motor
MOTOR_PWM_PIN = 18
IN3 = 23
IN4 = 24

class Engine:

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

    def accelerate(self, throttle_position):
        # Get pulse width value by subtracting offset from throttle position
        pulse_width = throttle_position - REVERSE_OFFSET
        
        # Get direction and change sign if necessary
        if pulse_width < 0:
            # Reverse
            self._pigpio.write(IN3, HIGH)
            self._pigpio.write(IN4, LOW)
            pulse_width *= -1
        else:
            # Forward
            self._pigpio.write(IN3, LOW)
            self._pigpio.write(IN4, HIGH)
            
        # If the pulse width value isn't within range
        if pulse_width < MIN_PULSE_WIDTH or pulse_width > MAX_PULSE_WIDTH:
            print("Please provide an argument with a pulse width value from {} to {}".format(MIN_PULSE_WIDTH, MAX_PULSE_WIDTH))
            
        else:        
            # Multiply pulse width by resolution
            pulse_width *= PULSE_WIDTH_RESOLUTION
            
            # Start PWM
            self._pigpio.hardware_PWM(MOTOR_PWM_PIN, PWM_FREQUENCY, pulse_width)

    def turn_off(self):
        self._pigpio.hardware_PWM(MOTOR_PWM_PIN, PWM_FREQUENCY, ENGINE_OFF)
