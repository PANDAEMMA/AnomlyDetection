import wx
from ADFrame import *

class ADApp(wx.App):
    def OnInit(self):
        self.MakeFrame()
        return True
    
    def MakeFrame(self, event=None):
        mainframe = ADFrame(size=(700, 650))
        mainframe.Show(True)
        self.SetTopWindow(mainframe)
    
if __name__== '__main__':
    app = ADApp(redirect=False) #show error message in console
    app.MainLoop()