from struct import unpack
from standard_protocol import STANDARD_PROTOCOL
from protocol_entry import ProtocolEntry

class Protocol():
  def __init__(self, entries=STANDARD_PROTOCOL):
    self.names = {}
    self.values = {}
    
    for e in entries:
      self.names[e.name] = e
      self.values[e.value] = e
  
  def add(self,entry):
    self.names[entry.name] = entry
    self.values[entry.value] = entry
    
  def find(self,key):
    try:
      if type(key) is int:
        return self.values[key]
      elif type(key) is str:
        return self.names[key]
    except KeyError:
      print 'Protocol entry not found for \"%s\"' % key.__str__()
      return None
      
  def parseData(self,key,data):
    entry = self.find(key)
    if entry is not None:
      return entry.parseData(data)
    
  def formatData(self,key,data):
    entry = self.find(key)
    if entry is not None:
      return entry.formatData(data)