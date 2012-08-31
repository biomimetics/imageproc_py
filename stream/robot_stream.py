from struct import pack

from imageproc_py.stream.basestation_stream import *
from imageproc_py.protocol.packet import *
from imageproc_py.protocol.protocol import *

class RobotStream():
  def __init__(self, basestation=None, addr=0x2072):
    self.basestation = basestation
    self.addr = addr
    
    self.reset()
    self.set_motor_gains([8000,100,0,0,10 , 8000,100,0,0,10]) #Hardware PID
  
  def send_packet(self, type, data=''):
    if self.basestation is not None:
      self.basestation.put(Message('packet',Packet(type,data,0,self.addr)))
    
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