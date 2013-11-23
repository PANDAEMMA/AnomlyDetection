import  wx
from ComicMap import *

class ComicMapWindow(wx.ScrolledWindow):
    def __init__(self, parent, id = -1, size = wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)

        self.maxWidth  = 1000
        self.maxHeight = 1000
        self.x = self.y = 0

        self.SetBackgroundColour("WHITE")

        self.SetVirtualSize((self.maxWidth, self.maxHeight))
        self.SetScrollRate(20,20)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
        
        #layout
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
    def AddComicMap(self, id, data):
        self.sizer.Clear(True)
        self.comicMap = ComicMap(self, id, data)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.comicMap, 0, wx.LEFT, 10)
        self.Layout()
        self.comicMapAddedBefore = True


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


## This is an example of what to do for the EVT_MOUSEWHEEL event,
## but since wx.ScrolledWindow does this already it's not
## necessary to do it ourselves. You would need to add an event table 
## entry to __init__() to direct wheelmouse events to this handler.

##     wheelScroll = 0
##     def OnWheel(self, evt):
##         delta = evt.GetWheelDelta()
##         rot = evt.GetWheelRotation()
##         linesPer = evt.GetLinesPerAction()
##         print delta, rot, linesPer
##         ws = self.wheelScroll
##         ws = ws + rot
##         lines = ws / delta
##         ws = ws - lines * delta
##         self.wheelScroll = ws
##         if lines != 0:
##             lines = lines * linesPer
##             vsx, vsy = self.GetViewStart()
##             scrollTo = vsy - lines
##             self.Scroll(-1, scrollTo)

