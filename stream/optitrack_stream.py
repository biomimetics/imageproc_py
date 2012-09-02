import NatNet
import time
import threading, Queue

from imageproc_py.stream.asynch_dispatch import *


class OptitrackStream(threading.Thread):
  def __init__(self, sinks=None, autoStart=True):
    threading.Thread.__init__(self)
    self.daemon = True
    
    self.c = NatNet.NatNetClient(1)
    print self.c.NatNetVersion()

    self.c.SetVerbosityLevel(NatNet.Verbosity_Info)

    self.c.Initialize("127.0.0.1", "127.0.0.1")
    
    self.dispatcher=AsynchDispatch(sinks=sinks,callbacks={'set_time':[self.set_time]})
    self.recieve_queue = Queue.Queue()
    self.input_data = ''

    self.c.SetDataCallback(self.net_data_callback)
    
    self.start_time = time.time()
    
    #TODO: handle multiple rigid bodies effectively
    
    if autoStart:
      self.start()
    
  def run(self):
    while (True):
      pass

  def get(self):
    if not self.recieve_queue.empty():
      return self.recieve_queue.get()
    else:
      return None
      
  def put(self, message):
    self.dispatcher.put(message)

  def add_sinks(self,sinks):
    self.dispatcher.add_sinks(sinks)
  
  def set_time(self,message):
    self.start_time = message.data
    
  #formats data from Optitrack and dispatches it
  def net_data_callback(self, dataFrame):
    bodyData = []
    for body in dataFrame.RigidBodies:
      bodyData.append([time.time()-self.start_time,body.x, body.y, body.z, body.qx, body.qy, body.qz, body.qw])
    
    self.dispatcher.dispatch(Message('optitrack_data', bodyData))
    
    