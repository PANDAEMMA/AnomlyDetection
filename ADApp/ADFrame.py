import wx
import math
from numpy import *
from DataPanel import *
from AnalyzePanel import *
from ADParse import *
from ADAnLineCell import *
from DataWindow import *
from DataCleanWindow import *
from ADAnList import *
from ADAnOverview import *
from time import clock,time

class ADFrame(wx.Frame):
    def __init__(self, size):
        wx.Frame.__init__(self, None, -1, 'Anomaly Detection Tool', size = size, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        #init data for app
        self.canClean = False
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
        # TimeLine
	self.TimeLineLen = 600
	# Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.DataPanel.SetSize((200, -1))
        sizer.Add(self.DataPanel, 0, wx.EXPAND)
        sizer.Add(self.AnalyzePanel, 1, wx.EXPAND)
        self.SetSizer(sizer)
    
    def CreateMenuBar(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        MENU_QUIT = wx.NewId()
	MENU_IMPORT = wx.NewId()
        file_menu.Append(MENU_QUIT,"&Exit")
        file_menu.Append(MENU_IMPORT, "&Import")
        menu_bar.Append(file_menu,"&File")
        
        tool_menu = wx.Menu()
        MENU_DATACLEANWINDOW = wx.NewId()
        tool_menu.Append(MENU_DATACLEANWINDOW,"&Clean Data")
        menu_bar.Append(tool_menu,"&Tools")
        
        help_menu = wx.Menu()
        MENU_ABOUT = wx.NewId()
        help_menu.Append(MENU_ABOUT,"&About")
        menu_bar.Append(help_menu,"&Help")
        self.Bind(wx.EVT_MENU, self.OnQuit, id=MENU_QUIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=MENU_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnDataClean, id=MENU_DATACLEANWINDOW)
	self.Bind(wx.EVT_MENU, self.OnImport, id=MENU_IMPORT)
        return menu_bar
        
    #event handlers
    def OnQuit(self, event):
        self.Destroy()
        
    def OnAbout(self, event):
        msg = "This Is ADetector:An Anomaly Detection and Data Clean Tool.\n\n" + \
              "Author: Tsung Tai Yeh&Shuying Feng @ Purdue\n\n"
        dlg = wx.MessageDialog(self, msg, "Data Clean Tool",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False, "Verdana"))
        dlg.ShowModal()
        dlg.Destroy()
        
    def OnDataClean(self, event):
        if self.canClean == True:
            self.dataCleanWindow = DataCleanWindow(self, id=-1000, data = self.cleanData)
            self.dataCleanWindow.Show()
        else:
            dlg = wx.MessageDialog(self, 'Please import the source data and select a region first!',
            'No anomalies found', wx.OK| wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        
    def OnImport(self, event):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.openFilePath = os.path.join(self.dirname, self.filename)
            #----------------TODO/Done-------------------
            #backend function called function: StatisticalAnalyze
            #self.dangerData = StatisticalAnalyze(self.openFilePath, self.DataType)
            self.dangerData = []
            self.dangerData = self.StatisticalAnalyze(self.openFilePath, self.DataType)
	    self.dataWindow = DataWindow(self, 1, self.dangerData)
            self.dataWindow.Show()	
        dlg.Destroy()

    def StatisticalAnalyze(self, openFilePath, DataType):
	year_ID = get_year_i(openFilePath, YEAR)
	y_data = normal_stat(openFilePath, YEAR, DataType)
	data = []
	dic1 = dict()
	for i in range(len(year_ID)):
		m_data = normal_mon_stat(openFilePath, year_ID[i], DataType)
		dic1 = dict( year=year_ID[i], year_data=y_data[i], month_data=m_data )
		data.append(dic1)
	return data
	
    def UpdateAttribute(self, attr):
	attr = 'temperature'
	"""
        checkboxes = self.DataPanel.attributePanel.GetChildren()
        if attr == 'temprature':
            checkboxes[0].SetValue(True)
        if attr == 'humidity':
            checkboxes[1].SetValue(True)
        if attr == 'airPressure':
            checkboxes[2].SetValue(True)"""
        
    #analyze functions
    def DrawComicMap(self, data):
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
    
    def DoneRegionSel(self, data):
        self.dataWindow.Close(True)
	self.anomalies = AnalyzeData(self.openFilePath, self.DataType, data[0], data[1])
	self.overviewData = self.cleanData = data
        self.cleanData = self.PackCleanData(self.cleanData)
        self.anomaliesData = self.PackDataToDraw(self.anomalies)
        self.timelineData = self.PackTimelineData(self.overviewData, self.anomalies)
        self.DrawComicMap(self.anomaliesData)
        self.DrawTimeline(self.timelineData)
        
    def PackCleanData(self, data):
        self.cleanData = dict()
        self.cleanData['labels'] = ['Type', 'Value', 'Date']
	self.clean = CleanAnalyze(self.openFilePath, self.DataType, data[0], data[1])
	clean_d1 = [item[0] for item in self.clean]
	clean_d2 = [item[1] for item in self.clean]
	clean_d3 = [item[2] for item in self.clean]
	clean_dd = zip(clean_d1, clean_d2, clean_d3)
	self.cleanData['data'] = clean_dd
        self.canClean = True
        return self.cleanData
        
    def PackDataToDraw(self, anomalies):
        data = []
        N = len(anomalies)
        for i in range(N):
            dic = dict()
            anomaly_data = []
            r = random.randint(100, 255)
            g = random.randint(30, 255)
            b = random.randint(30, 255)
            dic['color'] = (r,g,b)
            # Adding anomaly data index
            # decompose the anomaly data array
            index = [item[0] for item in anomalies[i]]
            an_data = [item[1] for item in anomalies[i]]
            date = [item[2] for item in anomalies[i]]
	    model = [item[4] for item in anomalies[i]]
            points = zip(index, an_data)
	    points_m = zip(index, model)
            length_index = len(index)
            """# std cal.
            std = []
            aa = stdcal(an_data, length_index)
            std.append('std:'+ (str)(aa))
            # avg cal.
            average = []
            av = avg(an_data, length_index)
            average.append('mean:' + (str)(av))"""
            # start date
            start_date = []
            start_date.append('sdate:'+ (str)(anomalies[i][0][2]))
            # end date
            end_date = []
            end_date.append('edate:' + (str)(anomalies[i][length_index - 1][2]))
           #label = zip(std, average, start_date, end_date)
	    label = zip(start_date, end_date)
            # add std, avg, and date into label
            dic['labels'] = label
            # add anomaly data
            dic['points'] = points
	    dic['model'] = points_m
            # add extreme data
            maxdata = getMaxIndex(an_data)
            anomaly_data.append(maxdata)
            #mindata = getMinIndex(an_data)
            #anomaly_data.append(mindata)
            dic['anomolies'] = anomaly_data
            data.append([dic])
            anomaly_data = []
            
        return data

    def PackTimelineData(self, an, anomalies):
	chunk_num = 5
	x_axis = get_x_axis(self.openFilePath, self.DataType, an[0], an[1], self.TimeLineLen, chunk_num)
        data = dict()
	data['labels'] = x_axis

	N = len(anomalies)
	size = get_year_size(self.openFilePath, self.DataType, an[0])
	miss = get_miss_index_list(self.openFilePath, self.DataType, an[0], an[1])
	ann = []
	ann2 = []
	i1 = [0]*int(N)
	i2 = [2]*int(len(miss))
	for j in range(N):	
		date = [item[3] for item in anomalies[j]]
		an_data = [item[1] for item in anomalies[j]]
		max_i = getMaxIndex(an_data)
		an_i = date[max_i]
		start_x = (float)(an_i)/(float)(size)*self.TimeLineLen
		ann.append(start_x)
		ann_zip = zip(i1, ann, ann)
	for k in range(len(miss)):
		an_x  = (float)(miss[k])/(float)(size)*self.TimeLineLen
		ann2.append(an_x)
		ann2_zip = zip(i2, ann2, ann2)
	if (len(miss) > 0):
		ann_zip.extend(ann2_zip)
	data['anomolies'] = ann_zip
	
	start = []
	end = []
	for i in range(N):
		date = [item[3] for item in anomalies[i]]
		start_d = date[0]
		step = len(date)
		stop_d = date[step - 1]
		start_x = (float)(start_d)/(float)(size)*self.TimeLineLen
		stop_x = (float)(stop_d)/(float)(size)*self.TimeLineLen
		start.append(start_x)
		end.append(stop_x)
	time_index = zip(start, end)
        #same as timeframe in comic map, for hightlight, (start date, end date)
	data['dates'] = time_index
        return data
        
    def onCleanData(self, cleanIndex):
        cleanData = [item[3] for item in self.clean]
	self.cleanIndex = cleanIndex
	for i in range(len(self.cleanIndex)):
		lines = open(self.openFilePath, 'r').readlines()
		del lines[cleanData[self.cleanIndex[i]]]
		open(self.openFilePath, 'w').writelines(lines)
		
