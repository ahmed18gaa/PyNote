import wx
import wx.stc as stc
import wx.lib.dialogs
import os

faces = {
    'times': 'Times New Roman',
    'mono': 'Courier New',
    'helv': 'Arial',
    'other': 'Comic Sans MS',
    'size': 14,
}

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))

        self.dirname = ''
        self.filename = ''
        self.leftMarginWidth = 35
        self.lineNumbersEnabled = True

        # Initialize text editor control
        self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

        # Apply BoxSizer so editor fills the entire window
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.control, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # Reset all styles and force light foreground (white) & dark background
        self.control.StyleResetDefault()
        self.control.StyleSetSpec(stc.STC_STYLE_DEFAULT, f"face:{faces['mono']},size:{faces['size']},fore:#FFFFFF,back:#1E1E1E")
        self.control.StyleClearAll()

        # Set specific line number style
        self.control.StyleSetSpec(stc.STC_STYLE_LINENUMBER, f"face:{faces['mono']},size:10,fore:#AAAAAA,back:#2B2B2B")

        # Set caret/cursor color to white so it's clearly visible
        self.control.SetCaretForeground(wx.Colour(255, 255, 255))

        # Zoom keyboard shortcuts
        self.control.CmdKeyAssign(ord('='), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.control.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        # Margins & Line Numbers
        self.control.SetViewWhiteSpace(False)
        self.control.SetMargins(5, 0)
        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.control.SetMarginWidth(1, self.leftMarginWidth)

        # Status Bar
        self.CreateStatusBar()
        self.StatusBar.SetBackgroundColour((220, 220, 220))

        # Menu Bar setup
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

        # Menu bindings
        self.Bind(wx.EVT_MENU, self.OnNew, menuNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnClose, menuClose)

        self.Bind(wx.EVT_MENU, self.OnUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.OnRedo, menuRedo)
        self.Bind(wx.EVT_MENU, self.OnSelectAll, menuSelectAll)
        self.Bind(wx.EVT_MENU, self.OnCopy, menuCopy)
        self.Bind(wx.EVT_MENU, self.OnCut, menuCut)
        self.Bind(wx.EVT_MENU, self.OnPaste, menuPaste)

        self.Bind(wx.EVT_MENU, self.OnToggleLineNumbers, menuLineNumbers)

        self.Bind(wx.EVT_MENU, self.OnHowTo, menuHowTo)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        # Key & Mouse bindings for cursor updates
        self.control.Bind(wx.EVT_KEY_UP, self.UpdateLineCol)
        self.control.Bind(wx.EVT_LEFT_UP, self.UpdateLineCol)
        self.control.Bind(wx.EVT_CHAR, self.OnCharEvent)

        self.Show()
        self.UpdateLineCol()

    def OnNew(self, e):
        self.filename = ''
        self.control.SetValue('')

    def OnOpen(self, e):
        try:
            dig = wx.FileDialog(self, "Open File", self.dirname, "", "*.*", wx.FD_OPEN)
            if dig.ShowModal() == wx.ID_OK:
                self.filename = dig.GetFilename()
                self.dirname = dig.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'r')
                self.control.SetValue(f.read())
                f.close()
            dig.Destroy()
        except:
            dig = wx.MessageDialog(self, "Error opening file", "Error", wx.OK | wx.ICON_ERROR)
            dig.ShowModal()
            dig.Destroy()

    def OnSave(self, e):
        try:
            f = open(os.path.join(self.dirname, self.filename), 'w')
            f.write(self.control.GetValue())
            f.close()
        except:
            try:
                dig = wx.FileDialog(self, "Save File", self.dirname, "", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if dig.ShowModal() == wx.ID_OK:
                    self.filename = dig.GetFilename()
                    self.dirname = dig.GetDirectory()
                    f = open(os.path.join(self.dirname, self.filename), 'w')
                    f.write(self.control.GetValue())
                    f.close()
                dig.Destroy()
            except:
                pass

    def OnSaveAs(self, e):
        try:
            dig = wx.FileDialog(self, "Save File", self.dirname, "", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if dig.ShowModal() == wx.ID_OK:
                self.filename = dig.GetFilename()
                self.dirname = dig.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'w')
                f.write(self.control.GetValue())
                f.close()
            dig.Destroy()
        except:
            pass

    def OnClose(self, e):
        self.Close(True)

    def OnUndo(self, e):
        self.control.Undo()

    def OnRedo(self, e):
        self.control.Redo()

    def OnSelectAll(self, e):
        self.control.SelectAll()

    def OnCopy(self, e):
        self.control.Copy()

    def OnCut(self, e):
        self.control.Cut()

    def OnPaste(self, e):
        self.control.Paste()

    def OnToggleLineNumbers(self, e):
        if self.lineNumbersEnabled:
            self.control.SetMarginWidth(1, 0)
            self.lineNumbersEnabled = False
        else:
            self.control.SetMarginWidth(1, self.leftMarginWidth)
            self.lineNumbersEnabled = True

    def OnHowTo(self, e):
        dig = wx.lib.dialogs.ScrolledMessageDialog(self, "How to use PyNote:\n\n1. To create a new document, go to File > New.\n2. To open an existing document, go to File > Open.\n3. To save the current document, go to File > Save or File > Save As.\n4. Use the Edit menu for undo, redo, copy, cut, and paste operations.\n5. Toggle line numbers in the editor via Preferences > Toggle Line Numbers.\n6. For more information about this application, go to Help > About.", "How To", size=(550, 250))
        dig.ShowModal()
        dig.Destroy()

    def OnAbout(self, e):
        dig = wx.MessageDialog(self, "PyNote\n\nA simple text editor built with Python and wxPython.\n\nCreated by Ahmed Alabbasi.\nLicensed under the MIT License.\nLinkedin: https://www.linkedin.com/in/ahmed-al-abbasi-1090a2195/\n\n GitHub: https://github.com/ahmed18gaa/PyNote", "About PyNote", wx.OK | wx.ICON_INFORMATION)
        dig.ShowModal()
        dig.Destroy()

    # Update the status bar with the current line and column numbers
    def UpdateLineCol(self, event=None):
        line = self.control.GetCurrentLine() + 1
        column = self.control.GetColumn(self.control.GetCurrentPos())
        stat = "Line: %s, Column: %s" % (line, column)
        self.StatusBar.SetStatusText(stat, 0)
        if event:
            event.Skip()

    def OnCharEvent(self, event):
        keycode = event.GetKeyCode()
        altDown = event.AltDown() or event.MetaDown()  # Supports Option key on macOS
        
        if keycode == 14:  # (Ctrl | control)+N
            self.OnNew(event)
        elif keycode == 15:  # (Ctrl | control)+O
            self.OnOpen(event)
        elif keycode == 19:  # (Ctrl | control)+S
            self.OnSave(event)
        elif (altDown and (keycode == 115 or keycode == 83 or keycode == 223)):  # Alt/Option + S (115='s', 83='S', 223='ß' on macOS)
            self.OnSaveAs(event)
        elif keycode == 23:  # (Ctrl | control)+W
            self.OnClose(event)
        elif keycode == 340:  # F1 | fn+F1
            self.OnHowTo(event)
        elif keycode == 341:  # F2 | fn+F2
            self.OnAbout(event)
        else:
            event.Skip()

app = wx.App()
frame = MainWindow(None, "PyNote")
app.MainLoop()