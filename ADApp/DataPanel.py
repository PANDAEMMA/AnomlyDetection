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
        self.import_button = wx.Button(self, -1, "Import Data Source", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnImport, self.import_button)
        
        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.import_button, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 50)
        self.SetSizer(sizer)
    
    def OnImport(self,e):
        self.GetTopLevelParent().OnImport(e)
        
class AttributePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.spinLabel = wx.StaticText(self, -1, "Anomalies No: ", (15, 10))
        font = wx.Font(12,  wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.spinLabel.SetFont(font)
        self.k_spin = wx.SpinCtrl(self, -1, "", (30, 50))
        self.k_spin.SetRange(1,50)
        self.k_spin.SetValue(self.GetTopLevelParent().AnomalNum)
        self.Bind(wx.EVT_SPINCTRL, self.OnSpin, self.k_spin)
        self.dragEffect = wx.RadioBox(
                self, -1, "Comic Map Effect: ", wx.DefaultPosition, wx.DefaultSize,
                ['swap', 'merge'], 2, wx.RA_SPECIFY_COLS
                )
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.dragEffect)
    
        # Layout
        self.k_spin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.k_spin_sizer.Add(self.spinLabel,1,wx.ALIGN_CENTER_VERTICAL)
        self.k_spin_sizer.Add(self.k_spin,0,wx.ALIGN_CENTER_VERTICAL)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(self.k_spin_sizer, 0, wx.LEFT|wx.TOP|wx.BOTTOM, 10)
        self.vsizer.Add(self.dragEffect, 0, wx.LEFT|wx.TOP|wx.BOTTOM, 10)
        self.SetSizer(self.vsizer)
        
    def OnSpin(self,e):
        self.GetTopLevelParent().SetAnomalyNum(self.k_spin.GetValue())
    
    def EvtRadioBox(self, event):
        if event.GetInt() == 0:
            self.GetTopLevelParent().SetGridEffect('swap')
        if event.GetInt() == 1:
            self.GetTopLevelParent().SetGridEffect('merge')

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