from xbee import XBee
import time
import serial
import sys
from struct import pack
import threading

from imageproc_py.stream.asynch_dispatch import *

class BasestationStream(threading.Thread):
  def __init__(self, port='COM1', baudrate=230400, addr=0x2071, sinks=None, timeout=-1, 
      timeoutFunction = None):
    
    threading.Thread.__init__(self)
    self.daemon = True
    
    try:
      self.ser = serial.Serial(port, baudrate, timeout=3, rtscts=0)
      self.xb = XBee(self.ser)
    except serial.serialutil.SerialException:
      print "Could not open serial port:%s" % port
      self.xb = None
    
    self.dispatcher=AsynchDispatch(sinks=sinks,
      callbacks={'packet':[self.send]})
      
    self.addr = addr
    
    self.timeout = timeout
    self.last_time = -1
    self.timeoutFunction = timeoutFunction
    
    old_timeout_code = '''def run(self):
    while True:
    if self.last_time != -1 and self.timeout != -1 \
          and self.timeoutFunction is not None \
          and (time.time() - self.last_time) > self.timeout:
        self.timeoutFunction()  '''
  
  def run(self):
    if self.xb is not None:
      while(True):
        data = self.xb.wait_read_frame()
        self.receive_callback(data)
        
  def exit(self):
    self.xb.halt()
    self.ser.close()
    self.xb = None
    
  def put(self,message):
    self.dispatcher.put(message)
    
  def receive_callback(self,xbee_data):
    self.last_time = time.time()
    
    pkt = Packet(dest_addr=self.addr, time=self.last_time,
      payload=xbee_data.get('rf_data'))
    self.dispatcher.dispatch(('packet',pkt))
  
  def send(self,message):
    pkt = message.data
    self.xb.tx(dest_addr = pack('>h',pkt.dest_addr), data = pkt.payload)
  