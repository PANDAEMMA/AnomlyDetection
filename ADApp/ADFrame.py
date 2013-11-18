import wx
import math
from DataPanel import *
from AnalyzePanel import *
from ADParse import *
from ADAnLineCell import *


class ADFrame(wx.Frame):
    def __init__(self, size):
        wx.Frame.__init__(self, None, -1, 'Anomaly Detection Tool', size = size)
        #init data for app
        self.AnomalNum = 4
        self.ParNum = 4
        self.GridEffect = 'swap'
        self.DataType = TEMPER
        #init main menu
        self.SetMenuBar(self.CreateMenuBar())
        #set panels
        self.ID_DATAPANEL = 100
        self.ID_ANALYZEPANEL = 101
        self.DataPanel = DataPanel(self,self.ID_DATAPANEL)
        self.AnalyzePanel = AnalyzePanel(self,self.ID_ANALYZEPANEL)
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
            #TODO handle data read and data parser by call utility functions here
            #TODO need a new draw function pass in data here
            #self.DrawComicMap(zipped)
            #self.anomalies = AnalyzeData(self.openFilePath)
            #self.anomaliesData = self.PackDataToDraw(self.anomalies)
            #self.DrawComicMap(self.anomaliesData)
            #self.UpdateAttribute('temprature')

            #TODO: Designing an interface to pass the following parameters: partition, top_k, dataObj_index
            partition = self.ParNum
            top_k = self.AnomalNum
            self.anomalies = AnalyzeData(self.openFilePath, self.DataType)
            #self.anomalies = []
            self.anomaliesData = self.PackDataToDraw(self.anomalies)
            #self.timelineData = self.PackTimelineData();
            self.DrawComicMap(self.anomaliesData)
            #self.DrawTimeline(self.timelineData)
        dlg.Destroy()
        
    def UpdateAttribute(self, attr):
        checkboxes = self.DataPanel.attributePanel.GetChildren()
        if attr == 'temprature':
            checkboxes[0].SetValue(True)
        if attr == 'humidity':
            checkboxes[1].SetValue(True)
        if attr == 'airPressure':
            checkboxes[2].SetValue(True)
            
    def PackDataToDraw(self, anomalies):
        data = []

#       TODO: Design an interface to let users key in top_k, chunk_num, dataObj_i
#	 top_k is the number of ceil you want to show them out
# 	 chunk_num is the number of partitions. Dividing data into a couple of partitions. e.g. 1, 2, .... 
# 	 dataObj_i is the category of data index. e.g. TEMPER = 8 (refer ADParse.py)

#	AnalyzeData(fileObj, top_k, chunk_num, dataObj_i):
#       AnalyzeData returns 
# 	t is the index of top_k, e.g. 1, 2, 3, ...
# 	index is the x-axis
# 	r is the index of data chunk
# 	temp_anomaly is the temperature in one data chunk
#       zip(t, r, index, temp_anomaly)
# 	zipped output: e.g. (1, 0, 0, 23.2) (1, 0, 1, 24.2)
#       Using index, and temp_anomaly to draw the graph

        N = len(anomalies)
        for i in range(N):
            dic = dict()
            anomaly_data = []
            r = random.randint(100, 255)
            g = random.randint(30, 255)
            b = random.randint(30, 255)
            dic['color'] = (r,g,b)
            #dic['color'] = 'red'
            dic['points'] = anomalies[i]
            dic['labels'] = ['avg:12','min:23','dates:12/01-12/23']
            # Adding anomaly data index
            it = [item[1] for item in anomalies[i]]
            maxdata = getMaxIndex(it)
            anomaly_data.append(maxdata)
            mindata = getMinIndex(it)
            anomaly_data.append(mindata)
            dic['anomolies'] = anomaly_data
            data.append([dic])
	    anomaly_data = []
        return data

        '''#mimic Data
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
        dic['points'] = [(-10, 30),(20, -40), (30, 90), (40, 50)]
        dic1['points'] = [(-20, 10),(0, 40), (30, 60), (40, 50)]
        dic2['points'] = [(-10, 30),(20, 90), (30, -40), (40, 90)]
        dic3['points'] = [(-40, 30),(0, -40), (30, 80), (40, 90)]
        dic['anomolies'] = [1]
        dic1['anomolies'] = [2]
        dic2['anomolies'] = [0,2]
        dic3['anomolies'] = [3]
        list.append([dic])
        list.append([dic1])
        list.append([dic2])
        list.append([dic3])
        return list'''
    
    def PackTimelineData(self):
        #[{labels:[list], color:, points: [list], nomolies: [list]}]
        # the data part is the information you need to give me
        list = []
        data = dict()
        data['color'] = 'green'
        data['labels'] = [(0,'03/02/10'), (10, '05/01/10'), (20, '09/01/10')]
        data['points'] = [(-20, 10),(-10, 30),(0, 40), (20, -40), (30, 90), (40, 50),(60, 20)]
        data['anomolies'] = [0,3,4,5]
        list.append(data)
        return list
        
    #analyze functions
    def DrawComicMap(self, data):
        #TODO need to maintain comic maps ID globally here
        self.AnalyzePanel.AddComicMap(200, data)
        
    def DrawTimeline(self, data):
        self.AnalyzePanel.AddTimeline(300, data)
    
    def SetAnomalyNum(self, num):
        self.AnomalNum = num
        
    def SetParNum(self, num):
        self.ParNum = num
        
    def SetGridEffect(self, effect):
        self.GridEffect = effect
        
    def SetDataType(self, type):
        if type == 'TEMPER':
            self.DataType = TEMPER
        if type == 'HUMID':
            self.DataType = HUMID
        if type == 'PRESS':
            self.DataType = PRESS
        
    def OnZoom(self, zoom):
        if self.AnalyzePanel.comicMap is None:
            return false
        else:
            self.AnalyzePanel.OnZoom(zoom)
    
