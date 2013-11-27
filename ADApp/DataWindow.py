import wx
import math
import random
import os

class DataWindow(wx.Frame):

    def __init__(self,parent,id):
        wx.Frame.__init__(self, parent, id, 'Data', size=(550,530))
        wx.Frame.CenterOnScreen(self)
        CONTENT_ID = wx.NewId()
        self.content = DataContent(self, CONTENT_ID, None)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.content, 0, wx.EXPAND)
        #self.new.Show(False)
        
        
class DataContent(wx.Window):
    def __init__(self, parent, id, data):
        wx.Window.__init__(self, parent, id=id)
        self.SetBackgroundColour(wx.WHITE)
        self.SetSize((550,510))
        self.rect = self.GetClientRect()
        self.zeroX = self.rect.x
        self.zeroY = self.rect.y
        self.width = self.rect.width
        self.height = self.rect.height
        self.eColor = wx.Colour(255, 50, 50)
        self.gColor = wx.Colour(50,255,50)
        self.mColor = wx.Colour(50, 50, 255)
        self.scale = 30
        self.num = 17
        self.offset = 50
        #self.addPng = wx.Image(self.opj('add.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
	self.addPng = wx.Bitmap('add.png')
        self.minusPng = wx.Image(self.opj('minus.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, event):
        pdc = wx.PaintDC(self)
        dc = wx.GCDC(pdc)
        self.DrawDivide(dc)
        self.DrawPercent(dc)
        self.DrawLabel(dc, ['1997', '1998', '1999','2000','2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013'])
        self.DrawButton(dc)
        
    def DrawButton(self, dc):
        for i in range(self.num):
	    dc = wx.PaintDC(self)
            dc.SetBackground(wx.Brush("WHITE"))
	    dc.DrawBitmap(self.addPng, 0, 10, useMask=False)
            #wx.StaticBitmap(self, -1, self.addPng, (10, 10), (20, 20))
    
    def DrawDivide(self, dc):
        dc.SetPen(wx.BLACK_PEN)
        for i in range(self.num):
            dc.DrawLine(self.zeroX, self.zeroY+self.scale*i,self.zeroX+self.width, self.zeroY+self.scale*i)
            
    def DrawPercent(self, dc):
        for i in range(self.num):
            if i == 2:
                self.DrawMonth(dc, i)
            elif i == 0:
                self.DrawMonth(dc, i)
            else:
                dc.SetPen(wx.Pen(self.eColor))
                dc.SetBrush( wx.Brush(self.eColor) )
                e = random.randint(25,40)
                dc.DrawRectangle(self.zeroX+self.offset, self.zeroY+self.scale*i+1, e, self.scale-1)
                dc.SetPen(wx.Pen(self.gColor))
                dc.SetBrush( wx.Brush(self.gColor) )
                g = random.randint(5,25)
                dc.DrawRectangle(self.zeroX+self.offset+e, self.zeroY+self.scale*i+1, g, self.scale-1)
                dc.SetPen(wx.Pen(self.mColor))
                dc.SetBrush( wx.Brush(self.mColor) )
                m = random.randint(25,50)
                dc.DrawRectangle(self.zeroX+self.offset+e+g, self.zeroY+self.scale*i+1, m, self.scale-1)
            
    def DrawLabel(self, dc, data):
        self.labelFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)
        dc.SetFont(self.labelFont)
        dc.SetPen(wx.BLACK_PEN)
        for i in range(len(data)):
            labelText = data[i]
            tw, th = dc.GetTextExtent(labelText)
            pos = (self.width-tw-5, self.zeroY+self.scale*i+5)
            dc.DrawText(labelText, pos[0], pos[1])
            
    def DrawMonth(self,dc, i):
        entryW = self.width/float(12)
        for j in range(12):
            dc.SetPen(wx.Pen(self.eColor))
            dc.SetBrush( wx.Brush(self.eColor) )
            e = random.randint(25,40)/float(12)
            dc.DrawRectangle(self.zeroX+self.offset+entryW*j, self.zeroY+self.scale*i+1, e, self.scale-1)
            dc.SetPen(wx.Pen(self.gColor))
            dc.SetBrush( wx.Brush(self.gColor) )
            g = random.randint(5,25)/float(12)
            dc.DrawRectangle(self.zeroX+self.offset+entryW*j+e, self.zeroY+self.scale*i+1, g, self.scale-1)
            dc.SetPen(wx.Pen(self.mColor))
            dc.SetBrush( wx.Brush(self.mColor) )
            m = random.randint(25,50)/float(12)
            dc.DrawRectangle(self.zeroX+self.offset+entryW*j+e+g, self.zeroY+self.scale*i+1, m, self.scale-1)
            if not j==0:
                dc.SetPen(wx.BLACK_PEN)
                dc.DrawLine(self.zeroX+self.offset+entryW*j, self.zeroY+self.scale*i,self.zeroX+self.offset+entryW*j, self.zeroY+self.scale*i+self.scale)
            
    
    def opj(self, path):
        """Convert paths to the platform-specific separator"""
        st = apply(os.path.join, tuple(path.split('/')))
        # HACK: on Linux, a leading / gets lost...
        if path.startswith('/'):
            st = '/' + st
        return st        
    
        
