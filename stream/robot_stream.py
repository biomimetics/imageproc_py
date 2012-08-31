from struct import pack

from imageproc_py.stream.basestation_stream import *
from imageproc_py.protocol.packet import *
from imageproc_py.protocol.protocol import *

class RobotStream():
  INIT      = 0
  RESET     = 1
  SET_GAINS = 2
  READY     = 3
  FAIL      = 4
  
  def __init__(self, basestation=None, addr=0x2072):
    self.basestation = basestation
    
    self.dispatcher=AsynchDispatch(sinks=sinks,
      callbacks={'packet':[self.process_packet]})
      
    if self.basestation is not None:
      self.basestation.register_robot(self, addr)
      
    self.addr = addr
    
    self.state = RobotStream.INIT
    
    self.new_data = threading.Condition()
    
  def run(self):
    while(True):
      self.new_data.acquire()
      self.new_data.wait()
      
      if self.state == RobotStream.INIT:
        self.reset()
        self.state = RobotStream.RESET
        
      elif self.state == RobotStream.RESET:
        
        self.set_motor_gains([8000,100,0,0,10 , 8000,100,0,0,10]) #Hardware PID
        
      elif self.state == RobotStream.SET_GAINS:
      elif self.state == RobotStream.READY:
      elif self.state == RobotStream.FAIL:
      
  def process_packet(self,message):
    pkt = message.data
    
    if pkt.dest_addr = self.addr
    
  def send_packet(self, type, data=''):
    if self.basestation is not None:
      self.basestation.put(Message('packet',Packet(type,data,0,self.addr)))
  
  
      
  def put(self,message):
    self.dispatcher.put(message)
    
  def reset(self):
    #xb_send(shared.xb, shared.DEST_ADDR, 0, command.SOFTWARE_RESET, pack('h',1))
    print 'Resetting Robot'
    self.send_packet('SOFTWARE_RESET')
      
  def set_motor_gains(self, gains):
    print 'Setting Gains'
    self.send_packet('SET_PID_GAINS',pack('10h',*gains))
            
  def set_motor_speeds(self, spleft, spright):
    print 'Setting Speed'
    thrust = [spleft, 0, spright, 0, 0]
    self.send_packet('SET_THRUST_CLOSED_LOOP',pack('5h',*thrust))