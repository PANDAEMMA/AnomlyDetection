import wx

#Data should be a list of dictionaries
#each dictionary is like {color:
#                         points: [list]}
# points:[(w1,h1) (w2,h2) (w3,h3)]
# need a id to maintain
# maxH to define the Y scale, default will be largest number+5
class PlotWindow(wx.Window):
    def __init__(self, parent, id, data, maxH=0, maxW=0):
        wx.Window.__init__(self, parent, id=id, style=wx.SUNKEN_BORDER)
        self.SetSize((100,100))
        self.SetBackgroundColour(wx.WHITE)
        #define maxH and maxW for Axis
        self.data = data
        self.maxH = maxH
        self.maxW = maxW
        self.findMaxHW(self.data)
        self.minH = maxH #here to use maxH(=0) or self.maxH??
        self.minW = maxW
        self.findMinHW(self.data)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    #def redefineInputData(self, data):
        
    def findMaxHW(self, list):
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
                
    def findMinHW(self, list):
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
        #draw
        dc.SetPen(wx.BLACK_PEN)
        if p[1] >self.zeroY:
            dc.DrawLine(self.zeroX,p[1],self.zeroX+self.rect.width,p[1])
        if p[0] >self.zeroX:
            dc.DrawLine(p[0],self.zeroY,p[0],self.zeroY+self.rect.height)
            
    def DrawData(self, data, dc):
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
        