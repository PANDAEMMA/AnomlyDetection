import wx

#Data should be a dictionary
#dictionary is like {labels:[list], anomolies: [list]}

class TimelineWindow(wx.Window):
    def __init__(self, parent, id):
        wx.Window.__init__(self, parent, id=id, style=wx.SUNKEN_BORDER)
        self.id = id
        self.SetSize((600,60))
        self.radius = 3 #mark circle size
        self.SetBackgroundColour(wx.Colour(235,235,235))
        self.data = None
        self.maxW = self.minW = 0
        #draw in the middle
        self.midY = 30
        self.mask = False
        self.eColor = wx.Colour(255, 50, 50)
        self.gColor = wx.Colour(50,255,50)
        self.mColor = wx.Colour(50, 50, 255)
        self.maskColor = wx.Colour(255,255,0, 92 )
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    def FindBound(self):
        c = self.data['labels']
        for label in c:
            if  label[0]>self.maxW:
                self.maxW = label[0]
            elif label[0]<self.minW:
                self.minW = label[0]
            else:
                continue
                
        self.maxW = self.maxW+2
        self.minW = self.minW
        
    def GetProjectionData(self):
        self.rect = self.GetClientRect()
        self.midY = float(self.rect.height)/2
        self.zeroX = self.rect.x
        self.zeroY = self.rect.y
        self.FindBound()
        self.unitX = float(self.rect.width)/(self.maxW-self.minW)
        
    def OnGetData(self, data):
        self.data = data
        self.GetProjectionData()
        self.Refresh()
        
    def OnMask(self, ids):
        self.mask = True
        self.maskIDs = ids
        self.Refresh()
        
    def OnPaint(self, event):
        #init paint 
        pdc = wx.PaintDC(self)
        dc = wx.GCDC(pdc)
        if self.data is None:
            return 
        else:
            self.DrawLabel(dc)
            self.DrawAxis(dc)
            #draw data
            self.DrawData(self.data, dc)
            #draw mask
            if self.mask == True:
                self.DrawMask(dc)
                
    def DrawLabel(self, dc):
        self.labelFont = wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL)
        dc.SetFont(self.labelFont)
        dc.SetPen(wx.BLACK_PEN)
        labelText = "Extreme:"
        tw, th = dc.GetTextExtent(labelText)
        pos1 = (3, 3)
        dc.DrawText(labelText, pos1[0], pos1[1])
        dc.SetPen(wx.Pen(self.eColor))
        dc.SetBrush( wx.Brush(self.eColor) )
        dc.DrawCircle(pos1[0]+tw+5, 8, 3)
        dc.SetPen(wx.BLACK_PEN)
        labelText = "Glitch:"
        tw, th = dc.GetTextExtent(labelText)
        pos2 = (pos1[0]+50, 3)
        dc.DrawText(labelText, pos2[0], pos2[1])
        dc.SetPen(wx.Pen(self.gColor))
        dc.SetBrush( wx.Brush(self.gColor) )
        dc.DrawCircle(pos2[0]+tw+5, 8, 3)
        dc.SetPen(wx.BLACK_PEN)
        labelText = "Miss:"
        tw, th = dc.GetTextExtent(labelText)
        pos3 = (pos2[0]+50, 3)
        dc.DrawText(labelText, pos3[0], pos3[1])
        dc.SetPen(wx.Pen(self.mColor))
        dc.SetBrush( wx.Brush(self.mColor) )
        dc.DrawCircle(pos3[0]+tw+5, 8, 3)
            
    def DrawAxis(self, dc):
        #draw x axis
        dc.SetPen(wx.BLACK_PEN)
        dc.DrawLine(self.zeroX,self.midY,self.zeroX+self.rect.width,self.midY)
    
    def DrawMask(self, dc):
        l = self.data['dates']
        for id in self.maskIDs:
            startx = self.ProjectX(l[id][0])
            endx = self.ProjectX(l[id][1])
            dc.SetPen( wx.Pen(self.maskColor) )
            dc.SetBrush( wx.Brush(self.maskColor) )
            dc.DrawRectangle( startx, self.GetClientRect().y, endx-startx, self.GetClientRect().height)
    
            
    def DrawData(self, data, dc):
        #draw label
        self.labelFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)
        dc.SetFont(self.labelFont)
        self.penWidth = 1
        dc.SetPen(wx.Pen(wx.BLACK, self.penWidth))
        labels = data['labels']
        for i in range(len(labels)):
            label = labels[i]
            x = self.ProjectX(label[0])
            dc.DrawCircle(x, self.midY, 2)
            labelText = label[1]
            tw, th = dc.GetTextExtent(labelText)
            if i == len(labels)-1:
                dc.DrawText(labelText, x-tw/2-10, self.midY)
            else:
                dc.DrawText(labelText, x, self.midY)
        #mark anomalies
        self.penWidth = 5
        anomalies = data['anomolies']
        for anomaly in anomalies:
            type = anomaly[0]
            if type == 0:
                dc.SetPen(wx.Pen(self.eColor, self.penWidth))
            elif type == 1:
                dc.SetPen(wx.Pen(self.gColor, self.penWidth))
            elif type == 2:
                dc.SetPen(wx.Pen(self.mColor, self.penWidth))
            x1 = self.ProjectX((anomaly[1]))
            x2 = self.ProjectX((anomaly[2]))
            dc.DrawLine(x1,self.midY,x2,self.midY)
    
    #project to wxpython coordinatate top-left is (0,0)
    def ProjectX(self, x):
        x = x-self.minW
        x = self.zeroX+x*self.unitX        
        return x