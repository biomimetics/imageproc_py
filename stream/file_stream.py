import threading
import glob
from asynch_dispatch import *

class FileStream(threading.Thread):
  def __init__(self, sinks=None, autoStart=True):
    
    threading.Thread.__init__(self)
    self.daemon = True
    
    self.new_data = threading.Condition()
    
    self.dispatcher=AsynchDispatch(sinks=sinks,
      callbacks={None:[self.write],'file_line':[self.write],
                'open':[self.open],'close':[self.close]})
                
    self.file = None
      
    if autoStart:
      self.start()
      
  def run(self):
    while(True):
      self.new_data.acquire()
      self.new_data.wait()
      lines = self.file.readlines()
      self.new_data.release()
      
      for line in lines:
        self.dispatcher.dispatch(Message('file_line',line))
  
  def put(self,message):
    self.dispatcher.put(message)
  
  def add_sinks(self,sinks):
    self.dispatcher.add_sinks(sinks)
  
  def file_open(self):
    return self.file is not None
    
  #if file exists, open in read mode, otherwise open in write
  def open(self, message): 
    if len(glob.glob(message.data)) == 1:
      self.new_data.acquire()
      self.file = open(message.data,'r')
      self.new_data.notify()
      self.new_data.release()
    else:
      self.file = open(message.data,'w')
      
  def close(self, message):
    if self.file is not None:
      self.file.close()
      self.file = None
    
  def write(self, message):
    if self.file is not None:
      if message.type == 'file_line':
        self.file.write(str(message.data) + '\n')
      else:
        self.file.write(str(message) + '\n')