import wx
from ComicMap import *
from TimelineWindow import *

class AnalyzePanel(wx.Panel):
    def __init__(self,parent,id):
        wx.Panel.__init__(self,parent,id=id,style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        
        # Layout
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
    def AddComicMap(self, id, data):
        self.comicMap = ComicMap(self, id, data)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.comicMap, 0, wx.LEFT, 10)
        self.Layout()
        
    def AddTimeline(self, id, data):
        self.timeline = TimelineWindow(self, id, data)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.timeline, 0, wx.LEFT, 10)
        self.Layout()
        
    def OnZoom(self, zoom):
        #self.sizer.Clear()
        self.comicMap.OnZoom(zoom)
        #self.sizer.AddSpacer(10)
        #self.sizer.Add(self.comicMap, 0, wx.LEFT, 10)
        #self.sizer.AddSpacer(10)
        #self.sizer.Add(self.timeline, 0, wx.LEFT, 10)
        #self.Layout()
        