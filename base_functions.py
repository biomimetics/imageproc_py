#!/usr/bin/env python

"""
authors: Kevin Peterson
Modification on 2011-10-4:

This file creates a class BaseFunctions that are some commonly used functions
for changing parameters on the basestation/XBee modules

This class depends upon the class BaseStation
Functions for communicating with the robot can be found in
the class RobotFunctions

USAGE:
For all commands, the basestation will only return a packet if the frame_id is nonzero
The frame_id is used for syncronizing sent packets from the computer with responses from
the basestation

"""

import time, os, sys
import command
from struct import *

class BaseFunctions(object):
    
    def __init__(self, basestation):
        self.bs = basestation
        
    def close(self):
        self.bs.close()

    def getChannel(self, frame_id):
        self.bs.sendAT(command='CH',frame_id=frame_id)

    def setChannel(self, param, frame_id = None):
        self.bs.sendAT(command='CH',parameter=param,frame_id = frame_id)

    def getPanID(self, frame_id):
        self.bs.sendAT(command='ID',frame_id=frame_id)
        
    def setPanID(self, param, frame_id = None):
        self.bs.sendAT(command='ID',parameter=param,frame_id = frame_id)
        
    def getSrcAddr(self, frame_id):
        self.bs.sendAT(command='MY',frame_id=frame_id)
        
    def setSrcAddr(self, param, frame_id = None):
        self.bs.sendAT(command='MY',parameter=param,frame_id = frame_id)

    def getLastAckd(self, frame_id):
        self.bs.sendAT(command='EA',frame_id=frame_id)
        
    #Basestation Only, no XBee
    def setSnifferMode(self, on):
        self.bs.sendAT(command='SN',parameter=chr(on))

