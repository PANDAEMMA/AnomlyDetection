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
        self.GetMax(data)
        i = 0
        while (i<len(data)):
            self.plots.append(PlotWindow(self, self.window_init_id+i, data=data[i]))
            i=i+1
        self.col = 3
        self.row=math.ceil(float(len(data))/self.col)
        self.sizer = wx.GridSizer(self.row,self.col)
        for plot in self.plots:
            self.sizer.Add(plot, 0, 0)
        self.SetSizer(self.sizer)
        self.Fit()
        
    def GetMax(self, data):
        self.maxH = self.maxW = 0
        self.FindMaxHW(data)
        
    def FindMaxHW(self, allData):
        for list in allData:
            for l in list:
                c = l['points']
                for point in c:
                    if point[1]>self.maxH and point[0]>self.maxW:
                        self.maxH = point[1]
                        self.maxW = point[0]
                    elif point[0]>self.maxW:
                        self.maxW = point[0]
                    elif point[1]>self.maxH:
                        self.maxH = point[1]
                    else:
                        continue
                
        self.maxH = self.maxH+5
        self.maxW = self.maxW+5
        
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
        sourceData = []
        targetData = []
        for s in range(len(sourceDataID)):
            sourceData = sourceData + self.data[sourceDataID[s]]
        for t in range(len(targetDataID)):
            targetData = targetData + self.data[targetDataID[t]]
        self.plots[source].ReDraw(targetDataID, targetData)
        self.plots[target].ReDraw(sourceDataID, sourceData)
        
    def Merge(self, source, target):
        if source == target:
            return
        else:
            sourceDataID = self.plots[source].dataID
            targetDataID = self.plots[target].dataID
            targetDataID = targetDataID+sourceDataID
            sourceData = []
            targetData = []
            for s in range(len(sourceDataID)):
                sourceData = sourceData + self.data[sourceDataID[s]]
            for t in range(len(targetDataID)):
                targetData = targetData + self.data[targetDataID[t]]
            self.plots[source].ReDraw(sourceDataID, sourceData)
            self.plots[target].ReDraw(targetDataID, targetData)
        
    def UpdateClick(self, id):
        i = 0
        while (i<len(self.plots)):
            if i == id:
                self.plots[i].UpdateClicke(True)
            else:
                self.plots[i].UpdateClicke(False)
            i=i+1
        self.GetParent().GetParent().UpdateTimeline(self.plots[id].dataID)
        
    def GetDataByIDs(self, ids):
        data = []
        for i in range(len(ids)):
            data = data + self.data[ids[i]]
        return data
        
        
        
        