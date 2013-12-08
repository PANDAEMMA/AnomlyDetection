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
	self.TimeLineLen = 60
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
        file_menu.Append(MENU_QUIT,"&Exit")
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
            """self.dangerData.append({'year':1997,'year_data':(0.23, 0.34, 0.06), 
            'month_data':[(0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3), 
            (0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3), (0.23, 0.34, 0.14),
            (0.21, 0.09, 0.07), (0.67, 0.11, 0.3), (0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3)]})
            self.dangerData.append({'year':1998,'year_data':(0.03, 0.14, 0.56), 
            'month_data':[(0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3), 
            (0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3), (0.23, 0.34, 0.14),
            (0.21, 0.09, 0.07), (0.67, 0.11, 0.3), (0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3)]})
            self.dangerData.append({'year':1999,'year_data':(0.13, 0.34, 0.56), 
            'month_data':[(0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3), 
            (0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3), (0.23, 0.34, 0.14),
            (0.21, 0.09, 0.07), (0.67, 0.11, 0.3), (0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3)]})
            self.dangerData.append({'year':2000,'year_data':(0.33, 0.04, 0.56), 
            'month_data':[(0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3), 
            (0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3), (0.23, 0.34, 0.14),
            (0.21, 0.09, 0.07), (0.67, 0.11, 0.3), (0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3)]})
            self.dangerData.append({'year':2001,'year_data':(0.03, 0.24, 0.06), 
            'month_data':[(0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3), 
            (0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3), (0.23, 0.34, 0.14),
            (0.21, 0.09, 0.07), (0.67, 0.11, 0.3), (0.23, 0.34, 0.14),(0.21, 0.09, 0.07), (0.67, 0.11, 0.3)]})"""
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
        checkboxes = self.DataPanel.attributePanel.GetChildren()
        if attr == 'temprature':
            checkboxes[0].SetValue(True)
        if attr == 'humidity':
            checkboxes[1].SetValue(True)
        if attr == 'airPressure':
            checkboxes[2].SetValue(True)
            
        #{labels:[list], anomolies: [list]}
        # the data part is the information you need to give me
        data = dict()
        #1st and last should be the start and end time, if no lable, can be like [(0, '')]
        #data['labels'] = [(0,'01/01/1997'), (15, '01/15/1997'), (31, '02/01/1997'), (46, '02/15/1997'), (60, '02/28/1997')]
        data['labels'] = self.Pick_xaxis()
        #0: extremes, 1: glitches, (type, xstart, xend), the index must be the same as comicmap data, #pass in source IDs
        data['anomolies'] = [(0,21,21), (0,19,19), (0,2,2), (0,9,9), (0,26,26), (0,33,33), (0,36,36), (0,42,42), (0,11,11)]
        #same as timeframe in comic map, for hightlight, (start date, end date)
 
	#data['dates'] = [(20, 24), (14, 20), (1, 5), (5, 10), (24, 30), (30, 35), (35, 39), (39, 43), (10, 14)]
        return data
        
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
        #print data
        #data (year, month), if select the whole year, month = -1
        #----------------TODO-------------------
        #backend function AnalyzeData can return a tuple
        #self.anomalies , self.overviewData, self.cleanData = AnalyzeData(File, self.DataType, (year, month))
	self.anomalies = AnalyzeData(self.openFilePath, self.DataType, data[0], data[1])
	self.overviewData = self.cleanData = data
        self.cleanData = self.PackCleanData(self.cleanData)
        self.anomaliesData = self.PackDataToDraw(self.anomalies)
        self.timelineData = self.PackTimelineData(self.overviewData, self.anomalies)
        self.DrawComicMap(self.anomaliesData)
        self.DrawTimeline(self.timelineData)
        
    def PackCleanData(self, data):
        #---------TODO/Done--------
        #If the data backend generated is the same as my data structure, no packing work needed here, just return the data
        #otherwise, reformat the data as my data structure
        
        #mimic Data for clean data
        self.cleanData = dict()
        self.cleanData['labels'] = ['Type', 'Value', 'Date']
	self.cleanData['data'] = CleanAnalyze(self.openFilePath, self.DataType, data[0], data[1])
        #0: extremes, 1: glitches, 2: Missing
        #self.cleanData['data'] = [(0, 33.4, "01/02/1997"), (0, '27','03/04/1988'),(0, '25', '06/07/2013'),
        #                        (1, 33.4, "01/03/1997"), (1, '66.8','03/08/1988'),(1, '77.4', '09/07/2013'),
        #                        (2, '', "01/05/1997"), (2, '','08/04/1988'),(2, '', '06/09/2013'),]
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
            points = zip(index, an_data)
    
            length_index = len(index)
            # std cal.
            std = []
            aa = stdcal(an_data, length_index)
            std.append('std:'+ (str)(aa))
            # avg cal.
            average = []
            av = avg(an_data, length_index)
            average.append('mean:' + (str)(av))
            # start date
            start_date = []
            start_date.append('sdate:'+ (str)(anomalies[i][0][2]))
            # end date
            end_date = []
            end_date.append('edate:' + (str)(anomalies[i][length_index - 1][2]))
            label = zip(std, average, start_date, end_date)
            # add std, avg, and date into label
            dic['labels'] = label
            # add anomaly data
            dic['points'] = points
            # add extreme data
            maxdata = getMaxIndex(an_data)
            anomaly_data.append(maxdata)
            #mindata = getMinIndex(an_data)
            #anomaly_data.append(mindata)
            dic['anomolies'] = anomaly_data
            data.append([dic])
            anomaly_data = []
            
        return data

        #mimic Data
        #genData mimic data here, will by read later
        '''list = []
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
        dic['labels'] = [("test")]
        dic1['labels'] = [("test")]
        dic2['labels'] = [("test")]
        dic3['labels'] = [("test")]
        list.append([dic])
        list.append([dic1])
        list.append([dic2])
        list.append([dic3])
        return list'''

    def PackTimelineData(self, an, anomalies):
        #---------TODO/Done--------
        #If the data backend generated is the same as my data structure, no packing work needed here, just return the data
        #otherwise, reformat the data as my data structure
	chunk_num = 5
	x_axis = get_x_axis(self.openFilePath, self.DataType, an[0], an[1], self.TimeLineLen, chunk_num)
        #mimic Data
        #{labels:[list], anomolies: [list]}
        # the data part is the information you need to give me
        data = dict()
        #1st and last should be the start and end time, if no lable, can be like [(0, '')]
	data['labels'] = x_axis

	N = len(anomalies)
	size = get_year_size(self.openFilePath, self.DataType, an[0])
	miss = get_miss_index_list(self.openFilePath, self.DataType, an[0], an[1])
	ann = []
	ann2 = []
	i1 = [0]*int(N)
	i2 = [1]*int(len(miss))
	for j in range(N):	
		date = [item[3] for item in anomalies[j]]
		an_data = [item[1] for item in anomalies[j]]
		max_i = getMaxIndex(an_data)
		an_i = date[max_i]
		an_x = start_x = (int)(((float)(an_i)/(float)(size))*self.TimeLineLen)
		ann.append(an_i)
		ann_zip = zip(i1, ann, ann)
	for k in range(len(miss)):
		an_x = start_x = (int)(((float)(miss[k])/(float)(size))*self.TimeLineLen)

		ann2.append(an_x)
		ann2_zip = zip(i2, ann2, ann2)
	ann_zip.extend(ann2_zip)
	data['anomolies'] = ann_zip
	#data['labels'] = [(0,'01/01/1997'), (15, '01/15/1997'), (31, '02/01/1997'), (46, '02/15/1997'), (60, '02/28/1997')]
        #0: extremes, 1: glitches, (type, xstart, xend), the index must be the same as comicmap data, #pass in source IDs
        #data['anomolies'] = [(0,21,21), (0,19,19), (0,2,2), (0,9,9), (0,26,26), (0,33,33), (0,36,36), (0,42,42), (0,11,11)]
	
	start = []
	end = []
	for i in range(N):
		date = [item[3] for item in anomalies[i]]
		start_d = date[0]
		step = len(date)
		stop_d = date[step - 1]
		start_x = (int)(((float)(start_d)/(float)(size))*self.TimeLineLen)
		stop_x = (int)(((float)(stop_d)/(float)(size))*self.TimeLineLen)
		start.append(start_x)
		end.append(stop_x)
	time_index = zip(start, end)
        #same as timeframe in comic map, for hightlight, (start date, end date)
	data['date'] = time_index
	print time_index
        #data['dates'] = [(20, 24), (14, 20), (1, 5), (5, 10), (24, 30), (30, 35), (35, 39), (39, 43), (10, 14)]
        return data
        
    def onCleanData(self, cleanIndex):
        self.cleanIndex = cleanIndex
        #print self.cleanIndex
        #----------------TODO-------------------
        #backend function CleanSourceData take in a array of indexes of the original anomalies that needs to be removed
        #CleanSourceData(self.cleanIndex)
