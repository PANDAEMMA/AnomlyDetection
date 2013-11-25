import wx

#Data should be a list of dictionaries
#each dictionary is like {color:,
#                         points: [list],anomolies: [list]}
# points:[(w1,h1) (w2,h2) (w3,h3)]
# need a id to maintain
# maxH to define the Y scale, default will be largest number+5
class PlotWindow(wx.Window):
    def __init__(self, parent, id, data):
        wx.Window.__init__(self, parent, id=id, style=wx.SUNKEN_BORDER)
        self.id = id-1000
        self.sourceID = id-1000
        self.dataID = [id-1000]
        #draw default setting
        self.mask_colour = wx.Colour( 0, 0, 0, 92 )
        self.radius = 3
        self.selectionStart = 0
        self.selectionEnd = 0
        self.scaleX = 1
        self.offsetX = 0
        self.projectedData = []
        self.selected = False
        self.clicked = False
        #drop target
        self.dropTarget = DropTarget(self)
        self.SetDropTarget(self.dropTarget)
        self.size = 200
        self.SetSize((self.size,self.size))
        self.SetBackgroundColour(wx.WHITE)
    
        self.data = data
        self.dataToDraw = data[:]
        self.GetProjectionData(False)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)#drag   
        self.Bind(wx.EVT_LEFT_UP,  self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)  
        
    #def redefineInputData(self, data):
    
    def getMaxData(self, redefineW):
        #define maxH and maxW for Axi, get from the unified value from parent
        self.maxH = self.GetParent().maxH
        if redefineW == True:
            self.findMaxW(self.dataToDraw)
        else:
            self.maxW = self.GetParent().maxW
        #self.findMaxHW(self.data)
        self.minH = 0 #here to use maxH(=0) or self.maxH??
        self.minW = 0
        self.findMinHW(self.data)
    
    def ReDraw(self, dataID, data):
        print "in redraw"
        print dataID
        self.dataID = dataID
        #define maxH and maxW for Axis
        self.data = data
        self.dataToDraw = data[:]
        self.GetProjectionData(False)
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
        
    def findMaxW(self, list):
        for l in list:
            c = l['points']
            for point in c:
                if point[0]>self.maxW:
                    self.maxW = point[0]
                elif point[0]>self.maxW:
                    self.maxW = point[0]
                else:
                    continue
                
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
        
    def GetProjectionData(self, redefineW):
        self.rect = self.GetClientRect()
        self.zeroX = self.rect.x
        self.zeroY = self.rect.y
        self.getMaxData(redefineW)
        self.unitX = float(self.rect.width)/(self.maxW-self.minW)
        self.unitY = float(self.rect.height)/(self.maxH-self.minH)
        
    def OnPaint(self, event):
        #init paint 
        pdc = wx.PaintDC(self)
        dc = wx.GCDC(pdc)
        #dc.SetUserScale(self.scaleX, self.scaleY)
        #draw data
        for dataset in self.dataToDraw:
            self.DrawData(dataset, dc)
        #draw Label
        self.DrawLabel(dc)
        #draw mask
        if not self.selectionStart == 0 and not self.selectionEnd == 0:
            self.DrawMask(dc)
        #draw outline
        if self.clicked == True:
            self.DrawOutline(dc)

    def DrawLabel(self, dc):
        self.labelFont = wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL)
        dc.SetFont(self.labelFont)
        dc.SetPen(wx.BLACK_PEN)
        for j in range(len(self.dataToDraw)):
            labels = self.dataToDraw[j]['labels'][0]
            for i in range(len(labels)):
                pos = (self.zeroX, self.zeroY)
                labelText = labels[i]
                tw, th = dc.GetTextExtent(labelText)
                dc.DrawText(labelText, pos[0]+3+(tw*j), pos[1]+i*(th+3))
        #cross
        print len(self.dataID)
        print self.dataID
        if (len(self.dataID))> 1:
            cross1 = (self.rect.width-25, self.zeroY)
            cross2 = (self.rect.width-5, self.zeroY)
            cross3 = (self.rect.width-5, self.zeroY+20)
            cross4 = (self.rect.width-25, self.zeroY+20)
            dc.DrawLine(cross1[0], cross1[1], cross2[0], cross2[1])
            dc.DrawLine(cross2[0], cross2[1], cross3[0], cross3[1])
            dc.DrawLine(cross3[0], cross3[1], cross4[0], cross4[1])
            dc.DrawLine(cross4[0], cross4[1], cross1[0], cross1[1])
        
            dc.DrawLine(cross1[0], cross1[1], cross3[0], cross3[1])
            dc.DrawLine(cross2[0], cross2[1], cross4[0], cross4[1])
                
    def DrawOutline(self, dc):
        penWidth = 1
        add = 5
        dc.SetPen(wx.Pen(wx.RED, penWidth))
        pos1 = (self.zeroX, self.zeroY)
        pos2 = (self.zeroX, self.zeroY+self.rect.height-add)
        pos3 = (self.zeroX+self.rect.width-add, self.zeroY+self.rect.height-add)
        pos4 = (self.zeroX+self.rect.width-add, self.zeroY)
        
        dc.DrawLine(pos1[0], pos1[1],pos2[0], pos2[1])
        dc.DrawLine(pos2[0], pos2[1],pos3[0], pos3[1])
        dc.DrawLine(pos3[0], pos3[1],pos4[0], pos4[1])
        dc.DrawLine(pos4[0], pos4[1],pos1[0], pos1[1])
            
    def DrawData(self, data, dc):
        #mark anomalies
        dc.SetPen(wx.RED_PEN)
        anomalies = data['anomolies']
        for dotID in anomalies:
            dotPos = data['points'][dotID] 
            ppos = self.Projection(dotPos)
            dc.DrawCircle(ppos[0], ppos[1], self.radius)
        #draw data
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
        for i in range(len(points)):
            newPoint = self.Projection(points[i])
            newpoints.append(newPoint)
        dc.DrawLines(newpoints)
        
    def DrawMask(self,dc):
        dc.SetPen( wx.Pen(self.mask_colour) )
        dc.SetBrush( wx.Brush(self.mask_colour) )
        dc.DrawRectangle( self.selectionStart, self.GetClientRect().y, self.selectionEnd-self.selectionStart, self.GetClientRect().height)
    
    def DoneZoom(self):
        for set in range(len(self.dataToDraw)):
            selected = []
            dataset = self.dataToDraw[set]
            for i in range(len(dataset['points'])):
                point = dataset['points'][i]
                print "-----------"
                print self.Projection(point)[0]
                print self.selectionStart
                print self.selectionEnd
                print "-----------"
                if self.Projection(point)[0]>= self.selectionStart and self.Projection(point)[0]>= self.selectionEnd:
                    selected.append(point)
            #resort
            diff = selected[0][0]-0
            for j in range(len(selected)):
                newpoint = (j,selected[j][1])
                selected[j] = newpoint
            self.dataToDraw[set]['points']= selected
            newAnomalies = []
            for anomly in self.dataToDraw[set]['anomolies']:
                anomly = anomly-diff
                if anomly<0 or anomly>len(self.dataToDraw[set]['points']):
                    continue
                else:
                    newAnomalies.append(anomly)
            self.dataToDraw[set]['anomolies']= newAnomalies       
        
        self.selectionStart = 0
        self.selectionEnd = 0
        
        self.GetProjectionData(True)
        self.Refresh()
        
        
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
        self.GetParent().UpdateClick(self.id)
        if self.GetTopLevelParent().GridEffect == "swap" or self.GetTopLevelParent().GridEffect == "merge":
            self.StartDragOpperation()
        if self.GetTopLevelParent().GridEffect == "zoom":
            self.selection = []
            x, y = event.GetPositionTuple()
            self.selectionStart = x;
            self.CaptureMouse()
            #self.GetTopLevelParent().UpDateTimeline
            
    def OnMotion(self, event):
        if self.HasCapture() and event.Dragging() and self.GetTopLevelParent().GridEffect == "zoom":
            x, y = event.GetPositionTuple()
            self.selectionEnd = x
            self.Refresh()
    
    def OnLeftUp(self, event):
        if self.HasCapture() and self.GetTopLevelParent().GridEffect == "zoom":
            self.ReleaseMouse()
            self.DoneZoom()
            
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
        result = dropSource.DoDragDrop(wx.Drag_AllowMove)

    def SetSwapSource(self, sourceID):
        self.GetParent().OnGridChange(int(sourceID), self.GetParent().dragTarget)
        
    def UpdateClicke(self, click):
        self.clicked = click
        self.Refresh()
    
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
        
