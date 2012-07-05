from struct import pack, unpack
from protocol import Protocol

class Packet():
  def __init__(self, pkt_type=255, data='', status=0, dest_addr=-1, time=-1, payload=None, protocol=Protocol()):
  
    self.dest_addr = dest_addr
    self.time = time
    
    if payload is not None:
      self.payload = payload
      self.pkt_type = ord(payload[0])
      self.entry = protocol.find(self.pkt_type)
      self.status = ord(payload[1])
      self.data = payload[2:]
    else:
      
      if type(pkt_type) is int:
        self.pkt_type = pkt_type
        self.entry = protocol.find(pkt_type)
      else:
        self.entry = protocol.find(pkt_type)
        if self.entry is not None:
          self.pkt_type = self.entry.value
        else:
          print 'Packet type \"%s\" not found' % pkt_type.__str__()
          self.pkt_type = -1
    
      self.payload = chr(status) + chr(self.pkt_type) + ''.join(data)
      
      self.status = status
      self.data = data
      
    if self.entry is not None:
      self.data_str = self.entry.formatData(self.data)
    else:
      self.data_str = self.data.encode('hex')
        
  def __str__(self):
    return '@ 0x%04X: S:%d T:0x%02X D:%s' % \
        (self.dest_addr, self.status, self.pkt_type, self.data_str)
