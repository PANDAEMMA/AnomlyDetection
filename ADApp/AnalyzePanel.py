import wx
from ComicMap import *

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