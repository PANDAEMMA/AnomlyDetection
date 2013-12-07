import  wx
import  wx.lib.scrolledpanel as scrolled
from ComicMap import *

class ComicMapWindow(scrolled.ScrolledPanel):
    def __init__(self, parent, id = -1, size = wx.DefaultSize):
        scrolled.ScrolledPanel.__init__(self, parent, id, (0, 0), size=size)
        self.SetBackgroundColour("WHITE")
        #layout
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        
    def AddComicMap(self, id, data):
        self.sizer.Clear(True)
        self.comicMap = ComicMap(self, id, data)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.comicMap, 0, wx.LEFT, 10)
        self.Layout()
        self.FitInside()


    def getWidth(self):
        return self.maxWidth

    def getHeight(self):
        return self.maxHeight

        dc.SetPen(wx.Pen('MEDIUM FOREST GREEN', 4))

        for line in self.lines:
            for coords in line:
                apply(dc.DrawLine, coords)


    def SetXY(self, event):
        self.x, self.y = self.ConvertEventCoords(event)

    def ConvertEventCoords(self, event):
        newpos = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        return newpos

    def OnLeftButtonEvent(self, event):
        if event.LeftDown():
            self.SetFocus()
            self.SetXY(event)



