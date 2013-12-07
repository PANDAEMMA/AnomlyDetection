import wx
import math
import random
import os

from ADAnRecordLabel import *
from ADParse import *
from ADFrame import *
from DataPanel import *

class DataWindow(wx.Frame):
    def __init__(self,parent,id, data):
        wx.Frame.__init__(self, parent, id, 'Data', size=(550,630))
        wx.Frame.CenterOnScreen(self)
        CONTENT_ID = wx.NewId()
        self.content = DataContent(self, CONTENT_ID, data)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.content, 0, wx.EXPAND)
        
class DataContent(wx.Window):
    def __init__(self, parent, id, data):
        wx.Window.__init__(self, parent, id=id)
        self.SetBackgroundColour(wx.WHITE)
        self.SetSize((550,610))
        self.rect = self.GetClientRect()
        self.zeroX = self.rect.x
        self.zeroY = self.rect.y
        self.width = self.rect.width
        self.height = self.rect.height
        self.eColor = wx.Colour(255, 50, 50)
        self.gColor = wx.Colour(50,255,50)
        self.mColor = wx.Colour(50, 50, 255)
        self.scale = 32
        self.num = 2
        self.offset = 32
        self.data = data
        self.ParseData()
        
        # Layout
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        self.Show(True)
        
    def ParseData(self):
        self.num = len(self.data)
        self.yw = self.width-self.offset
        self.mw = self.yw/float(12)
        self.labels = []
        self.buttons = []
        self.buttonPos = []
        self.yearRegion = []
        self.monthRegion = []
        self.yearData = []
        self.monthData = []
        for i in range(len(self.data)):
            self.labels.append(str(self.data[i]['year']))
            self.buttons.append('year')
            self.yearData.append(self.data[i]['year_data'])
            self.monthData.append(self.data[i]['month_data'])
            self.yearRegion.append(wx.Rect(self.zeroX+self.offset,self.zeroY+self.scale*i+1,self.width-self.offset,self.scale))
            self.monthRegionYear = []
            for j in range(12):
                self.monthRegionYear.append(wx.Rect(self.zeroX+self.offset+self.mw*j, self.zeroY+self.scale*i+1, self.mw, self.scale))
            self.monthRegion.append(self.monthRegionYear)
            self.buttonPos.append(wx.Rect(self.zeroX+3, self.zeroY+self.scale*i+3, 26, 26))

    def OnPaint(self, event):
        pdc = wx.PaintDC(self)
        dc = wx.GCDC(pdc)
        self.DrawPercent(dc, self.yearData, self.monthData, self.buttons)
        self.DrawDivide(dc, self.num)
        self.DrawLabel(dc,self.labels)
        self.DrawButtons(dc, self.buttons, self.buttonPos)
        
    def DrawButtons(self, dc, buttonInfo, buttonPos):
        for i in range(len(buttonInfo)):
            if buttonInfo[i] == 'year':
                self.DrawButton(dc, buttonPos[i], 1)
            else:
                self.DrawButton(dc, buttonPos[i], 0)
            
    def DrawButton(self, dc, posRect, type):
        dc.SetPen(wx.Pen(wx.BLACK, 2))
        dc.SetBrush(wx.WHITE_BRUSH)
        center = (posRect.x+float(posRect.width)/2, posRect.y+float(posRect.height)/2)
        radius = (posRect.width)/2
        len = radius-8
        dc.DrawCircle(center[0], center[1], radius)
        dc.DrawLine(center[0]-len, center[1],center[0]+len, center[1])
        if type == 1:
            dc.DrawLine(center[0], center[1]-len,center[0], center[1]+len)

    def DrawDivide(self, dc, len):
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        for i in range(len + 1):
            dc.DrawLine(self.zeroX, self.zeroY+self.scale*i,self.zeroX+self.width, self.zeroY+self.scale*i)
            
    def DrawLabel(self, dc, data):
        self.labelFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        dc.SetFont(self.labelFont)
        dc.SetPen(wx.BLACK_PEN)
        for i in range(len(data)):
            labelText = data[i]
            tw, th = dc.GetTextExtent(labelText)
            pos = (self.width-tw-5, self.zeroY+self.scale*i+5)
            dc.DrawText(labelText, pos[0], pos[1])
            
    def DrawPercent(self, dc, yeardata, monthdata, buttons):
        for i in range(len(buttons)):
            if buttons[i] == 'year':
                self.DrawYear(dc, i, yeardata[i])
            else:
                self.DrawMonth(dc, i, monthdata[i])
                
    def DrawYear(self, dc, i, data):
        dc.SetPen(wx.Pen(self.eColor))
        dc.SetBrush( wx.Brush(self.eColor))
        dc.DrawRectangle(self.zeroX+self.offset, self.zeroY+self.scale*i+1, data[0]*self.yw, self.scale-1)
        dc.SetPen(wx.Pen(self.gColor))
        dc.SetBrush( wx.Brush(self.gColor) )
        dc.DrawRectangle(self.zeroX+self.offset+ data[0]*self.yw, self.zeroY+self.scale*i+1, data[1]*self.yw, self.scale-1)
        dc.SetPen(wx.Pen(self.mColor))
        dc.SetBrush( wx.Brush(self.mColor) )
        dc.DrawRectangle(self.zeroX+self.offset+((data[0] + data[1])*self.yw), self.zeroY+self.scale*i+1, data[2]*self.yw, self.scale-1)
            
    def DrawMonth(self,dc, i, data):
        for j in range(12):
            md = data[j]
            dc.SetPen(wx.Pen(self.eColor))
            dc.SetBrush( wx.Brush(self.eColor) )
            dc.DrawRectangle(self.zeroX+self.offset+self.mw*j, self.zeroY+self.scale*i+1, md[0]*self.mw, self.scale-1)
            dc.SetPen(wx.Pen(self.gColor))
            dc.SetBrush( wx.Brush(self.gColor) )
            dc.DrawRectangle(self.zeroX+self.offset+self.mw*j+md[0]*self.mw, self.zeroY+self.scale*i+1, md[1]*self.mw, self.scale-1)
            dc.SetPen(wx.Pen(self.mColor))
            dc.SetBrush( wx.Brush(self.mColor) )
            dc.DrawRectangle(self.zeroX+self.offset+self.mw*j+((md[0]+md[1])*self.mw), self.zeroY+self.scale*i+1, md[2]*self.mw, self.scale-1)
            if not j==0:
                dc.SetPen(wx.BLACK_PEN)
                dc.DrawLine(self.zeroX+self.offset+self.mw*j, self.zeroY+self.scale*i,self.zeroX+self.offset+self.mw*j, self.zeroY+self.scale*i+self.scale)
            #draw month label
            self.labelFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            dc.SetFont(self.labelFont)
            dc.SetPen(wx.BLACK_PEN)
            labelText = str(j+1)
            tw, th = dc.GetTextExtent(labelText)
            pos = (self.zeroX+self.offset+self.mw*j+1, self.zeroY+self.scale*(i+1)-th)
            dc.DrawText(labelText, pos[0], pos[1])
    
    def InRegion(self, x, y, bRect):
        if x>bRect.x and x<bRect.x+bRect.width and y>bRect.y and y<bRect.y+bRect.height:
            return True
        else:
            return False
    
    def OnClick(self, event):
        x, y = event.GetPositionTuple()
        for i in range(len(self.buttonPos)):
            if self.InRegion(x, y, self.buttonPos[i]):
                if self.buttons[i] == "year":
                    self.buttons[i] = "month"
                elif self.buttons[i] == "month":
                    self.buttons[i] = "year"
                self.Refresh()
    
    def OnDoubleClick(self, event):
        x, y = event.GetPositionTuple()
        for i in range(len(self.buttons)):
            if self.buttons[i] == "year":
                if self.InRegion(x, y, self.yearRegion[i]):
                    print (int(float(self.labels[i])), -1)
                    return True
            else:
                for j in range(len(self.monthRegion[i])):
                    if self.InRegion(x, y, self.monthRegion[i][j]):
                        print (int(float(self.labels[i])), j+1)
                        return True