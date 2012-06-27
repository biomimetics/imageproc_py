import wx

class BarGraphPanel(wx.Panel):
  def __init__(self, parent, dataLabel='', sensorRange=(0.0,1.0)):
    wx.Panel.__init__(self, parent)
    
    self.label = wx.StaticText(self,-1,label=dataLabel)
    self.value = wx.StaticText(self,-1,label='0.0')
    self.bar = BarGraph(self, sensorRange)
    self.bar.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
    
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    
    self.sizer.Add(self.label,0,wx.GROW)
    self.sizer.Add(self.bar,1,wx.GROW)
    self.sizer.Add(self.value,0,wx.GROW)
    
    self.SetSizer(self.sizer)
    self.SetAutoLayout(1)
    self.sizer.Fit(self)
    
  def update(self, value):
    self.value.SetLabel('%.2f' % value)
    self.bar.update(value)
    self.Refresh(False)

class BarGraph(wx.Panel):
  def __init__(self, parent, sensorRange):
    wx.Panel.__init__(self, parent,size=(50,300))
    
    self.sensorRange = sensorRange
    self.sensorVal = 0.0
    
    self.Bind(wx.EVT_PAINT, self.on_paint)
    self.Bind(wx.EVT_SIZE, self.resize)
  
  def update(self,value):
    self.sensorVal = value
    self.Refresh(False)
  
  def resize(self,event):
    self.Refresh(False)
    
  def on_paint(self, event):
    dc = wx.AutoBufferedPaintDC(self)
    
    dc.Clear()
    
    w,h = dc.GetSize()
    
    if self.sensorVal < self.sensorRange[0]:
      sensorScale = 0.0
    elif self.sensorVal > self.sensorRange[1]:
      sensorScale = 1.0
    else:
      sensorScale = (self.sensorVal-self.sensorRange[0])/(self.sensorRange[1]-self.sensorRange[0])
    
    dc.SetBrush(wx.Brush('black'))
    dc.DrawRectangle(10,10,w-20,h-20)
    dc.SetBrush(wx.Brush('red'))
    dc.DrawRectangle(12,12+int((h-30)*(1-sensorScale)),w-24,6+int((h-30)*sensorScale))