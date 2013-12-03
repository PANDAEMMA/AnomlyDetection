import wx
import math
import random
import os

from ADAnRecordLabel import *
from ADParse import *
from ADFrame import *
from DataPanel import *

class DataWindow(wx.Frame):

    def __init__(self,parent,id, File):
        wx.Frame.__init__(self, parent, id, 'Data', size=(550,630))
        wx.Frame.CenterOnScreen(self)
        CONTENT_ID = wx.NewId()
        self.content = DataContent(self, CONTENT_ID, None, File)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.content, 0, wx.EXPAND)
        
class DataContent(wx.Window):
    def __init__(self, parent, id, data, File):
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
        self.offset = 100
        # Layout
        self.File = File
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Show(True)

    def OnPaint(self, event):
        pdc = wx.PaintDC(self)
        dc = wx.GCDC(pdc)
        #self.DrawDivide(dc)

        #self.DrawLabel(dc, ['1997', '1998', '1999','2000','2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013'])
        # Get the number of year
        year = get_year(self.File, YEAR)
        length = len(year)
        self.DrawPercent(dc, length)
        self.DrawLabel(dc, year)
        self.DrawDivide(dc, length)
        # Draw out annual statistic
        for i in range(length):
            self.Bind(wx.EVT_BUTTON, self.doMe, self.DrawButton_add((int)(year[i]),i))
            self.Bind(wx.EVT_BUTTON, self.doMe, self.DrawButton_min(((int)(year[i])-1997)*ZOOM_OUT,i))
            self.Bind(wx.EVT_BUTTON, self.doMe, self.DrawButton_check(((int)(year[i]) -1997)*CHECK,i))

        
    def DrawButton_min(self, id, y_axis):
	self.image2 = wx.Image("minus.ico", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.button2 = wx.BitmapButton(self, id, bitmap=self.image2,
        pos=(self.image2.GetWidth(), y_axis*self.image2.GetHeight()), size = (self.image2.GetWidth(), self.image2.GetHeight()))
	self.button2.SetDefault()

    def DrawButton_check(self, id, y_axis):
	self.image3 = wx.Image("check.ico", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.button3 = wx.BitmapButton(self, id, bitmap=self.image3,
        pos=(2 * self.image3.GetWidth(), y_axis*self.image3.GetHeight()), size = (self.image3.GetWidth(), self.image3.GetHeight()))
	self.button3.SetDefault()

    def DrawButton_add(self, id, y_axis):
	self.image1 = wx.Image("add.ico", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.button1 = wx.BitmapButton(self, id, bitmap=self.image1,
        pos=(0, y_axis*self.image1.GetHeight()), size = (self.image1.GetWidth(), self.image1.GetHeight()))
	self.button1.SetDefault()

    def doMe(self, event):
	id_n = event.GetId()
	if ((id_n % CHECK) == 0):
		year = (id_n / CHECK) + 1997
		fd = open(self.File, 'r')
		fd1 = open(self.File+'.tmp', 'w+')
		for line in fd.readlines():
			a = re.split(',|\n| ', line)
			if((int)(a[YEAR]) == year):
				fd1.write(line)
		fd.close()
		fd1.close()
        self.GetParent().GetParent().DoneRegionSel([])
	#self.Destroy() # test

    def DrawDivide(self, dc, year):
        dc.SetPen(wx.BLACK_PEN)
        for i in range(year + 1):
            dc.DrawLine(self.zeroX, self.zeroY+self.scale*i,self.zeroX+self.width, self.zeroY+self.scale*i)
            
    def DrawPercent(self, dc, length):
	aa = normal_stat(self.File, YEAR, TEMPER)
	miss_data = [item[0] for item in aa]
	max_data = [item[1] for item in aa]
	min_data = [item[2] for item in aa]
        for i in range(length):
                dc.SetPen(wx.Pen(self.eColor))
                dc.SetBrush( wx.Brush(self.eColor) )
       #         e = random.randint(25,40)
                dc.DrawRectangle(self.zeroX+self.offset, self.zeroY+self.scale*i+1, miss_data[i] * self.width, self.scale-1)
                dc.SetPen(wx.Pen(self.gColor))
                dc.SetBrush( wx.Brush(self.gColor) )
         #       g = random.randint(5,25)
                dc.DrawRectangle(self.zeroX+self.offset+ (miss_data[i] * self.width), self.zeroY+self.scale*i+1, max_data[i] * self.width, self.scale-1)
                dc.SetPen(wx.Pen(self.mColor))
                dc.SetBrush( wx.Brush(self.mColor) )
       #         m = random.randint(25,50)
                dc.DrawRectangle(self.zeroX+self.offset+((miss_data[i] + max_data[i]) * self.width), self.zeroY+self.scale*i+1, min_data[i] * self.width, self.scale-1)
            
    def DrawLabel(self, dc, data):
        self.labelFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
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
    
        
