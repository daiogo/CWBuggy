#!/usr/bin/env python3

import socket
import vehicle

# Define constants
PORT = 5541
RECEIVE_BUFFER_SIZE = 4

class Remote:
    
    ####################################################################
    # PROPERTIES                                                       #
    ####################################################################
    _socket = None          # Socket object
    _connection = None      # Connection object
    _address = None         # Address string
    _command = b''          # Commands to the vehicle
    _steering_angle = 0     # Vehicle steering angle in º
    _throttle_position = 0  # Throttle position in %
    _horn = 0               # Horn status
    _vehicle = None         # Vehicle object

    ####################################################################
    # METHODS                                                          #
    ####################################################################
    def __init__(self, vehicle):
        self._vehicle = vehicle
    
    def create_socket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self._socket.bind(("", PORT))
        self._socket.listen()

    def accept_connection(self):
        # Accept incoming connection request
        print("Waiting for connection...")
        self._connection, self._address = self._socket.accept() # Blocking code
        print("Connected to: ", self._address)

    def close_connection(self):
        # Immobilize vehicle before closing the connection
        self._vehicle.immobilize_vehicle()

        # Close connection
        print("\nClosing connection...")
        self._connection.close()
        self._connection = None
        print("Connection closed")


    def close_socket(self):
        # Close socket if process is terminated and exit loop
        print("\nClosing socket...")
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()
        print("Socket closed")

    def receive_command(self):
        # Receive data from remote controller
        self._command = self._connection.recv(RECEIVE_BUFFER_SIZE)  # Blocking code
        
        # If client closed connection on his side, then also close on server side
        if self._command == b'':
            self._steering_angle = 25
            self._throttle_position = 100
            self._horn = 0
            self.close_connection()
            
        else:
            # Extract commands from received data
            self._steering_angle = self._command[0]
            self._throttle_position = self._command[1]
            self._horn = self._command[2]

    def start(self):
        self.create_socket()
        
        # As long the process isn't finished
        while 1:
            
            # If there are no connections, then wait for one
            if self._connection == None:
                try:
                    self.accept_connection()
                    self._vehicle.set_immobilized(False)
                
                # If user presses Ctrl-C while accept() is executing, then close the socket
                except KeyboardInterrupt:
                    self.close_socket()
                    break
                    
            # Receive commands and control vehicle
            try:
                self.receive_command()
                if self._vehicle.get_immobilized() == False:
                    self._vehicle.control_vehicle(self._steering_angle, self._throttle_position, self._horn)
            
            # If user presses Ctrl-C while recv() is executing, then close the connection
            except KeyboardInterrupt:
                self.close_connection()
                
