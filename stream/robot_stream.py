from struct import pack
import time

from imageproc_py.stream.basestation_stream import *
from imageproc_py.protocol.packet import *
from imageproc_py.protocol.protocol import *

class RobotStream():
  def __init__(self, basestation=None, addr=0x2072, sinks=None):
    self.basestation = basestation
    
    self.dispatcher=AsynchDispatch(sinks=sinks,
      callbacks={addr:[self.receive_packet],
                'console_input':[self.receive_command]})
      
    if self.basestation is not None:
      self.basestation.register_robot(self, addr)
      
    self.addr = addr
    
    # [Kp Ki Kd Kanti-wind ff]
    # now uses back emf velocity as d term
    self.motorgains = [500,0,250,0,50, 500,0,250,0,50]
    self.cycle = 125 # ms for a leg cycle
    self.delta = [8,8,8,8]  # adds up to 32 counts
    self.intervals = []  # total 213 ms
    self.vel = []  # = 256*delta/interval
    
    self.duration = 5000
    self.count = 0
    
    self.motor_gains_set = False
    self.telemetry = False
    
    print 'stream_keyboard_telem Aug. 31, 2012\n'
    print "using robot address", hex(self.addr)
  
    count = 0
    while not(self.motor_gains_set):
      print "Setting motor gains. Packet:",count
      count = count + 1
      self.set_pid_gains(self.motorgains)
      time.sleep(2)
      if count > 8:
        print "count exceeded"
        break
    
    time.sleep(0.5)  # wait for whoami before sending next command
    self.set_vel_profile()
    
    self.running = False
    self.last_time = time.time() - self.duration/1000.0
    
    print 'Robot Ready'
    
  #set velocity profile
  def set_vel_profile(self):
    self.intervals = [self.cycle/4, self.cycle/4, self.cycle/4, self.cycle/4]
    tempsum = self.intervals[0]+self.intervals[1]+self.intervals[2]+self.intervals[3]
    self.intervals[3]=self.intervals[3]+self.cycle - tempsum
    self.vel = [self.delta[0]*256/self.intervals[0],
                self.delta[1]*256/self.intervals[1],
                self.delta[2]*256/self.intervals[2],
                self.delta[3]*256/self.intervals[3]]
    temp = self.intervals+self.delta+self.vel
    temp = temp+temp  # left = right
    #print temp
    self.send_packet('SET_VEL_PROFILE', pack('24h',*temp))
    time.sleep(.15)
  
  def receive_command(self,message):
    cmd = message.data.split()
    if len(cmd)>0:
      keypress = cmd[0][0]
      
      if keypress == 'e':
        self.send_packet('ECHO',  "Echo Test")
      elif keypress =='n':
        self.send_packet('WHO_AM_I', 'Robot Echo')
      elif keypress == 'r':
        self.reset()
      elif keypress == 'a' and len(cmd)>1:
        self.cycle = 1000/int(cmd[1])
        #print 'cycle='+str(self.cycle)+' duration='+str(self.duration)+'. New Frequency (Hz):',
        self.set_vel_profile()
      elif (keypress == 'd') and len(cmd)>1:
        self.duration = int(cmd[1])
        self.last_time = time.time() - self.duration/1000.0
      elif (keypress == 'p'):
        self.proceed()
      elif (keypress == 'f'):
        self.flash_readback()

  def receive_packet(self,message):
    pkt = message.data
    p = Protocol()
    if pkt.pkt_type == p.find('SET_PID_GAINS').value:
			self.motor_gains_set = True
    #print "From Robot:",str(pkt)
    
  def send_packet(self, type, data=''):
    if self.basestation is not None:
      pkt = Packet(type,data,0,self.addr)
      #print 'To Robot:',str(pkt)
      self.basestation.put(Message('packet',pkt))
  
  def put(self,message):
    self.dispatcher.put(message)
    
  def reset(self):
    print 'Resetting Robot'
    self.send_packet('SOFTWARE_RESET')
      
  def set_pid_gains(self, gains):
    print 'Setting Gains'
    self.send_packet('SET_PID_GAINS',pack('10h',*gains))
            
  def set_thrust_closed_loop(self, thrust):
    print 'Setting Thrust'
    self.send_packet('SET_THRUST_CLOSED_LOOP',pack('5h',*thrust))
    
  def proceed(self):
    print 'Running experiment'
    self.count = int(self.duration/1000.0 * 300)
    self.last_time = time.time()
    #self.send_packet('ZERO_POS')
    if self.telemetry:
      self.send_packet('ERASE_SECTORS', pack('h',0))
      print "started erase, 3 second dwell"
      time.sleep(3)
      start = 0   # two byte start time to record
      skip = 0    # store every other sample if = 1
      temp=[self.count,start,skip]
      print 'telem command =',temp,'\n'
      self.send_packet('START_TELEM', pack('3h',*temp))
    self.set_thrust_closed_loop([0, self.duration, 0, self.duration, 0])

  def flash_readback(self):
    print "Starting readback",self.count
    self.send_packet('FLASH_READBACK', pack('=h',self.count))
  
  def expected_speed(self):
    if (time.time()-self.last_time) < (self.duration/1000.0):
      return 1000.0/self.cycle
    else:
      return 0.0