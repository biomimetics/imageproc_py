import NatNet
import time
import threading, Queue
from asynch_dispatch import *


class OptitrakStream(threading.Thread):
	def __init__(self, sinks=None, autoStart=True):
		threading.Thread.__init__(self)
		self.daemon = True
    
		self.c = NatNet.NatNetClient(1)
		print self.c.NatNetVersion()

		self.c.SetVerbosityLevel(NatNet.Verbosity_Info)

		self.c.Initialize("127.0.0.1", "127.0.0.1")
		
		self.dispatcher=AsynchDispatch(sinks=sinks)
		self.recieve_queue = Queue.Queue()
		self.input_data = ''

		self.c.SetDataCallback(self.get_Net_Callback)
		
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
      
	def put(self, data):
		self.dispatcher.put(message)

	def add_sinks(self,sinks):
		self.dispatcher.add_sinks(sinks)

	#gets data from the optitrak stream
	def get_Net_Callback(self, dataFrame):
		body = dataFrame.RigidBodies[0]
		#comment out and delete all body2 from self.input_data if only tracking 1 body
		body2 = dataFrame.RigidBodies[1]
#		body3 = dataFrame.RigidBodies[2]
#		"x %.2f  y %.2f  z %.2f  qx %.4f  qy %.4f  qz %.4f qw %.4f x2 %.2f y2 %.2f z2 %.2f" %
		self.input_data = [body.x, body.y, body.z, body.qx, body.qy, body.qz, body.qw,
											body2.x, body2.y, body2.z]

	#sends the most current data when called by virtual.py
	def get_optitrak_position(self):
		self.dispatcher.dispatch(Message('optitrak_data', self.input_data))
		