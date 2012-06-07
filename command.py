#!/usr/bin/env python
"""
cmd module
authors: stanbaek
Created on 2010-07-07:

"""

# CMD values of 0x00 - 0x7F(127) are defined here
# Add CMD definitions 
# for bootloader (0x00 - 0x1F)

###########################################################
##          DEPRICATED 

CMD_NACK = 0x00        # START_APPLICATION = 0
CMD_ACK = 0x01
CMD_READ_PM = 0x02
CMD_WRITE_PM = 0x03
CMD_READ_EE = 0x04
CMD_WRITE_EE = 0x05
CMD_READ_CM = 0x06
CMD_WRITE_CM = 0x07
CMD_RESET = 0x08
CMD_READ_ID = 0x09
CMD_READ_GOTO = 0x10
#################################################################


BOOTLOADER = 0x00

SET_AUTO_CTRL = 0x11
SET_REMOTE_CTRL = 0x12

SET_PID_YAW = 0x16
SET_PID_PITCH = 0x18

SET_THRUST = 0x1A
SET_STEER = 0x1B
SET_STEER_MODE = 0x1C
SET_RC_VALUES = 0x1D


ECHO = 0x1F      # send back the received packet

# for IMU (0x20 - 0x3F)
GET_IMU_DATA = 0x20
GET_WII_DATA = 0x22

RUN_GYRO_CALIB = 0x24
GET_GYRO_CALIB_PARAM = 0x25

SET_SAVE_DATA_FLASH = 0x26
SET_ESTIMATE_RUNNING = 0x27

TX_SAVED_STATE_DATA = 0x2B
TX_DUTY_CYCLE = 0x2C    # no longer used (2011-01-27)

START_BODE = 0x33
SET_YAW_RATE_FILTER = 0x34
SET_PITCH_RATE_FILTER = 0x35

ERASE_MEM_SECTOR = 0x3A

RESET_STOPWATCH = 0x3B

BASE_ECHO = 0x3f


# CMD values of 0x80(128) - 0xEF(239) are available for user applications.

# CMD values of 0xF0(240) - 0xFF(255) are reserved for future use



