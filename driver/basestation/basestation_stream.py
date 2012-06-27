from xbee import XBee
import threading
import Queue
import time
import serial
import sys
from struct import pack

class BasestationStream(threading.Thread):
  def __init__(self, port='COM1', baudrate=230400, addr=0x2071, timeout=-1, 
      timeoutFunction = None):
      
    threading.Thread.__init__(self)
    self.daemon = True
    
    try:
      self.ser = serial.Serial(port, baudrate, timeout=3, rtscts=0)
      
    except serial.serialutil.SerialException:
      print "Could not open serial port:%d"
      sys.exit()
    
    self.addr = addr
    
    self.timeout = timeout
    self.last_time = -1
    self.timeoutFunction = timeoutFunction
    self.xb = XBee(self.ser, callback = self.receiveCallback)
    self.send_queue = Queue.Queue()
    self.receive_queue = Queue.Queue()
    
  def run(self):
    while True:
      if self.last_time != -1 and self.timeout != -1 \
          and self.timeoutFunction is not None \
          and (time.time() - self.last_time) > self.timeout:
        self.timeoutFunction()
        
      if not self.send_queue.empty():
        entry = self.send_queue.get()
        
        if entry[0] == 'packet':
          pkt = entry[1]
          print pkt
          #self.xb.tx(dest_addr = pack('>h',pkt.dest_addr), data = pkt.payload)
          self.xb.tx(dest_addr = pack('>h',pkt.dest_addr), data = (chr(0) + chr(0x88) + ''.join(pack('h',0))))
        
        elif entry[0] == 'quit':
          self.xb.halt()
          self.ser.close()
          sys.exit()
    
  def get(self):
    if not self.receive_queue.empty():
      return self.receive_queue.get()
    else:
      return None
  
  def put(self,entry):
    self.send_queue.put(entry)
    
  def receiveCallback(self,xbee_data):
    self.last_time = time.time()
    pkt = Packet(dest_addr=self.addr, time=self.last_time,
      payload=xbee_data.get('rf_data'))
    self.receive_queue.put(('packet',pkt))
  
  def sendPacket(self,pkt):
    self.send_queue.put(('packet',pkt))
  