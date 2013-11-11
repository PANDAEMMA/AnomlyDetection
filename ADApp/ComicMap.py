import wx
import math
import sys

from PlotWindow import *

class ComicMap(wx.Panel):
    def __init__(self, parent, id, data):
        wx.Panel.__init__(self, parent, id=id, style=wx.NO_BORDER)
        self.data = data
        self.plots =[]
        self.dragTarget = 0
        self.window_init_id = 1000
        self.plotSize = 150
        self.scale = 1
        i = 0
        while (i<len(data)):
            self.plots.append(PlotWindow(self, self.window_init_id+i, data=data[i]))
            i=i+1
        self.nInRow = math.sqrt(len(data))
        self.sizer = wx.GridSizer(rows=math.ceil(float(len(data))/self.nInRow))
        for plot in self.plots:
            self.sizer.Add(plot, 0, 0)
        self.SetSizer(self.sizer)
        self.Fit()
        
    def UpdateDragTarget(self, target):
        self.dragTarget = target
        
    def OnGridChange(self, source, target):
        self.effect = self.GetTopLevelParent().GridEffect
        if (self.effect == "swap"):
            self.Swap(source, target)
        if(self.effect == "merge"):
            self.Merge(source, target)
        
    def Swap(self, source, target):
        sourceDataID = self.plots[source].dataID
        targetDataID = self.plots[target].dataID
        self.plots[source].ReDraw(targetDataID, self.data[targetDataID])
        self.plots[target].ReDraw(sourceDataID, self.data[sourceDataID])
        
    def Merge(self, source, target):
        print "in merge"
        sourceDataID = self.plots[source].dataID
        targetDataID = self.plots[target].dataID
        i = 0;
        while (i<len(self.data[sourceDataID])):
            self.data[targetDataID].append(self.data[sourceDataID][i])
            i=i+1
        self.plots[source].ReDraw(sourceDataID, self.data[sourceDataID])
        self.plots[target].ReDraw(targetDataID, self.data[targetDataID])
        
    def OnZoom(self, zoom):
        if zoom == "in":
            self.plotSize = self.plotSize+10
        if zoom == "out":
            self.plotSize = self.plotSize-10
        i=0
        self.newSizer =  wx.GridSizer(rows=math.ceil(float(len(self.data))/self.nInRow))
        while (i<len(self.plots)):
            self.plots[i].SetSize((self.plotSize,self.plotSize))
            i=i+1
        for plot in self.plots:
            self.newSizer.Add(plot, 0, 0)
        self.SetSizer(self.newSizer)
        self.Fit()
        
        
        