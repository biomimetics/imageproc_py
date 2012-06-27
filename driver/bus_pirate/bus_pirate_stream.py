from pyBusPirateLite.UART import *
from asynch_dispatch import *
import threading
import Queue
import time

class BusPirateStream(threading.Thread):
  def __init__(self, port='COM9', sinks=None, autoStart=True):
    threading.Thread.__init__(self)
    self.daemon = True
    
    self.send_lock = threading.Lock()
    
    self.dispatcher=AsynchDispatch(
      callbacks={'reset':[self.reset_grid],
                 'serial_data':[self.send]})
    
    try:
      self.bp = UART(port,115200)
      self.bp.BBmode()
      self.setup_UART()
      
      self.bp.cfg_pins(PinCfg.POWER)
      
      self.bp.begin_input()
    except:
      print 'Failed to start BusPirate'
      self.bp = None
      
    self.send_queue = Queue.Queue()
    
    if autoStart:
      self.start()
    
  def run(self):
    if self.bp is not None:
      while(True):
        self.send_lock.acquire()
        rx_byte = self.bp.response(256,True)
        if rx_byte != '':
          self.dispatcher.dispatch(Message('serial_data',rx_byte))
        self.send_lock.release()
        
  def send(self, message):
    self.send_lock.acquire()
    self.bp.port.timeout = None
    self.bp.end_input()
    self.bp.cfg_pins(PinCfg.POWER|PinCfg.AUX)
    
    self.bp.bulk_trans(1,map(ord,list(message.data)))
    
    self.bp.begin_input()
    self.bp.cfg_pins(PinCfg.POWER)
    self.bp.port.timeout = 0.1
    self.send_lock.release()
    
  def setup_UART(self):
    if self.bp is not None:
      self.bp.enter_UART()
      self.bp.set_cfg(UARTCfg.OUTPUT_OPENC | UARTCfg.DATA_8N | UARTCfg.STOP_1 | UARTCfg.RX_NORMAL)
      self.bp.set_speed(UARTSpeed._1200)
      self.bp.begin_input()
  
  def reset_grid(self):
    if self.bp is not None:
      self.send_lock.acquire()
      self.bp.cfg_pins(0)
      time.sleep(0.5)
      self.bp.cfg_pins(PinCfg.POWER)
      self.send_lock.release()