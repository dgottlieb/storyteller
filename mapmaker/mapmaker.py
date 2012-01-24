import  wx
import  wx.grid             as  gridlib
import os

#----------------------------------------------------------------------
ID_New  = wx.NewId()
ID_Save = wx.NewId()
ID_SaveAs = wx.NewId()
ID_Close = wx.NewId()
ID_Exit = wx.NewId()
ID_ShowGrid = wx.NewId()


#----------------------------------------------------------------------


class NameSizeDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, pos, size,
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):

        #Precreate, required for creating custom dialog i guess
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)
        self.PostCreate(pre)



        #start building custom dialog
        sizer = wx.BoxSizer(wx.VERTICAL)

        labelHeader = wx.StaticText(self, -1, "Create New Map")
        sizer.Add(labelHeader, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        boxMapName = wx.BoxSizer(wx.HORIZONTAL)

        labelMapName = wx.StaticText(self, -1, "Map Name")
        boxMapName.Add(labelMapName, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        txtMapName = wx.TextCtrl(self, -1, "", size=(80,-1))
        self.txtMapName = txtMapName
        boxMapName.Add(txtMapName, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(boxMapName, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Tiles X:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        txtTilesX = wx.TextCtrl(self, -1, "", size=(80,-1))
        self.txtTilesX = txtTilesX
        txtTilesX.SetHelpText("Numbers Only")
        box.Add(txtTilesX, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Tiles Y:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        txtTilesY = wx.TextCtrl(self, -1, "", size=(80,-1))
        self.txtTilesY = txtTilesY
        txtTilesY.SetHelpText("Numbers Only")
        box.Add(txtTilesY, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        self.SetSizer(sizer)


#This is what allows you to put images into a cell
class MyImageRenderer(wx.grid.PyGridCellRenderer):
     def __init__(self, img):
          wx.grid.PyGridCellRenderer.__init__(self)
          self.img = img
          
         
     def Draw(self, grid, attr, dc, rect, row, col, isSelected):
          
          image = wx.MemoryDC()
          image.SelectObject(self.img)
          dc.SetBackgroundMode(wx.SOLID)
          dc.DrawRectangleRect(rect)
          width, height = 64, 64

          dc.Blit(rect.x, rect.y, width, height, image, 0, 0, wx.COPY, True, 0, 0)


class MapGrid(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)



       
        self.moveTo = None
    
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.SetDefaultColSize(64)
        self.SetDefaultRowSize(64)
        self.CreateGrid(parent.tilesX, parent.tilesY)
        self.EnableDragColSize(False)
        self.EnableDragColMove(False)
        self.EnableDragGridSize(False)
        self.EnableDragRowSize(False)
        self.EnableEditing(False)
        self.EnableCellEditControl(False)
        

        #THis will set the background for avll tiles on creation
        img = wx.Bitmap(tileSelected, wx.BITMAP_TYPE_PNG)
        defaultImageRenderer = MyImageRenderer(img)
        self.SetDefaultRenderer(defaultImageRenderer)
        

    def OnCellLeftClick(self, evt):
       

        img = wx.Bitmap(tileSelected, wx.BITMAP_TYPE_PNG)
        
        imageRenderer = MyImageRenderer(img)
        self.SetCellRenderer(evt.GetRow(), evt.GetCol(), imageRenderer)
        self.SetCellValue(evt.GetRow(), evt.GetCol(), tileID)
        self.ClearSelection()
        self.ForceRefresh()
        evt.Skip()


#This is the 'Tile Window' for choosing whhich tile to place.
class TileGrid(wx.Frame): ##, mixins.GridAutoEditMixin):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        
        self.grid = gridlib.Grid(self, 1, wx.Point(0,0),  self.GetSize(),wx.WANTS_CHARS, "Test")
        self.grid.moveTo = None

        
        self.grid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.grid.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectChange)
        self.grid.SetDefaultColSize(64)
        self.grid.SetDefaultRowSize(64)
        
        self.grid.SetColLabelSize(0)
        self.grid.SetRowLabelSize(0)
        self.grid.CreateGrid(20, 2)
        self.grid.SetColSize(1, 26)
        self.grid.EnableDragColSize(False)
        self.grid.EnableDragColMove(False)
        self.grid.EnableDragGridSize(False)
        self.grid.EnableDragRowSize(False)
        self.grid.EnableEditing(False)
        self.grid.EnableCellEditControl(False)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows )
      
        self.grid.SetSelectionBackground(wx.BLACK)
        self.grid.SetDefaultCellFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.grid.SelectRow(0)
        
        #Load images, this will need to be reworked to load from a source
        imgGrass = wx.Bitmap("grass.png", wx.BITMAP_TYPE_PNG)
        
        imageRenderer = MyImageRenderer(imgGrass)
        self.grid.SetCellRenderer(0,0, imageRenderer)
        self.grid.SetCellValue(0,1, "G")
        self.grid.SetCellValue(0,0, "grass.png")
        
        imgWater = wx.Bitmap("water.png", wx.BITMAP_TYPE_PNG)
        imageRenderer = MyImageRenderer(imgWater)
        self.grid.SetCellRenderer(1,0, imageRenderer)
        self.grid.SetCellValue(1,1, "W")
        self.grid.SetCellValue(1,0, "water.png")

        imgDirt = wx.Bitmap("dirt.png", wx.BITMAP_TYPE_PNG)
        imageRenderer = MyImageRenderer(imgDirt)
        self.grid.SetCellRenderer(2,0, imageRenderer)
        self.grid.SetCellValue(2,1, "D")
        self.grid.SetCellValue(2,0, "dirt.png")


        self.grid.ForceRefresh()
        global tileSelected
        tileSelected = self.grid.GetCellValue(0, 0)
        global tileID
        tileID= self.grid.GetCellValue(1, 1)
        
    def OnSelectChange(self, evt):
        global tileSelected
        tileSelected = self.grid.GetCellValue(evt.GetRow(), 0)
        global tileID
        tileID= self.grid.GetCellValue(evt.GetRow(), 1)
        print tileSelected
        

    def OnCellLeftClick(self, evt):
        

        #img = wx.Bitmap("smiles.png", wx.BITMAP_TYPE_PNG)
        
        #imageRenderer = MyImageRenderer(img)
        #self.SetCellRenderer(evt.GetRow(), evt.GetCol(), imageRenderer)
       # self.ClearSelection()
       # self.ForceRefresh() 
        evt.Skip()




class MapWindow(wx.Frame):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)

        #Give Dialog So we know what size to make the map
        dlg = NameSizeDialog(self, -1, "Create Map",  pos = (-1, -1), size =(220, 220),
                            style = wx.DEFAULT_DIALOG_STYLE,useMetal=False,)
        val =dlg.ShowModal()

        self.tilesX = int(dlg.txtTilesX.GetLineText(0))
        self.tilesY = int(dlg.txtTilesY.GetLineText(0))
        self.mapName = dlg.txtMapName.GetLineText(0)


        #Menu Bar Stuff
        menu = wx.Menu()
        menu.Append(ID_Save, "Save")        
        menu.AppendSeparator()
        menu.Append(ID_Close, "Close")
        menubar = wx.MenuBar()
        menubar.Append(menu, "&File")        
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnSave, id=ID_Save)
        self.Bind(wx.EVT_MENU, self.OnClose, id=ID_Close) 
    
    
        #Grid stuff
        self.grid = gridlib.Grid(self, 1, wx.Point(0,0),  self.GetSize(),wx.WANTS_CHARS, "Test")

        self.grid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.grid.SetDefaultColSize(64)
        self.grid.SetDefaultRowSize(64)
        self.grid.CreateGrid(self.tilesX, self.tilesY)
        self.grid.EnableDragColSize(False)
        self.grid.EnableDragColMove(False)
        self.grid.EnableDragGridSize(False)
        self.grid.EnableDragRowSize(False)
        self.grid.EnableEditing(False)
        self.grid.EnableCellEditControl(False)
        

        #THis will set the background for avll tiles on creation
        img = wx.Bitmap(tileSelected, wx.BITMAP_TYPE_PNG)
        defaultImageRenderer = MyImageRenderer(img)
        self.grid.SetDefaultRenderer(defaultImageRenderer)

        #And adding controls to sizer and then the frame
        sizer = wx.BoxSizer()
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Layout()
        dlg.Destroy()


    def OnClose(self, evt):
        self.grid.Destroy()
        self.Destroy()

    def OnSave(self, evt):
        colCount = self.grid.GetNumberCols()
        rowCount = self.grid.GetNumberRows()
	print self.mapName
        print colCount, ", ", rowCount
	output_file = file('./%s.py' % (self.mapName,), 'w')
	output_file.write('string goes here\n')
	output_file.close()
            

    def OnCellLeftClick(self, evt):
       

        img = wx.Bitmap(tileSelected, wx.BITMAP_TYPE_PNG)
        
        imageRenderer = MyImageRenderer(img)
        self.grid.SetCellRenderer(evt.GetRow(), evt.GetCol(), imageRenderer)
        self.grid.SetCellValue(evt.GetRow(), evt.GetCol(), tileID)
        self.grid.ClearSelection()
        self.grid.ForceRefresh()
        evt.Skip()
        
#This is the first window to load
class MyParentFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Storyteller Map Maker", size=(400,53))
         #not used by me.
        self.winCount = 0
        self.SetPosition(wx.Point(300, 0))
        #Create the menu
        menu = wx.Menu()
        menu.Append(ID_New, "&New Map")        
        menu.AppendSeparator()
        menu.Append(ID_Exit, "E&xit")
        menubar = wx.MenuBar()
        menubar.Append(menu, "&File")        
        self.SetMenuBar(menubar)

        #Status Bar(not used yet)
        self.CreateStatusBar()

        
        self.Bind(wx.EVT_MENU, self.OnNewWindow, id=ID_New)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_Exit)

        


        #Make tile window
       # myTup =self.GetClientSize()
        winTools = TileGrid(self, -1, "Tile Window", size=(350, 200), style = wx.DEFAULT_FRAME_STYLE)
       
       # winTools = wx.Window(-1)
        winTools.SetPosition(wx.Point(0,0))
        winTools.SetSize(wx.Size(90, 600))
        
        
      
        
        winTools.SetMaxSize(wx.Size(90, 1000))
        winTools.Show(True)
       # winTools.Maximize()
        #self.SetDimensions(0, 0, 100, 600, sizeFlags = wx.ACCEL_ALTSIZE_AUTO)
        
       # tileGrid = TileGrid(winTools)
      #  ToolWindow = TileWindow(winTools)
    

    
    def OnExit(self, evt):
        self.Close(True)


    def OnNewWindow(self, evt): 

        self.MapName = "Map"

      #  myTup =self.GetClientSize()
       # win = wx.MDIChildFrame(self, -1, "Map")
        win = MapWindow(self, -1, "Map", size=(350, 200), style = wx.DEFAULT_FRAME_STYLE)
        
 
        win.SetPosition(wx.Point(120, 50))
        win.SetSize(wx.Size(600, 600))
          
       # mapwWindow = MapWindow(win)
   
        
        

        
        win.Show(True)




#----------------------------------------------------------------------

if __name__ == '__main__':
    class MyApp(wx.App):
        def OnInit(self):
            wx.InitAllImageHandlers()
            frame = MyParentFrame()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True


    app = MyApp(False)
    app.MainLoop()



