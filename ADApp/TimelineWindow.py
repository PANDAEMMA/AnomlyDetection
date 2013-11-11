import wx

#Data should be a list of dictionaries
#each dictionary is like {color:, labels:[list], anomolies: [list], points: [list]}
# points:[(w1,h1) (w2,h2) (w3,h3)]
# need a id to maintain
# maxH to define the Y scale, default will be largest number+5
class TimelineWindow(wx.Window):
    def __init__(self, parent, id, data):
        wx.Window.__init__(self, parent, id=id, style=wx.SUNKEN_BORDER)
        self.id = id
        self.SetSize((600,100))
        self.radius = 3 #mark circle size
        self.SetBackgroundColour(wx.WHITE)
        self.data = data
        self.maxH = self.maxW = self.minH = self.minW = 0
        self.findMax(self.data)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    def findMax(self, list):
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
        
        for l in list:
            c = l['points']
            for point in c:
                if point[1]<self.minH and point[0]<self.minW:
                    self.minH = point[1]
                    self.minW = point[0]
                elif point[0]<self.minW:
                    self.minW = point[0]
                elif point[1]<self.minH:
                    self.minH = point[1]
                else:
                    continue
        self.minH = self.minH-5
        self.minW = self.minW-5
        
    def OnPaint(self, event):
        #init paint 
        dc = wx.PaintDC(self)
        self.rect = self.GetClientRect()
        self.zeroX = self.rect.x
        self.zeroY = self.rect.y
        self.unitX = float(self.rect.width)/(self.maxW-self.minW)
        self.unitY = float(self.rect.height)/(self.maxH-self.minH)
        #dc.DrawLine(0,0,2,2)
        self.DrawAxis(dc)
        for dataset in self.data:
            self.DrawData(dataset, dc)
            
    def DrawAxis(self, dc):
        #find origin
        p = self.Projection((0, 0))
        #draw x axis
        dc.SetPen(wx.BLACK_PEN)
        if p[1] >self.zeroY:
            dc.DrawLine(self.zeroX,p[1],self.zeroX+self.rect.width,p[1])
            
    def DrawData(self, data, dc):
        #draw label
        self.labelFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)
        dc.SetFont(self.labelFont)
        dc.SetPen(wx.BLACK_PEN)
        labels = data['labels']
        for label in labels:
            pos = self.Projection((label[0], 0))
            dc.DrawCircle(pos[0], pos[1], 2)
            labelText = label[1]
            tw, th = dc.GetTextExtent(labelText)
            dc.DrawText(labelText, pos[0], pos[1])
        #mark anomalies
        dc.SetPen(wx.RED_PEN)
        anomalies = data['anomolies']
        for dotID in anomalies:
            dotPos = data['points'][dotID] 
            ppos = self.Projection(dotPos)
            dc.DrawCircle(ppos[0], ppos[1], self.radius)
        #draw lines
        if data['color'] == 'red':
            dc.SetPen(wx.RED_PEN)
        if data['color'] == 'green':
            dc.SetPen(wx.GREEN_PEN)
        if data['color'] == 'blue':
            dc.SetPen(wx.BLUE_PEN)
        if type(data['color']) == tuple:
            dc.SetPen(wx.Pen(wx.Colour(data['color'][0], data['color'][1], data['color'][2])))
        points = data['points']
        newpoints = []
        for point in points:
            newpoints.append(self.Projection(point))
        dc.DrawLines(newpoints)
        
    #project to wxpython coordinatate top-left is (0,0)
    def Projection(self, p):
        x = p[0]
        y = p[1]
        x = x-self.minW
        y = y-self.minH
        x = self.zeroX+x*self.unitX;
        y = self.zeroY+(self.rect.height-y*self.unitY)
        return (x,y)