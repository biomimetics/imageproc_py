#!/usr/bin/python
#
# Copyright (c) 2010-2012, Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the University of California, Berkeley nor the names
#   of its contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
#
# Wireless interface abstraction
#
# by Stanley S. Baek
#
# v.0.1
#
# Revisions:
#  Stanley S. Baek                  2010        Initial release.
#  Fernando L. Garcia Bermudez      2012-3-4    Defined radio abstraction
#                                               layer, adding destructor.
#
# Notes:
#  - This file is derived from basestation.py, by Stanley S. Baek.
#

import sys, time
import serial, xbee


class radio:
    def __init__(self, port, baudrate, callback):
        try:
            self.serial = serial.Serial(port, baudrate, timeout=3, rtscts=0)
            self.radio  = xbee.XBee(self.serial, callback=callback)
        except self.serial.serialutil.SerialException as e:
            print("SerialException: " + str(e))
            sys.exit(1)
    def send(self, dest_addr, pkt_status, pkt_type, pkt_data):
        self.radio.tx(dest_addr=dest_addr, data=(chr(pkt_status) +            \
                                                chr(pkt_type) + str(pkt_data)))
        time.sleep(.1)
    def __del__(self):
        self.radio.halt()
        self.serial.close()
