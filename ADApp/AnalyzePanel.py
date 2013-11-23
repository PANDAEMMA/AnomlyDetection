import wx
from TimelineWindow import *
from ComicMapWindow import *

class AnalyzePanel(wx.Panel):
    def __init__(self,parent,id):
        wx.Panel.__init__(self,parent,id=id,style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        self.comicMapAddedBefore = False
        
        # Layout
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.comicMapWindow = ComicMapWindow(self, 900)
        self.sizer.Add(self.comicMapWindow, 1, wx.EXPAND)
        self.timeline = TimelineWindow(self, 901)
        self.sizer.Add(self.timeline, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT |wx.EXPAND)
        self.Layout()
        
    def AddComicMap(self, id, data):
        self.comicMapWindow.AddComicMap(id, data)
        
    def AddTimeline(self, id, data):
        self.timeline.OnGetData(data)
        
    def UpdateTimeline(self, ids):
        self.timeline.OnMask(ids)
        
    def OnZoom(self, zoom):
        #self.sizer.Clear()
        self.comicMap.OnZoom(zoom)
        #self.sizer.AddSpacer(10)
        #self.sizer.Add(self.comicMap, 0, wx.LEFT, 10)
        #self.sizer.AddSpacer(10)
        #self.sizer.Add(self.timeline, 0, wx.LEFT, 10)
        #self.Layout()
        