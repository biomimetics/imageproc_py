import threading
import Queue

class Message():
  def __init__(self, msg_type=None, data=None):
    if type(msg_type) is tuple:
      self.type = msg_type[0]
      self.data = msg_type[1]
    else:
      self.type = msg_type
      self.data = data
    
  def __str__(self):
    return '%s: %s' % (self.type.__str__(), self.data.__str__())
    
class AsynchDispatch(threading.Thread):
  def __init__(self, callbacks=None, sinks=None, autoStart=True):
    threading.Thread.__init__(self)
    self.daemon = True
    
    self.new_data = threading.Condition()
    
    self.in_queue = Queue.Queue()
    
    if callbacks is not None:
      self.callbacks = callbacks
    else:
      self.callbacks = {}
      
    if sinks is not None:
      self.sinks = sinks
    else:
      self.sinks = {}
    
    if autoStart:
      self.start()
      
  def run(self):
    while(True):
      # Atomically empty message entries from in_queue
      self.new_data.acquire()
      self.new_data.wait()
      
      messages = []
      while not self.in_queue.empty():
        messages.append(self.in_queue.get())
        
      self.new_data.release()      
      
      # Send data through callbacks
      for message in messages:
        if message.type in self.callbacks.keys():
          for callback in self.callbacks[message.type]:
            callback(message)
        elif None in self.callbacks.keys():
          for callback in self.callbacks[None]:
            callback(message)
            
  def put(self, messages):
    # Atomically add messages to in_queue and signal that there is new data
    self.new_data.acquire()
    
    for message in self.to_message_list(messages):
      self.in_queue.put(message)
        
    self.new_data.notify()
    self.new_data.release()
  
  def to_message_list(self, messages):
    messages_out = []
    
    if type(messages) is not list:
      messages = [messages]
    
    for m_i in messages:
      if type(m_i) is tuple:
        messages_out.append(Message(m_i))
      else:
        messages_out.append(m_i)
    
    return messages_out
    
  def dispatch(self, messages):
    for message in self.to_message_list(messages):
      if message.type in self.sinks.keys():
        for sink in self.sinks[message.type]:
          sink(message)
    
  def add_callbacks(self, callback_map):
    for msg_type,callbacks in callback_map.items():
      if msg_type in self.callbacks.keys():
        self.callbacks[msg_type] += callbacks
      else:
        self.callbacks[msg_type] = callbacks
    
  def add_sinks(self, sink_map):
    for msg_type,sinks in sink_map.items():
      if msg_type in self.sinks.keys():
        self.sinks[msg_type] += sinks
      else:
        self.sinks[msg_type] = sinks