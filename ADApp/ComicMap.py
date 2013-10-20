import wx
import math
import sys
from PlotWindow import *

class ComicMap(wx.Panel):
    def __init__(self, parent, id, data, nInRow = 3):
        wx.Panel.__init__(self, parent, id=id, style=wx.NO_BORDER)
        
        self.plots =[]
        self.window_init_id = 1000
        i = 0
        while (i<len(data)):
            self.plots.append(PlotWindow(self, self.window_init_id+i, data=data[i], maxH=0, maxW=0))
            i=i+1

        sizer = wx.GridSizer(rows=math.ceil(float(len(data))/nInRow))
        for plot in self.plots:
            sizer.Add(plot, 0, 0)
        self.SetSizer(sizer)
        self.Fit()
        
        