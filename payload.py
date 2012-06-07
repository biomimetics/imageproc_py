#!/usr/bin/env python
"""
stanbaek
2010-11-18

"""

from struct import *

HEADER_LENGTH = 2
STATUS_POSITION = 0
TYPE_POSITION = 1
#SQN_POSITION = 2
DATA_POSITION = 2

class Payload(object):
    
    def __init__(self, data, status = None, type = None):
        
        if status == None:  # str type data contains type, status, and sqn
            self.status = ord(data[STATUS_POSITION])
            self.type = ord(data[TYPE_POSITION])
            #(self.sqn, ) = unpack('H', data[SQN_POSITION:SQN_POSITION+2])
            self.data = data[DATA_POSITION:]
            self.data_len = len(data) - HEADER_LENGTH
        else:
            self.status = status
            self.type = type
            #self.sqn = sqn
            self.data = data
            self.data_len = len(data)

    def __repr__(self):
        # return chr(self.status) + chr(self.type) +  ''.join(pack('H', self.sqn)) + ''.join(self.data)
        return chr(self.status) + chr(self.type) +  ''.join(self.data)

    def __str__(self):
        # return chr(self.status) + chr(self.type) +  ''.join(pack('H', self.sqn)) + ''.join(self.data)
        return chr(self.status) + chr(self.type) + ''.join(self.data)

    def __len__(self):
        return self.data_len + HEADER_LENGTH

    


if __name__ == '__main__':

    pld1 = Payload("Need Medical Attention?", 0, 0x3f, 1024)
    rf_data = chr(0) + chr(0x3f) + ''.join(pack('H', 1024)) + ''.join("Hello World")
    pld2 = Payload(rf_data)

    print pld1
    print len(pld1), str(pld1)
    print pld1.status, pld1.type, pld1.data
    print pld2
    print len(pld2), str(pld2)
    print pld2.status, pld2.type, pld2.data


