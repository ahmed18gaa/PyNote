import wx
import wx.stc as stc
import wx.lib.dialogs

faces = {
    'times': 'Times New Roman',
    'mono': 'Courier New',
    'helv': 'Arial',
    'other': 'Comic Sans MS',
    'size': 10,
    'size2': 8,
}

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.leftMarginWidth = 25

        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

        self.control.CmdKeyAssign(ord('='), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN) # (Ctrl or command) + (=) to zoom in
        self.control.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT) # (Ctrl or command) + (-) to zoom out

        self.control.SetViewWhiteSpace(False)
        self.control.SetMargins(5,0)
        self.control.SetMarginType(1,stc.STC_MARGIN_NUMBER)
        self.control.SetMarginWidth(1, self.leftMarginWidth)

        self.CreateStatusBar()
        self.StatusBar.SetBackgroundColour((220, 220, 220))

        filemenu = wx.Menu()
        menuNew = filemenu.Append(wx.ID_NEW, "&New", "Create a new document")
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open an existing document")
        menuSave = filemenu.Append(wx.ID_SAVE, "&Save", "Save the current document")
        menuSaveAs = filemenu.Append(wx.ID_SAVEAS, "Save &As", "Save the current document under a new name")
        filemenu.AppendSeparator()
        menuClose = filemenu.Append(wx.ID_CLOSE, "&Close", "Close the application")

        editmenu = wx.Menu()
        menuUndo = editmenu.Append(wx.ID_UNDO, "&Undo", "Undo the last action")
        menuRedo = editmenu.Append(wx.ID_REDO, "&Redo", "Redo the last undone action")
        editmenu.AppendSeparator()
        menuSelectAll = editmenu.Append(wx.ID_SELECTALL, "Select &All", "Select all text in the document")
        menuCopy = editmenu.Append(wx.ID_COPY, "&Copy", "Copy the selected text to the clipboard")
        menuCut = editmenu.Append(wx.ID_CUT, "Cu&t", "Cut the selected text to the clipboard")
        menuPaste = editmenu.Append(wx.ID_PASTE, "&Paste", "Paste text from the clipboard into the document")

        preferencesMenu = wx.Menu()
        menuLineNumbers = preferencesMenu.Append(wx.ID_ANY, "Toggle &Line Numbers", "Show or hide line numbers in the editor")

        helpMenu = wx.Menu()
        menuHowTo = helpMenu.Append(wx.ID_ANY, "&How To", "Instructions on how to use the application")
        helpMenu.AppendSeparator()
        menuAbout = helpMenu.Append(wx.ID_ANY, "&About", "Information about this application")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(preferencesMenu, "&Preferences")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)

        self.Show()

app = wx.App()
frame = MainWindow(None, "PyNote")
app.MainLoop()