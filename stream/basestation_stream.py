from xbee import XBee
import time
import serial
import sys
from struct import pack,unpack
import threading

from imageproc_py.stream.asynch_dispatch import *
from imageproc_py.protocol.packet import *

class BasestationStream(threading.Thread):
  def __init__(self, port='COM1', baudrate=230400, addr=0x2071, sinks=None, autoStart=True):
    
    threading.Thread.__init__(self)
    self.daemon = True
    
    self.robots = {}
    
    try:
      self.ser = serial.Serial(port, baudrate, timeout=3, rtscts=0)
      self.xb = XBee(self.ser)
    except serial.serialutil.SerialException:
      print "Could not open serial port:%s" % port
      self.xb = None
    
    self.dispatcher=AsynchDispatch(sinks=sinks,
      callbacks={'packet':[self.send]})
      
    self.addr = addr
        
    if autoStart:
        self.start()
        
  def run(self):
    if self.xb is not None:
      while(True):
        data = self.xb.wait_read_frame()
        self.receive_callback(data)
        
  def exit(self):
    if self.xb is not None:
      self.xb.halt()
      self.ser.close()
      self.xb = None
    
  def put(self,message):
    self.dispatcher.put(message)
    
  def receive_callback(self,xbee_data):
    self.last_time = time.time()
    pkt = Packet(dest_addr=self.addr, time=self.last_time,
      payload=xbee_data.get('rf_data'))
      
    source_addr = unpack('>h',xbee_data.get('source_addr'))
    source_addr = source_addr[0]
    
    if source_addr in self.dispatcher.sinks.keys():
      self.dispatcher.dispatch((source_addr,pkt))
    else:
      self.dispatcher.dispatch(('packet',pkt))
    
  def send(self,message):
    pkt = message.data
    self.xb.tx(dest_addr = pack('>h',pkt.dest_addr), data = pkt.payload)
  
  def register_robot(self,robot,addr):
    self.dispatcher.add_sinks({addr:[robot.put]})