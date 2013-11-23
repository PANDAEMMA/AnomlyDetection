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
        self.eColor = wx.RED
        self.gColor = wx.Colour(47,79,47)
        self.mColor = wx.BLUE
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
            self.DrawAxis(dc)
            #draw data
            self.DrawData(self.data, dc)
            #draw mask
            if self.mask == True:
                self.DrawMask(dc)
            
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
        for label in labels:
            x = self.ProjectX(label[0])
            dc.DrawCircle(x, self.midY, 2)
            labelText = label[1]
            tw, th = dc.GetTextExtent(labelText)
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