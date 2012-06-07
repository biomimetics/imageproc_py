#!/usr/bin/env python

"""
authors: Kevin Peterson
Modification on 2011-10-4:

This file creates a class RobotFunctions that are some commonly used functions
for commanding the obots with an ImageProc2 board

This class depends upon the class BaseStation
Functions for communicating with the basestation can be found in
the class BaseFunctions

"""

import time, os, sys
import command
from struct import *

class RobotFunctions(object):
    def __init__(self, basestation):
        self.bs = basestation
        
    def close(self):
        self.bs.close()
        
    def go(self, pwm):
        self.bs.sendTX(0, command.SET_THRUST, pack('f', pwm))

    def stop(self):
        self.bs.sendTX(0, command.SET_THRUST, pack('f', 0))

    def echo(self,data):
        self.bs.sendTX(0, command.ECHO, data)

    def connect(self):
        self.bs.sendTX(0, command.ECHO, "Connection Successful")

    def IMUone(self):
        self.bs.sendTX(0, command.GET_IMU_DATA, '')

    def IMUloop(self,t):
        del dataloop[:]
        self.bs.sendTX(0, command.GET_IMU_LOOP, pack('L', t*1000000.0))
        #time.sleep(t)

    def Runloop(self,t, pwm):
        self.bs.sendTX(0, command.RUN_IMU_LOOP, pack('Lf', t*1000000.0, pwm))
        #time.sleep(t)

    def PostRunloop(self):
        self.bs.sendTX(0, command.POSTRUN_IMU_LOOP, '')
        #time.sleep(t)

    def PreRunloop(self):
        self.bs.sendTX(0, command.PRERUN_IMU_LOOP, '')
        #time.sleep(t)

    def delaygo(self,d, pwm):
        time.sleep(d)
        go(pwm)

    def delayRunloop(self,d, t, pwm):
        time.sleep(d)
        Runloop(t, pwm)

    def EraseMem(self):
        self.bs.sendTX(0, command.ERASE_MEM_SECTOR, '')

    def ReadFlash(self):
        self.bs.sendTX(0, command.TX_SAVED_IMU_DATA, '')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    