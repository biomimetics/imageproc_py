import threading
import wx

class GUI_Stream(threading.Thread):
  def __init__(self, frameClass=None, panelClass=None, title='', autoStart=True):
    threading.Thread.__init__(self)
    self.daemon = True
    
    if panelClass is None:
      self.panelClass = wx.Panel
    else:
      self.panelClass = panelClass
    
    self.frameClass = frameClass
    
    self.title = title
    
    if autoStart:
      self.start()
      
  def run(self):
    self.app = wx.App(False)
    if self.frameClass is not None:
      self.frame = self.frameClass()
    else:
      self.frame = ThreadedFrame(self.title, self.panelClass)
    self.app.MainLoop()
    
class ThreadedFrame(wx.Frame):
  def __init__(self, title, panelClass):
    wx.Frame.__init__(self, None, title=title)
    
    self.mainPanel = panelClass(self)
    self.Fit()
    self.Show(True)