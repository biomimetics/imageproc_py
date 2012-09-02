from threading import *
import time
import math

from imageproc_py.stream.asynch_dispatch import *
from imageproc_py.stream.serial_stream import *

class TreadmillStream(threading.Thread):
  def __init__(self, robot, ctrl_params, period=0.1, sinks=None, autoStart = True):
    threading.Thread.__init__(self)
    self.daemon = True
    
    self.dispatcher=AsynchDispatch(sinks=sinks,
      callbacks={'optitrack_data':[self.optitrack_update],'set_time':[self.set_time]})
    
    self.lock = threading.Condition()
    
    self.robot = robot
    
    self.bounds = ctrl_params[0]
    self.setpoint = ctrl_params[1]
    self.max_speed = ctrl_params[2]
    self.k_p = ctrl_params[3]
    self.k_f = ctrl_params[4]
    
    self.period = period
    
    self.enable = True
    self.in_bounds = False
    self.out_count = 0
    
    self.robot_pos = [0,0,0,0,0,0]
    
    self.treadmill_serial = SerialStream('COM4',115200,sinks={None:[self.receive_serial]})
    
    self.start_time = 0
    
    if autoStart:
      self.start()
    
  def run(self):
    while(True):      
      time.sleep(self.period)
      if self.enable:
        self.lock.acquire()
        
        #print map(int,self.robot_pos)
        
        if self.in_bounds:
          p_term = self.k_p*(self.robot_pos[0] - self.setpoint)
          f_term = self.k_f*self.robot.expected_speed()
          speed = int(p_term + f_term)
    
          if speed < 0:
            speed = 0
          elif speed > self.max_speed:
            speed = self.max_speed
      
          self.treadmill_serial.put(('serial_data',chr(speed)))
        else:
          self.treadmill_serial.put(('serial_data',chr(0)))
        
        self.lock.release()
      
  def put(self,message):
    self.dispatcher.put(message)
    
  def exit(self):
    self.treadmill_serial.put(('serial_data',chr(0)))
    self.enable = False
  
  def receive_serial(self,message):
    data = '%f,%s' % (time.time()-self.start_time, message.data.strip().replace('\t',','))
    self.dispatcher.dispatch(('treadmill_data',data))
  
  def set_time(self,message):
    self.start_time = message.data
    
  def optitrack_update(self,message):
    self.lock.acquire()
    
    # m to mm
    for i in range(3):
      self.robot_pos[i] = message.data[0][i+1]*1000
    
    # quaterion to euler. Optitrack is qx,qy,qz,qw; equation expects qw,qx,qy,qz
    q = message.data[0][4:8]
    q = q[1:] + [q[0]]
    
    self.robot_pos[3] = math.atan2(2*(q[0]*q[1] + q[2]*q[3]), 1-2*(q[1]*q[1]+q[2]*q[2]))
    self.robot_pos[4] = math.asin(2*(q[0]*q[2]-q[3]*q[1]))
    self.robot_pos[5] = math.atan2(2*(q[0]*q[3]+q[1]*q[2]), 1-2*(q[2]*q[2]+q[3]*q[3]))
    
    # radian to degree
    for i in range(3,6):
      self.robot_pos[i] = 180.0*self.robot_pos[i]/math.pi
    
    # check bounds
    good = True
    for i in range(6):
      if self.robot_pos[i] < self.bounds[0][i] or self.robot_pos[i] > self.bounds[1][i]:
        good = False
        break
    
    if not good:
      if self.out_count < 10:
        self.out_count = self.out_count + 1
      else:
        self.in_bounds = False
    else:
      self.out_count = 0
      self.in_bounds = True
    
    self.lock.release()