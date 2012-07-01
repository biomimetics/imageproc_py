from asynch_dispatch import *
import threading
import Queue
import sys

class ConsoleStream(threading.Thread):
  def __init__(self, dispatcher=None, autoStart=True):
    threading.Thread.__init__(self)
    self.daemon = True
    
    self.dispatcher = AsynchDispatch(callbacks = {'serial_data':[self.put]})
    
    if autoStart:
      self.start()
      
  def run(self):
    while(True):
      cmd = sys.stdin.readline()
      if cmd:
        self.dispatcher.dispatch(Message('console_input',cmd.strip()))
  
  def add_sinks(self, sinks):
    self.dispatcher.add_sinks(sinks)
    
  def put(self, message):
    print message