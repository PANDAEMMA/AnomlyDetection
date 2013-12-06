import wx
import sys
import wx.lib.mixins.listctrl as listmix

class DataCleanWindow(wx.Frame):
    def __init__(self,parent,id,data):
        wx.Frame.__init__(self, parent, id, 'Data', size=(350,500))
        wx.Frame.CenterOnScreen(self)
        CONTENT_ID = wx.NewId()
        self.panel = wx.Panel(self)
        self.list = DataCleanContent(self.panel, CONTENT_ID, data)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.list, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        
class DataCleanContent(wx.ListCtrl, listmix.CheckListCtrlMixin, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id, data):
        wx.ListCtrl.__init__(self, parent, id=id, style=wx.LC_REPORT)
        listmix.CheckListCtrlMixin.__init__(self)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(4)
        self.data = data
        self.SetLabels(self.data['labels'])
        self.SetData(self.data['data'])

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        
    def SetLabels(self, labels):
        self.InsertColumn(0, "Clean")
        for i in range(len(labels)):
            self.InsertColumn(i+1, labels[i])
            
    def SetData(self,data):
        for i in range(len(data)):
            index = self.InsertStringItem(sys.maxint, 'Delete')
            if data[i][0] == 0:
                self.SetStringItem(index, 1, 'Extreme')
            elif data[i][0] == 1:
                self.SetStringItem(index, 1, 'Glitche')
            else:
                self.SetStringItem(index, 1, 'Missing')
            self.SetStringItem(index, 2, str(data[i][1]))
            self.SetStringItem(index, 3, data[i][2])
            self.SetItemData(index, i)

    def OnItemActivated(self, evt):
        self.ToggleItem(evt.m_itemIndex)
        
    def OnCheckItem(self, index, flag):
        print(index, flag)
            
