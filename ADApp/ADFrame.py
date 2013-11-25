import wx
import math
from DataPanel import *
from AnalyzePanel import *
from File import *
from Search import *

#phi = (1 + math.sqrt(5)) / 2
#resphi = 2 - phi

class ADFrame(wx.Frame):
    def __init__(self, size):
        wx.Frame.__init__(self, None, -1, 'Anomaly Detection Tool', size = size)
        #init main menu
        self.SetMenuBar(self.CreateMenuBar())
        #set panels
        self.ID_DATAPANEL = 100
        self.ID_ANALYZEPANEL = 101
        self.DataPanel = DataPanel(self,self.ID_DATAPANEL)
        self.AnalyzePanel = AnalyzePanel(self,self.ID_ANALYZEPANEL)
	#File Read
	self.File = File(self)
	#Data Search
	self.Search = Search(self)
        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.DataPanel.SetSize((200, -1))
        sizer.Add(self.DataPanel, 0, wx.EXPAND)
        sizer.Add(self.AnalyzePanel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
    def CreateMenuBar(self):
        menu_bar = wx.MenuBar()
        #menus
        file_menu = wx.Menu()
        MENU_QUIT = wx.NewId()
        file_menu.Append(MENU_QUIT,"&Exit")
        menu_bar.Append(file_menu,"&File")
        
        help_menu = wx.Menu()
        MENU_ABOUT = wx.NewId()
        help_menu.Append(MENU_ABOUT,"&About")
        menu_bar.Append(help_menu,"&Help")
        #bind events for menu
        self.Bind(wx.EVT_MENU, self.OnQuit, id=MENU_QUIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=MENU_ABOUT)
        return menu_bar
        
    #event handlers
    def OnQuit(self, event):
        self.Destroy()
        
    def OnAbout(self, event):
        msg = "This Is The About Anomaly Detection and Data Clean Tool.\n\n" + \
              "Author: Tsung Tai Yeh&Shuying Feng @ Purdue\n\n"
        dlg = wx.MessageDialog(self, msg, "Data Clean Tool",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False, "Verdana"))
        dlg.ShowModal()
        dlg.Destroy()
   
    def OnImport(self, event):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.openFilePath = os.path.join(self.dirname, self.filename)
	    data = self.File.FileRead(self.openFilePath)
 	    dataSize = len(data)	
	    result = self.Search.goldenSectionSearch(data, 0, dataSize/2, dataSize, 1)
	    print result
            #TODO handle data read and data parser by call utility functions here
            #TODO need a new draw function pass in data here
	    #TODO need to deliver multiple possible data ranges
            self.DrawComicMap(zipped)
        dlg.Destroy()
    
	#analyze functions
    def DrawComicMap(self, zipped):
        #genData mimic data here, will by read later
        list = []
        dic = dict()
        dic1 = dict()
        dic2 = dict()
        dic3 = dict()
        dic['color'] = 'red'
        dic1['color'] = (255, 255, 0)
        dic2['color'] = (255, 0, 255)
        dic3['color'] = 'green'
        #dic['points'] = [(-10, 30),(20, -40), (30, 90), (40, 50)]
        dic['points'] = zipped
	dic1['points'] = [(-20, 10),(0, 40), (30, 60), (40, 50)]
        dic2['points'] = [(-10, 30),(20, 90), (30, -40), (40, 90)]
        dic3['points'] = [(-40, 30),(0, -40), (30, 80), (40, 90)]
        list.append([dic])
        list.append([dic1])
        list.append([dic2])
        list.append([dic3])
        #TODO need to maintain comic maps ID globally here
        self.AnalyzePanel.AddComicMap(list, 200, 3)
