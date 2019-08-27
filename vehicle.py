#!/usr/bin/env python3

import pigpio
import engine
import steering

class Vehicle:
    
    ####################################################################
    # PROPERTIES                                                       #
    ####################################################################
    _pigpio = None          # pigpio object
    _engine = None          # Engine object
    _steering = None        # Steering object
    _horn = None			# Horn object
    _immobilized = True     # Immobilized flag

    ####################################################################
    # METHODS                                                          #
    ####################################################################
    def __init__(self):
        # Instantiate pigpio object
        self._pigpio = pigpio.pi()
        self._engine = engine.Engine(self._pigpio)
        self._steering = steering.Steering(self._pigpio)
        #self._horn = horn.Horn(self._pigpio)
        
    def __del__(self):
        self._pigpio.stop()
        
    def control_vehicle(self, steering_angle, throttle_position, horn):
        self._steering.steer(steering_angle)
        self._engine.accelerate(throttle_position)
        #self._horn.honk(horn)
        print("Steering angle: {}".format(steering_angle))
        print("Throttle position: {}".format(throttle_position))
        #print("Horn: {}".format(horn))

    def immobilize_vehicle(self):
        self._immobilized = True
        self._steering.turn_off()
        self._engine.turn_off()

    def set_immobilized(self, value):
        self._immobilized = value

    def get_immobilized(self):
        return self._immobilized
