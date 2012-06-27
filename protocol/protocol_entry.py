class ProtocolEntry():
  def __init__(self, name, value, dataFormat=None, stringFormat=None):
    self.name = name
    self.value = value
    self.dataFormat = dataFormat
    self.stringFormat = stringFormat
  
  def __str__(self):
    return '%s (%02X)' % (self.name, self.value)
    
  def parseData(self, data):
    if self.dataFormat is not None:
      return unpack(self.dataFormat, data)
    else:
      return data
  
  def formatData(self, data):
    if self.stringFormat is not None:
      data_string = self.stringFormat % self.parseData(data)
    else:
      data_string = self.parseData(data).__str__()
      
    return '%s:%s' % (self.name, data_string)