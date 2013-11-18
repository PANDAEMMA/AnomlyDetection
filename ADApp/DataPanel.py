import wx
import os
import wx.lib.agw.foldpanelbar as fpb

class DataPanel(wx.Panel):
    def __init__(self,parent,id):
        wx.Panel.__init__(self,parent,id=id,style=wx.SUNKEN_BORDER)
        #create the manager
        self.foldPanel = FoldPanelMgr(self)
        #init
        self.dataSourcePanel = self.foldPanel.AddPanel(DataSourcePanel, "Data")
        self.attributePanel = self.foldPanel.AddPanel(AttributePanel, "Attribute")
        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.foldPanel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
#sub panels
class DataSourcePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        '''self.spinLabel = wx.StaticText(self, -1, "Anomalies No: ", (15, 10))
        font = wx.Font(12,  wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.spinLabel.SetFont(font)
        self.k_spin = wx.SpinCtrl(self, -1, "", (30, 50))
        self.k_spin.SetRange(1,50)
        self.k_spin.SetValue(self.GetTopLevelParent().AnomalNum)
        self.Bind(wx.EVT_SPINCTRL, self.OnSpinK, self.k_spin)
        
        self.parLabel = wx.StaticText(self, -1, "Partition No: ", (15, 10))
        font = wx.Font(12,  wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.parLabel.SetFont(font)
        self.par_spin = wx.SpinCtrl(self, -1, "", (30, 50))
        self.par_spin.SetRange(1,50)
        self.par_spin.SetValue(self.GetTopLevelParent().ParNum)
        self.Bind(wx.EVT_SPINCTRL, self.OnSpinPar, self.par_spin)'''
        
        self.dataType = wx.RadioBox(
                self, -1, "Choose Data: ", wx.DefaultPosition, wx.DefaultSize,
                ['Temperature', 'Humidity', 'Pressure'], 1, wx.RA_SPECIFY_COLS
                )
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.dataType)
        
        self.import_button = wx.Button(self, -1, "Import Data Source", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnImport, self.import_button)
        
        # Layout
        #self.k_spin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.k_spin_sizer.Add(self.spinLabel,1,wx.ALIGN_CENTER_VERTICAL)
        #self.k_spin_sizer.Add(self.k_spin,0,wx.ALIGN_CENTER_VERTICAL)
        #self.par_spin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.par_spin_sizer.Add(self.parLabel,1,wx.ALIGN_CENTER_VERTICAL)
        #self.par_spin_sizer.Add(self.par_spin,0,wx.ALIGN_CENTER_VERTICAL)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        #self.vsizer.Add(self.k_spin_sizer, 0, wx.LEFT|wx.TOP|wx.BOTTOM, 10)
        #self.vsizer.Add(self.par_spin_sizer, 0, wx.LEFT|wx.TOP|wx.BOTTOM, 10)
        self.vsizer.Add(self.dataType, 0, wx.LEFT|wx.TOP|wx.BOTTOM, 10)
        self.vsizer.Add(self.import_button, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 50)
        self.SetSizer(self.vsizer)
    
    def OnImport(self,e):
        self.GetTopLevelParent().OnImport(e)
        
    def OnSpinK(self,e):
        self.GetTopLevelParent().SetAnomalyNum(self.k_spin.GetValue())
        
    def OnSpinPar(self,e):
        self.GetTopLevelParent().SetParNum(self.par_spin.GetValue())
    
    def EvtRadioBox(self, event):
        if event.GetInt() == 0:
            self.GetTopLevelParent().SetDataType('TEMPER')
        if event.GetInt() == 1:
            self.GetTopLevelParent().SetDataType('HUMID')
        if event.GetInt() == 2:
            self.GetTopLevelParent().SetDataType('PRESS')
            
        
class AttributePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
    
        self.dragEffect = wx.RadioBox(
                self, -1, "Comic Map Effect: ", wx.DefaultPosition, wx.DefaultSize,
                ['swap', 'merge', 'zoom'], 1, wx.RA_SPECIFY_COLS
                )
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.dragEffect)
        self.zoomIn = wx.Button(self, 501, "Zoom In", (20,150), style=wx.NO_BORDER)
        self.Bind(wx.EVT_BUTTON, self.OnClickZoomIn, self.zoomIn)
        self.zoomOut = wx.Button(self, 502, "Zoom Out", (20,150), style=wx.NO_BORDER)
        self.Bind(wx.EVT_BUTTON, self.OnClickZoomOut, self.zoomOut)
    
        # Layout
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(self.dragEffect, 0, wx.LEFT|wx.TOP|wx.BOTTOM, 10)
        self.vsizer.Add(self.zoomIn , 0, wx.LEFT|wx.TOP|wx.BOTTOM, 10)
        self.vsizer.Add(self.zoomOut , 0, wx.LEFT|wx.TOP|wx.BOTTOM, 10)
        self.SetSizer(self.vsizer)
    
    def EvtRadioBox(self, event):
        if event.GetInt() == 0:
            self.GetTopLevelParent().SetGridEffect('swap')
        if event.GetInt() == 1:
            self.GetTopLevelParent().SetGridEffect('merge')
        if event.GetInt() == 2:
            self.GetTopLevelParent().SetGridEffect('zoom')
            
    def OnClickZoomIn(self, event):
        self.GetTopLevelParent().OnZoom("in")
    
    def OnClickZoomOut(self, event):
        self.GetTopLevelParent().OnZoom("out")
    

#a utility class fold panel manager
class FoldPanelMgr(fpb.FoldPanelBar):
    """Fold panel that manages a collection of Panels"""
    def __init__(self,parent,*args,**kwargs):
        super(FoldPanelMgr, self).__init__(parent,*args,**kwargs)
        
    """Add a panel to the manager, 
       combine AddFoldPanel and AddFoldPanelWindow, 
       also set sizer to wrapper class
        @param pclass: Class constructor (callable)
        @keyword title: foldpanel title
        @keyword collapsed: start with it collapsed
        @return: pclass instance
        """
    def AddPanel(self, pclass, title=u"", collapsed=False):
        fpitem = self.AddFoldPanel(title, collapsed=collapsed)
        wnd = pclass(fpitem)
        best = wnd.GetBestSize()
        wnd.SetSize(best)
        self.AddFoldPanelWindow(fpitem, wnd)
        return wnd