import wx
from FoldPanelBar import *

def GetCollapsedIconData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x8eIDAT8\x8d\xa5\x93-n\xe4@\x10\x85?g\x03\n6lh)\xc4\xd2\x12\xc3\x81\
\xd6\xa2I\x90\x154\xb9\x81\x8f1G\xc8\x11\x16\x86\xcd\xa0\x99F\xb3A\x91\xa1\
\xc9J&\x96L"5lX\xcc\x0bl\xf7v\xb2\x7fZ\xa5\x98\xebU\xbdz\xf5\\\x9deW\x9f\xf8\
H\\\xbfO|{y\x9dT\x15P\x04\x01\x01UPUD\x84\xdb/7YZ\x9f\xa5\n\xce\x97aRU\x8a\
\xdc`\xacA\x00\x04P\xf0!0\xf6\x81\xa0\xf0p\xff9\xfb\x85\xe0|\x19&T)K\x8b\x18\
\xf9\xa3\xe4\xbe\xf3\x8c^#\xc9\xd5\n\xa8*\xc5?\x9a\x01\x8a\xd2b\r\x1cN\xc3\
\x14\t\xce\x97a\xb2F0Ks\xd58\xaa\xc6\xc5\xa6\xf7\xdfya\xe7\xbdR\x13M2\xf9\
\xf9qKQ\x1fi\xf6-\x00~T\xfac\x1dq#\x82,\xe5q\x05\x91D\xba@\xefj\xba1\xf0\xdc\
zzW\xcff&\xb8,\x89\xa8@Q\xd6\xaaf\xdfRm,\xee\xb1BDxr#\xae\xf5|\xddo\xd6\xe2H\
\x18\x15\x84\xa0q@]\xe54\x8d\xa3\xedf\x05M\xe3\xd8Uy\xc4\x15\x8d\xf5\xd7\x8b\
~\x82\x0fh\x0e"\xb0\xad,\xee\xb8c\xbb\x18\xe7\x8e;6\xa5\x89\x04\xde\xff\x1c\
\x16\xef\xe0p\xfa>\x19\x11\xca\x8d\x8d\xe0\x93\x1b\x01\xd8m\xf3(;x\xa5\xef=\
\xb7w\xf3\x1d$\x7f\xc1\xe0\xbd\xa7\xeb\xa0(,"Kc\x12\xc1+\xfd\xe8\tI\xee\xed)\
\xbf\xbcN\xc1{D\x04k\x05#\x12\xfd\xf2a\xde[\x81\x87\xbb\xdf\x9cr\x1a\x87\xd3\
0)\xba>\x83\xd5\xb97o\xe0\xaf\x04\xff\x13?\x00\xd2\xfb\xa9`z\xac\x80w\x00\
\x00\x00\x00IEND\xaeB`\x82' 

def GetCollapsedIconBitmap():
    return wx.BitmapFromImage(GetCollapsedIconImage())

def GetCollapsedIconImage():
    import cStringIO
    stream = cStringIO.StringIO(GetCollapsedIconData())
    return wx.ImageFromStream(stream)

#----------------------------------------------------------------------
def GetExpandedIconData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x9fIDAT8\x8d\x95\x93\xa1\x8e\xdc0\x14EO\xb2\xc4\xd0\xd2\x12\xb7(mI\
\xa4%V\xd1lQT4[4-\x9a\xfe\xc1\xc2|\xc6\xc2~BY\x83:A3E\xd3\xa0*\xa4\xd2\x90H!\
\x95\x0c\r\r\x1fK\x81g\xb2\x99\x84\xb4\x0fY\xd6\xbb\xc7\xf7>=\'Iz\xc3\xbcv\
\xfbn\xb8\x9c\x15 \xe7\xf3\xc7\x0fw\xc9\xbc7\x99\x03\x0e\xfbn0\x99F+\x85R\
\x80RH\x10\x82\x08\xde\x05\x1ef\x90+\xc0\xe1\xd8\ryn\xd0Z-\\A\xb4\xd2\xf7\
\x9e\xfbwoF\xc8\x088\x1c\xbbae\xb3\xe8y&\x9a\xdf\xf5\xbd\xe7\xfem\x84\xa4\
\x97\xccYf\x16\x8d\xdb\xb2a]\xfeX\x18\xc9s\xc3\xe1\x18\xe7\x94\x12cb\xcc\xb5\
\xfa\xb1l8\xf5\x01\xe7\x84\xc7\xb2Y@\xb2\xcc0\x02\xb4\x9a\x88%\xbe\xdc\xb4\
\x9e\xb6Zs\xaa74\xadg[6\x88<\xb7]\xc6\x14\x1dL\x86\xe6\x83\xa0\x81\xba\xda\
\x10\x02x/\xd4\xd5\x06\r\x840!\x9c\x1fM\x92\xf4\x86\x9f\xbf\xfe\x0c\xd6\x9ae\
\xd6u\x8d \xf4\xf5\x165\x9b\x8f\x04\xe1\xc5\xcb\xdb$\x05\x90\xa97@\x04lQas\
\xcd*7\x14\xdb\x9aY\xcb\xb8\\\xe9E\x10|\xbc\xf2^\xb0E\x85\xc95_\x9f\n\xaa/\
\x05\x10\x81\xce\xc9\xa8\xf6><G\xd8\xed\xbbA)X\xd9\x0c\x01\x9a\xc6Q\x14\xd9h\
[\x04\xda\xd6c\xadFkE\xf0\xc2\xab\xd7\xb7\xc9\x08\x00\xf8\xf6\xbd\x1b\x8cQ\
\xd8|\xb9\x0f\xd3\x9a\x8a\xc7\x08\x00\x9f?\xdd%\xde\x07\xda\x93\xc3{\x19C\
\x8a\x9c\x03\x0b8\x17\xe8\x9d\xbf\x02.>\x13\xc0n\xff{PJ\xc5\xfdP\x11""<\xbc\
\xff\x87\xdf\xf8\xbf\xf5\x17FF\xaf\x8f\x8b\xd3\xe6K\x00\x00\x00\x00IEND\xaeB\
`\x82' 

def GetExpandedIconBitmap():
    return wx.BitmapFromImage(GetExpandedIconImage())

def GetExpandedIconImage():
    import cStringIO
    stream = cStringIO.StringIO(GetExpandedIconData())
    return wx.ImageFromStream(stream)

#----------------------------------------------------------------------
def GetMondrianData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82' 

def GetMondrianBitmap():
    return wx.BitmapFromImage(GetMondrianImage())

def GetMondrianImage():
    import cStringIO
    stream = cStringIO.StringIO(GetMondrianData())
    return wx.ImageFromStream(stream)

def GetMondrianIcon():
    icon = wx.EmptyIcon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon

# ----------------------------------------------------------------------------
# Beginning Of Extended Demo
# ----------------------------------------------------------------------------

class Extended(wx.Frame):
    
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(700,650), style=wx.DEFAULT_FRAME_STYLE):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self._flags = 0
        
        self.SetIcon(GetMondrianIcon())
        self.SetMenuBar(self.CreateMenuBar())

        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-4, -3])
        self.statusbar.SetStatusText("Tsung Tai Yeh @ 14 Oct 2013", 1)

        self._leftWindow1 = wx.SashLayoutWindow(self, 101, wx.DefaultPosition,
                                                wx.Size(200, 1000), wx.NO_BORDER |
                                                wx.SW_3D | wx.CLIP_CHILDREN)

        self._leftWindow1.SetDefaultSize(wx.Size(200, 1000))
        self._leftWindow1.SetOrientation(wx.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)

        self._pnl = 0

        # will occupy the space not used by the Layout Algorithm
        self.remainingSpace = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
        self.remainingSpace.SetBackgroundColour(wx.WHITE)

        self.ID_WINDOW_TOP = 100
        self.ID_WINDOW_LEFT1 = 101
        self.ID_WINDOW_RIGHT1 = 102
        self.ID_WINDOW_BOTTOM = 103
    
        self._leftWindow1.Bind(wx.EVT_SASH_DRAGGED_RANGE, self.OnFoldPanelBarDrag,
                               id=100, id2=103)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.ReCreateFoldPanel(0)
        

    def OnSize(self, event):

        wx.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        event.Skip()
        

    def OnQuit(self, event):
 
        self.Destroy()


    def OnAbout(self, event):

        msg = "This Is The About Anomaly Detection and Data Clean Tool.\n\n" + \
              "Author: Tsung Tai Yeh @ Purdue\n\n" + \
              "Welcome To wxPython " + wx.VERSION_STRING + "!!"
              
        dlg = wx.MessageDialog(self, msg, "Data Clean Tool",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False, "Verdana"))
        dlg.ShowModal()
        dlg.Destroy()



    def OnFoldPanelBarDrag(self, event):

        if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
            return

        if event.GetId() == self.ID_WINDOW_LEFT1:
            self._leftWindow1.SetDefaultSize(wx.Size(event.GetDragRect().width, 1000))


        # Leaves bits of itself behind sometimes
        wx.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        self.remainingSpace.Refresh()

        event.Skip()
        

    def ReCreateFoldPanel(self, fpb_flags):

        # delete earlier panel
        self._leftWindow1.DestroyChildren()

        # recreate the foldpanelbar

        self._pnl = FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                 wx.Size(-1,-1), FPB_DEFAULT_STYLE, fpb_flags)

        Images = wx.ImageList(16,16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())
            
        item = self._pnl.AddFoldPanel("Data Source", collapsed=False,
                                      foldIcons=Images)

        self._pnl.AddFoldPanelWindow(item, wx.StaticText(item, -1, "Select a file!"), FPB_ALIGN_WIDTH, 5, 20) 

        
        button1 = wx.Button(item, wx.ID_ANY, "Apply To All")
        button1.Bind(wx.EVT_BUTTON, self.OnExpandMe)
        self._pnl.AddFoldPanelWindow(item, button1)


        style = self._pnl.GetCaptionStyle(item)

        # Metric Options

        item = self._pnl.AddFoldPanel("Metrics", False, foldIcons=Images)

        self.ID_USE_VGRADIENT = wx.NewId()
        self.ID_USE_HGRADIENT = wx.NewId()
        self.ID_USE_SINGLE = wx.NewId()
        self.ID_USE_RECTANGLE = wx.NewId()
        self.ID_USE_FILLED_RECTANGLE = wx.NewId()
        
        currStyle =  wx.RadioButton(item, self.ID_USE_VGRADIENT, "&Temperature")
        self._pnl.AddFoldPanelWindow(item, currStyle, FPB_ALIGN_WIDTH,
                                     FPB_DEFAULT_SPACING, 10)
        
        currStyle.SetValue(True)

        radio1 = wx.RadioButton(item, self.ID_USE_HGRADIENT, "&Humidity")
        radio2 = wx.RadioButton(item, self.ID_USE_SINGLE, "&Air Pressure")

        currStyle.Bind(wx.EVT_RADIOBUTTON, self.OnStyleChange)
        radio1.Bind(wx.EVT_RADIOBUTTON, self.OnStyleChange)
        radio2.Bind(wx.EVT_RADIOBUTTON, self.OnStyleChange)
        
        self._pnl.AddFoldPanelWindow(item, radio1, FPB_ALIGN_WIDTH, FPB_DEFAULT_SPACING, 10) 
        self._pnl.AddFoldPanelWindow(item, radio2, FPB_ALIGN_WIDTH, FPB_DEFAULT_SPACING, 10) 

        self._pnl.AddFoldPanelSeparator(item)

	# Time range option
	item = self._pnl.AddFoldPanel("Time Range", False, foldIcons=Images)

	self._pnl.AddFoldPanelWindow(item, wx.StaticText(item, -1, "Start time"), FPB_ALIGN_WIDTH, 5, 20) 
	self._pnl.AddFoldPanelWindow(item, wx.TextCtrl(item, -1, "Comments"),
                                     FPB_ALIGN_WIDTH, FPB_DEFAULT_SPACING, 10)
	self._pnl.AddFoldPanelWindow(item, wx.StaticText(item, -1, "End time"), FPB_ALIGN_WIDTH, 5, 20)         
        self._pnl.AddFoldPanelWindow(item, wx.TextCtrl(item, -1, "Comments"),
                                     FPB_ALIGN_WIDTH, FPB_DEFAULT_SPACING, 10)
	
        # Misc analysis methods
        cs = CaptionBarStyle()
        cs.SetCaptionStyle(CAPTIONBAR_RECTANGLE)

        item = self._pnl.AddFoldPanel("Misc Stuff", collapsed=True, foldIcons=Images,cbstyle=cs)

	self.ID_USE_RECTANGLE = wx.NewId()
        self.ID_USE_FILLED_RECTANGLE = wx.NewId()

	currStyle =  wx.RadioButton(item, self.ID_USE_RECTANGLE, "&Corr. analysis")
        self._pnl.AddFoldPanelWindow(item, currStyle, FPB_ALIGN_WIDTH,
                                     FPB_DEFAULT_SPACING, 10)

        currStyle.SetValue(True)

        radio1 = wx.RadioButton(item, self.ID_USE_HGRADIENT, "&Slope Analysis")
        radio2 = wx.RadioButton(item, self.ID_USE_SINGLE, "&Model-base Analysis")

        currStyle.Bind(wx.EVT_RADIOBUTTON, self.OnStyleChange)
        radio1.Bind(wx.EVT_RADIOBUTTON, self.OnStyleChange)
        radio2.Bind(wx.EVT_RADIOBUTTON, self.OnStyleChange)

        self._pnl.AddFoldPanelWindow(item, radio1, FPB_ALIGN_WIDTH, FPB_DEFAULT_SPACING, 10)
        self._pnl.AddFoldPanelWindow(item, radio2, FPB_ALIGN_WIDTH, FPB_DEFAULT_SPACING, 10)

        self._pnl.AddFoldPanelSeparator(item)
	

        button2 = wx.Button(item, wx.NewId(), "Collapse All")        
        self._pnl.AddFoldPanelWindow(item, button2) 
        self._pnl.AddFoldPanelWindow(item, wx.StaticText(item, -1, "Enter Some Comments"),
                                     FPB_ALIGN_WIDTH, 5, 20) 
        self._pnl.AddFoldPanelWindow(item, wx.TextCtrl(item, -1, "Comments"),
                                     FPB_ALIGN_WIDTH, FPB_DEFAULT_SPACING, 10)

        button2.Bind(wx.EVT_BUTTON, self.OnCollapseMe)
        self.radiocontrols = [currStyle, radio1, radio2]
        
        self._leftWindow1.SizeWindows()
        

    def OnCollapseMe(self, event):

        for i in range(0, self._pnl.GetCount()):
            item = self._pnl.GetFoldPanel(i)
            self._pnl.Collapse(item)

    def OnExpandMe(self, event):

	style = CaptionBarStyle()

	counter = 0
        for items in self.radiocontrols:
            if items.GetValue():
                break
            counter = counter + 1

        if counter == 0:
            mystyle = CAPTIONBAR_GRADIENT_V
        elif counter == 1:
            mystyle = CAPTIONBAR_GRADIENT_H
        elif counter == 2:
            mystyle = CAPTIONBAR_SINGLE
        elif counter == 3:
            mystyle = CAPTIONBAR_RECTANGLE
        else:
            mystyle = CAPTIONBAR_FILLED_RECTANGLE

        style.SetCaptionStyle(mystyle)
        self._pnl.ApplyCaptionStyleAll(style)


    def CreateMenuBar(self, with_window=False):

        # Make a menubar
        file_menu = wx.Menu()

        FPBTEST_QUIT = wx.NewId()
        FPBTEST_ABOUT = wx.NewId()

        file_menu.Append(FPBTEST_QUIT, "&Exit")
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")

	help_menu = wx.Menu()
        help_menu.Append(FPBTEST_ABOUT, "&About")

	menu_bar.Append(help_menu, "&Help")
        self.Bind(wx.EVT_MENU, self.OnQuit, id=FPBTEST_QUIT)
	self.Bind(wx.EVT_MENU, self.OnAbout, id=FPBTEST_ABOUT)

        return menu_bar
    def OnStyleChange(self, event):

        style = CaptionBarStyle()

        eventid = event.GetId()

        if eventid == self.ID_USE_HGRADIENT:
            style.SetCaptionStyle(CAPTIONBAR_GRADIENT_H)

        elif eventid == self.ID_USE_VGRADIENT:
            style.SetCaptionStyle(CAPTIONBAR_GRADIENT_V)

        elif eventid == self.ID_USE_SINGLE:
            style.SetCaptionStyle(CAPTIONBAR_SINGLE)

        elif eventid == self.ID_USE_RECTANGLE:
            style.SetCaptionStyle(CAPTIONBAR_RECTANGLE)

        elif eventid == self.ID_USE_FILLED_RECTANGLE:
            style.SetCaptionStyle(CAPTIONBAR_FILLED_RECTANGLE)

        else:
		raise "ERROR: Undefined Style Selected For CaptionBar: " + repr(eventid)

        col1 = wx.Colour(self._rslider1.GetValue(), self._gslider1.GetValue(),
                         self._bslider1.GetValue())
        col2 = wx.Colour(self._rslider2.GetValue(), self._gslider2.GetValue(),
                         self._bslider2.GetValue())

        style.SetFirstColour(col1)
        style.SetSecondColour(col2)

        if self._single.GetValue():
            item = self._pnl.GetFoldPanel(1)
            self._pnl.ApplyCaptionStyle(item, style)
        else:
            self._pnl.ApplyCaptionStyleAll(style)


def main():

    MyApp = wx.PySimpleApp()
    wx.InitAllImageHandlers()

    Frame = Extended(None, -1, title="Data Clean Tool", pos=wx.Point(50, 50),
                     size=wx.Size(700, 650))

    Frame.CenterOnScreen()    
    MyApp.SetTopWindow(Frame)

    Frame.Show()
    MyApp.MainLoop()


if __name__ == "__main__":
    
    main()

    

