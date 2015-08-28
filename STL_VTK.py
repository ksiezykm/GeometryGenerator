"""
Created on Fri Dec 13 11:45:03 2013
 
@author: Sukhbinder Singh
 
VTL STL File reader with wxPython GUI
 
"""
import wx
import vtk
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor

e_a = 10
a_a = 70

pSource = [-5.0,1.0,1.0]
pTarget = [5.0,-1.0,-0.5]

xmin = -20.0
xmax = 20.0
ymin = -20.0
ymax = 20.0
zmin = -20.0
zmax = 60.0

pp1 = [xmin,ymin,zmin]
pp2 = [xmax,ymin,zmin]
pp3 = [xmin,ymax,zmin]
pp4 = [xmax,ymax,zmin]
pp5 = [xmin,ymax,zmax]
pp6 = [xmax,ymax,zmax]
pp7 = [xmin,ymin,zmax]
pp8 = [xmax,ymin,zmax]

def addPoint(renderer, p, radius=1.0, color=[0.0,0.0,0.0]):
    point = vtk.vtkSphereSource()
    point.SetCenter(p)
    point.SetRadius(radius)
    point.SetPhiResolution(10)
    point.SetThetaResolution(10)
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(point.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    
    renderer.AddActor(actor)
    
def addLine(renderer, p1, p2, color=[0.0,0.0,1.0]):
    line = vtk.vtkLineSource()
    line.SetPoint1(p1)
    line.SetPoint2(p2)
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(line.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    
    renderer.AddActor(actor)
    
def IsInside(pX,pY,pZ,mesh):
    select = vtk.vtkSelectEnclosedPoints()
    select.SetSurface(mesh)
            
    pts = vtk.vtkPoints()
    pts.InsertNextPoint(pX,pY,pZ)
    pts_pd = vtk.vtkPolyData()
    pts_pd.SetPoints(pts)
    select.SetInput(pts_pd)
    select.Update()
    print select.IsInside(0)
            #select.Update()
    
 
class p1(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
         
        #to interact with the scene using the mouse use an instance of vtkRenderWindowInteractor.
        self.widget = wxVTKRenderWindowInteractor(self, -1)
        self.widget.Enable(1)
        self.widget.AddObserver("ExitEvent", lambda o,e,f=self: f.Close())
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.widget, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Layout()
        self.ren = vtk.vtkRenderer()
        self.filename=""
        self.isploted = False
        self.cam = self.ren.GetActiveCamera()
            
    def renderthis(self):
            # open a window and create a renderer           
            self.widget.GetRenderWindow().AddRenderer(self.ren)
   
           # open file            
            openFileDialog = wx.FileDialog(self, "Open STL file", "", self.filename,
                                       "*.stl", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
             
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.filename = openFileDialog.GetPath()
            
            
            # render the data
            reader = vtk.vtkSTLReader()
            reader.SetFileName(self.filename)
            
            reader.Update()
            mesh = reader.GetOutput()         
            
            # To take the polygonal data from the vtkConeSource and
            # create a rendering for the renderer.
            coneMapper = vtk.vtkPolyDataMapper()
            coneMapper.SetInput(reader.GetOutput())
 
            # create an actor for our scene
            if self.isploted:
                coneActor=self.ren.GetActors().GetLastActor()
                self.ren.RemoveActor(coneActor)
                 
            coneActor = vtk.vtkActor()
            coneActor.SetMapper(coneMapper)
            # Add actor
            self.ren.AddActor(coneActor)
           # print self.ren.GetActors().GetNumberOfItems()
           
            #addPoint(self.ren, pSource, color=[1.0,0.0,0.0]) 
            #addPoint(self.ren, pTarget, color=[1.0,0.0,1.0]) 
            addLine(self.ren, pp1, pp2)
            addLine(self.ren, pp3, pp4)
            addLine(self.ren, pp5, pp6)
            addLine(self.ren, pp7, pp8)
            
            addLine(self.ren, pp1, pp7)
            addLine(self.ren, pp3, pp5)
            addLine(self.ren, pp4, pp6)
            addLine(self.ren, pp2, pp8)
            
            addLine(self.ren, pp1, pp3)
            addLine(self.ren, pp7, pp5)
            addLine(self.ren, pp4, pp2)
            addLine(self.ren, pp6, pp8)            
            
            obbTree = vtk.vtkOBBTree()
            obbTree.SetDataSet(mesh)
            obbTree.BuildLocator()
            
            pointsVTKintersection = vtk.vtkPoints()
            obbTree.IntersectWithLine(pSource, pTarget, pointsVTKintersection, None)
            #####################################################################################
            featureEdge=vtk.vtkFeatureEdges()
            featureEdge.FeatureEdgesOff()
            featureEdge.BoundaryEdgesOn()
            featureEdge.NonManifoldEdgesOn()
            featureEdge.SetInput(mesh)
            featureEdge.Update()
            openEdges = featureEdge.GetOutput().GetNumberOfCells()

            if openEdges != 0:
                print "the stl file is not closed"
            
            select = vtk.vtkSelectEnclosedPoints()
            select.SetSurface(mesh)
            
           
            for i in range(11):
                IsInside(i-5,0.1,0.1,mesh)
            #####################################################################################
            pointsVTKIntersectionData = pointsVTKintersection.GetData()
            noPointsVTKIntersection = pointsVTKIntersectionData.GetNumberOfTuples()
            pointsIntersection = []
            for idx in range(noPointsVTKIntersection):
                _tup = pointsVTKIntersectionData.GetTuple3(idx)
                pointsIntersection.append(_tup)
                
            print pointsIntersection
 
            if not self.isploted:
                axes = vtk.vtkAxesActor()
                self.marker = vtk.vtkOrientationMarkerWidget()
                self.marker.SetInteractor( self.widget._Iren )
                self.marker.SetOrientationMarker( axes )
                self.marker.SetViewport(0.75,0,1,0.25)
                self.marker.SetEnabled(1)
 
            self.ren.ResetCamera()
            self.ren.ResetCameraClippingRange()
            #cam = self.ren.GetActiveCamera()
            self.cam.Elevation(10)
            self.cam.Azimuth(40)
            #cam.SetPosition(0,0,1)
            #cam.SetFocalPoint(0,0,-50)
            self.isploted = True
            self.ren.Render()
 
class VTKFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(800,900), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        self.sp = wx.SplitterWindow(self)
        self.p1 = p1(self.sp)
        self.p2 = wx.Panel(self.sp,style=wx.SUNKEN_BORDER)
         
        self.sp.SplitHorizontally(self.p1,self.p2,770)
 
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Click on the Load Button to load a STL file")
         
        self.plotbut = wx.Button(self.p2,-1,"Browse for STL file ", size=(120,20),pos=(10,10))
        self.plotbut.Bind(wx.EVT_BUTTON,self.plot)
        
        self.Xview = wx.Button(self.p2,-1,"X ", size=(70,20),pos=(200,10))
        self.Xview.Bind(wx.EVT_BUTTON,self.Xview_position)
        
        self.Yview = wx.Button(self.p2,-1,"Y ", size=(70,20),pos=(300,10))
        self.Yview.Bind(wx.EVT_BUTTON,self.Yview_position)
         
 
    def plot(self,event):
        self.p1.renderthis()
        self.SetTitle("STL File Viewer: "+self.p1.filename)
        self.statusbar.SetStatusText("Use W,S,F,R keys and mouse to interact with the model ")
        
    def Xview_position(self,event): 
        self.p1.cam.Elevation(90)
        self.p1.cam.Azimuth(0)
        self.p1.ren.SetBackground(1,1,1)
        self.p1.widget.Render()
        print "Xview"
        #self.p1.ren.Render()
        
        
    def Yview_position(self,event):        
        self.p1.cam.Elevation(0)
        self.p1.cam.Azimuth(90) 
        self.p1.ren.SetBackground(1,1,0)
        self.p1.widget.Render()
        print "Yview"
        #self.p1.ren.Render()
       
        
    
 
         
app = wx.App(redirect=False)
frame = VTKFrame(None,"STL File Viewer")
frame.Show()
app.MainLoop()
    

