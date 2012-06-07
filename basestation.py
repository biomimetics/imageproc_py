#!/usr/bin/env python
"""
authors: Kevin Peterson and Stan Baek
Modification on 2011-10-4:

This file creates a class BaseStation that can be used to send commands 
to the custom basestation or an XBee module

Wrapper functions are provided for this class, see:
base_functions and robot_functions

"""


import time, os, sys
import command 
from serial import *
from struct import *
from xbee import XBee

class BaseStation(object):

    def __init__(self, port, baud, dest_addr = None, call_back = None):
        self.ser = Serial(port, baud, timeout = 1)
        self.ser.writeTimeout = 5

        if call_back == None:
            self.xb = XBee(self.ser)
        else:
            self.xb = XBee(self.ser, callback = call_back)
        
        self.dest_addr = dest_addr

    def close(self):
        try:
            self.xb.halt()
            self.ser.close()
        except SerialException:
            print "SerialException"

    def sendTX(self, status, type, data ):
        pld = chr(status) + chr(type)  + ''.join(data)
        self.xb.tx(dest_addr = self.dest_addr, data = pld)
        time.sleep(0.1)
        
    def sendAT(self, command, parameter = None, frame_id = None):
        if parameter is not None:
            if frame_id is not None:
                self.xb.at(frame_id = frame_id, command = command, parameter = parameter)
            else:
                self.xb.at(command = command, parameter = parameter)
        elif frame_id is not None:
            self.xb.at(frame_id = frame_id, command = command)
        else:
            self.xb.at(command = command)
        time.sleep(0.1)

    def read(self):
        packet = self.xb.wait_read_frame()

        return packet
        