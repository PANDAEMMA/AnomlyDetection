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
        
        self.dataType = wx.RadioBox(
                self, -1, "Choose Data: ", wx.DefaultPosition, wx.DefaultSize,
                ['Temperature', 'Humidity', 'Pressure'], 1, wx.RA_SPECIFY_COLS
                )
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.dataType)
        
        self.import_button = wx.Button(self, -1, "Import Data Source", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnImport, self.import_button)
        
        # Layout
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(self.dataType, 0, wx.LEFT|wx.TOP|wx.BOTTOM, 10)
        self.vsizer.Add(self.import_button, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 20)
        self.SetSizer(self.vsizer)
    
    def OnImport(self,e):
        self.GetTopLevelParent().OnImport(e)
        
    def OnSpinK(self,e):
        self.GetTopLevelParent().SetAnomalyNum(self.k_spin.GetValue())
        
    def OnSpinPar(self,e):
        self.GetTopLevelParent().SetParNum(self.par_spin.GetValue())
    
    def OnStartDateChanged(self, evt):
        self.log.write("OnDateChanged: %s\n" % evt.GetDate())
    
    def OnEndDateChanged(self, evt):
        self.log.write("OnDateChanged: %s\n" % evt.GetDate())
    
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
    
        # Layout
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(self.dragEffect, 0, wx.LEFT|wx.TOP|wx.BOTTOM, 10)
        self.SetSizer(self.vsizer)
    
    def EvtRadioBox(self, event):
        if event.GetInt() == 0:
            self.GetTopLevelParent().SetGridEffect('swap')
        if event.GetInt() == 1:
            self.GetTopLevelParent().SetGridEffect('merge')
        if event.GetInt() == 2:
            self.GetTopLevelParent().SetGridEffect('zoom')
    

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
