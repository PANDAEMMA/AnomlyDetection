import wx
import os
import wx.lib.agw.foldpanelbar as fpb

class DataPanel(wx.Panel):
    def __init__(self,parent,id):
        wx.Panel.__init__(self,parent,id=id,style=wx.SUNKEN_BORDER)
        #create the manager
        self.foldPanel = FoldPanelMgr(self)
        #init
        self.foldPanel.AddPanel(DataSourcePanel, "Data")
        self.foldPanel.AddPanel(AttributePanel, "Attribute")
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
        wx.Button(self, 10, "Attribute Button", (20, 100))

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