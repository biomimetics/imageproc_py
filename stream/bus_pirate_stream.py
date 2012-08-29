import threading
import Queue
import time

from imageproc_py.stream.py_bus_pirate_lite.UART import *
from imageproc_py.stream.asynch_dispatch import *

class BusPirateStream(threading.Thread):
  def __init__(self, port='COM1', sinks=None, autoStart=True):
    threading.Thread.__init__(self)
    self.daemon = True
    
    self.dispatcher=AsynchDispatch(sinks=sinks,
      callbacks={'serial_data':[self.send]})
    
    try:
      self.bp = UART(port,115200)
    except:
      print 'Failed to start BusPirate'
      self.bp = None
    
    if autoStart:
      self.start()
    
  def run(self):
    if self.bp is not None:
      while(True):
        rx_bytes = self.bp.response(1000,True)
        if rx_bytes != '':
          self.dispatcher.dispatch(Message('serial_data',rx_bytes))
        
  def send(self, message):
    if self.bp is not None:
      self.bp.bulk_trans(len(message.data),map(ord,list(message.data)))