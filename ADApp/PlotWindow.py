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
        self.id = id
        self.sourceID = id-1000
        self.dataID = id-1000
        print self.GetParent()
        #drop target
        self.dropTarget = DropTarget(self)
        self.SetDropTarget(self.dropTarget)
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
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)#drag     
        
    #def redefineInputData(self, data):
    
    def ReDraw(self, dataID, data):
        self.dataID = dataID
        #define maxH and maxW for Axis
        self.data = data
        self.maxH = self.maxW = 0
        self.findMaxHW(self.data)
        self.minH = self.maxH #here to use maxH(=0) or self.maxH??
        self.minW = self.maxW
        self.findMinHW(self.data)
        self.Refresh()
        
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
    
    def OnLeftDown(self, event):
        self.StartDragOpperation()
        
    def UpdateDragTarget(self):
        self.GetParent().UpdateDragTarget(self.sourceID)


    def StartDragOpperation(self):

        # create our own data format and use it in a
        # custom data object
        data = wx.CustomDataObject("anomalyID")
        data.SetData(str(self.sourceID))

        # And finally, create the drop source and begin the drag
        # and drop opperation
        dropSource = wx.DropSource(self)
        dropSource.SetData(data)
        #print "Begining DragDrop\n"
        result = dropSource.DoDragDrop(wx.Drag_AllowMove)
        #print "DragDrop completed:\n"

        #if result == wx.DragMove:
    def SetSwapSource(self, sourceID):
        self.GetParent().Swap(int(sourceID), self.GetParent().dragTarget)
    
class DropTarget(wx.PyDropTarget):
    def __init__(self, window):
        wx.PyDropTarget.__init__(self)
        self.dv = window

        # specify the type of data we will accept
        self.data = wx.CustomDataObject("anomalyID")
        self.SetDataObject(self.data)
        
    def OnEnter(self, x, y, d):
        self.dv.UpdateDragTarget()
        return d


    # Called when OnDrop returns True.  We need to get the data and
    # do something with it.
    def OnData(self, x, y, d):

        # copy the data from the drag source to our data object
        if self.GetData():
            # convert it back to a list of lines and give it to the viewer
            anomalyID = self.data.GetData()
            self.dv.UpdateDragTarget()
            self.dv.SetSwapSource(anomalyID)
            
        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return d  
        