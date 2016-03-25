"""
Created on Fri Dec 13 11:45:03 2013
 
@author: Sukhbinder Singh
 
VTL STL File reader with wxPython GUI
 
"""
import wx
import vtk
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
import numpy as np
from vtk import vtkGlyph3D
from obliczenia import *
#e_a = 10
#a_a = 70
lwX = 50
lwY = 200
lwZ = 50

stoProcent = lwX*lwY
licz = 0
licz2 = 0
licznik = 0
warunek=0

zrodloGlyph = []

siatkaX = np.arange(0.0,lwX+1,1.0)
siatkaY = np.arange(0.0,lwY+1,1.0)
siatkaZ = np.arange(0.0,lwZ+1,1.0)



maska = np.arange(0,(lwX)*(lwY)*(lwZ),1)
maska3D = np.arange(0,(lwX)*(lwY)*(lwZ),1).reshape(lwY,lwX,lwZ)
maska3D_forcing = np.arange(0,(lwX)*(lwY)*(lwZ),1).reshape(lwY,lwX,lwZ)
boundary_points = np.arange(0,(lwX)*(lwY)*(lwZ),1)
intersection = []*3
#print maska3D

print intersection

pSource = [-80.0,0.0,0.0]
pTarget = [30.0,0.0,0.0]

xmin = -1.0
xmax = 1.0
ymin = -1.0
ymax = 7.0
zmin = -1.0
zmax = 1.0

rozmiarX=xmax-xmin
rozmiarY=ymax-ymin
rozmiarZ=zmax-zmin

siatkaX[1]=xmin
siatkaY[1]=ymin
siatkaZ[1]=zmin   

hX = float(rozmiarX/(lwX-1))
hY = float(rozmiarY/(lwY-1))
hZ = float(rozmiarZ/(lwZ-1))

for i in range(2,lwX+1):
    siatkaX[i] = siatkaX[i-1]+hX   
    
for i in range(2,lwY+1):
    siatkaY[i] = siatkaY[i-1]+hY   
    
for i in range(2,lwZ+1):
    siatkaZ[i] = siatkaZ[i-1]+hZ 
    
#odczytX = open('MESH_X.txt')

#for i in range(1,lwX+1):
   # siatkaX[i] = (odczytX.readline()) 
   # print i,siatkaX[i]
    
#odczytX.close
 
#odczytY = open('MESH_Y.txt')

#for i in range(1,lwY+1):
    #siatkaY[i] = (odczytY.readline()) 
    #print i,siatkaY[i]
    
#odczytY.close

#for i in range(1,lwY+1):
    #siatkaY[i]=siatkaY[i]/siatkaY[lwY]
   # print i,siatkaY[i]
    
#for i in range(1,lwY+1):
   # siatkaY[i]=siatkaY[i]*6.0
   # print i,siatkaY[i]


pp1 = [xmin,ymin,zmin]
pp2 = [xmax,ymin,zmin]
pp3 = [xmin,ymax,zmin]
pp4 = [xmax,ymax,zmin]
pp5 = [xmin,ymax,zmax]
pp6 = [xmax,ymax,zmax]
pp7 = [xmin,ymin,zmax]
pp8 = [xmax,ymin,zmax]

def addEdges(renderer):
    
    addLine(renderer, pp1, pp2)
    addLine(renderer, pp3, pp4)
    addLine(renderer, pp5, pp6)
    addLine(renderer, pp7, pp8)
            
    addLine(renderer, pp1, pp7)
    addLine(renderer, pp3, pp5)
    addLine(renderer, pp4, pp6)
    addLine(renderer, pp2, pp8)
            
    addLine(renderer, pp1, pp3)
    addLine(renderer, pp7, pp5)
    addLine(renderer, pp4, pp2)
    addLine(renderer, pp6, pp8)            
            

def addPoint(renderer, p, radius=0.5, color=[0.0,0.0,0.0]):
    point = vtk.vtkSphereSource()
    point.SetCenter(p)
    point.SetRadius(radius)
    point.SetPhiResolution(3)
    point.SetThetaResolution(3)
    
    #pointGlyph = vtkGlyph3D()
   # pointGlyph.SetSourceConnection(point.GetOutputPort())
      
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
    
def IsInsideCheck(pX,pY,pZ,mesh):
    select = vtk.vtkSelectEnclosedPoints()
    select.SetSurface(mesh)
    select.SetTolerance(.00001)
    
    pts = vtk.vtkPoints()
    pts.InsertNextPoint((pX),(pY),(pZ))
    pts_pd = vtk.vtkPolyData()
    pts_pd.SetPoints(pts)
    select.SetInput(pts_pd)
    select.Update()
   # print pX,pY,pZ,select.IsInside(0)
    return select.IsInside(0)
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
            
    def renderthis(self,warunek):
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
            
            if warunek==1:
                addEdges(self.ren)            
            
            
            
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
            
            inside_polydat = vtk.vtkPolyData()
            forcing_polydat = vtk.vtkPolyData()
            interpolation_polydat = vtk.vtkPolyData()
            inside_points = vtk.vtkPoints()
            forcing_points = vtk.vtkPoints()
            interpolation_points = vtk.vtkPoints()
           # for i in range(11):
                #IsInside(i-5,0.1,0.1,mesh)
            global licz 
            global licz2
            global licznik
            
            for j in range(1,lwY+1):
                for i in range(1,lwX+1):
                    licz += 1
                    print (licz/float(stoProcent))*100.0
                    for k in range(1,lwZ+1):
                        sprawdzenie = 0
                        siatkaX[1]=xmin+0.001
                        siatkaX[lwX]=xmax-0.001
                        siatkaY[1]=ymin+0.001
                        siatkaY[lwY]=ymax-0.001
                        siatkaZ[1]=zmin+0.001
                        siatkaZ[lwZ]=zmax-0.001
                        sprawdzenie = IsInsideCheck(siatkaX[i],siatkaY[j],siatkaZ[k],mesh)
                        siatkaX[1]=xmin
                        siatkaX[lwX]=xmax
                        siatkaY[1]=ymin
                        siatkaY[lwY]=ymax
                        siatkaZ[1]=zmin
                        siatkaZ[lwZ]=zmax
                        mesh_point_inside = [siatkaX[i],siatkaY[j],siatkaZ[k]]
                        #mesh_point_forcing = [siatkaX[i]+1.0,siatkaY[j],siatkaZ[k]]
                        
                        maska[licznik] = sprawdzenie
                        licznik=licznik+1
                        if sprawdzenie == 1:
                            inside_points.InsertNextPoint(mesh_point_inside)
                            #forcing_points.InsertNextPoint(mesh_point_forcing)
                            
            licznik=0   
            
    
            for j in range(0,lwY):
                for i in range(0,lwX):
                    for k in range(0,lwZ):
                        #print j,i,k
                        maska3D[j][i][k]=maska[licznik]
                        licznik=licznik+1
            
            #print maska3D
            find_forcing_points(lwY,lwX,lwZ,maska3D,forcing_points,siatkaX,siatkaY,siatkaZ,boundary_points,mesh,intersection,maska3D_forcing,interpolation_points)
            
            print featureEdge
            #print intersection 
            #print "+++++++++++++++++++="
            #print maska3D_forcing
            """
            licznik=0
            for j in range(0,lwY):
                for i in range(0,lwX-1):
                    for k in range(0,lwZ):
                        mesh_point_forcing = [siatkaX[i+1],siatkaY[j+1],siatkaZ[k+1]]
                        if (maska3D[j][i][k] == 0) and (maska3D[j][i+1][k] == 1):
                            forcing_points.InsertNextPoint(mesh_point_forcing)
                        licznik=licznik+1
              """          
                        
            zapis = open('Maska.txt', 'w')
            for i in range(0,lwX*lwY*lwZ):
                zapis.write(str(maska[i]))
                zapis.write('\n')
            zapis.close()		
            print "zapisano Maske"
            inside_polydat.SetPoints(inside_points)
            
            inside = vtk.vtkSphereSource()
            inside.SetRadius(0.02)
            inside.SetPhiResolution(8)
            inside.SetThetaResolution(8)
    
            ballGlyph = vtkGlyph3D()
            ballGlyph.SetColorModeToColorByScalar()
            ballGlyph.SetSourceConnection(inside.GetOutputPort())
            ballGlyph.SetInput(inside_polydat)
      
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(ballGlyph.GetOutputPort())
    
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor([1.0,0.0,0.0])
    
            self.ren.AddActor(actor)
            ######################################################################################
            forcing_polydat.SetPoints(forcing_points)
            
            forcing = vtk.vtkSphereSource()
            #point.SetCenter(pS)
            forcing.SetRadius(0.02)
            forcing.SetPhiResolution(8)
            forcing.SetThetaResolution(8)
    
            forcingGlyph = vtkGlyph3D()
            forcingGlyph.SetColorModeToColorByScalar()
            forcingGlyph.SetSourceConnection(forcing.GetOutputPort())
            forcingGlyph.SetInput(forcing_polydat)
      
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(forcingGlyph.GetOutputPort())
    
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor([0.0,1.0,0.0])
    
            self.ren.AddActor(actor)
            #####################################################################################
            interpolation_polydat.SetPoints(interpolation_points)
            
            interpolation = vtk.vtkSphereSource()
            #point.SetCenter(pS)
            interpolation.SetRadius(0.02)
            interpolation.SetPhiResolution(8)
            interpolation.SetThetaResolution(8)
    
            interpolationGlyph = vtkGlyph3D()
            interpolationGlyph.SetColorModeToColorByScalar()
            interpolationGlyph.SetSourceConnection(interpolation.GetOutputPort())
            interpolationGlyph.SetInput(interpolation_polydat)
      
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(interpolationGlyph.GetOutputPort())
    
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor([0.0,0.0,1.0])
    
            self.ren.AddActor(actor)
            #####################################################################################
            obbTree = vtk.vtkOBBTree()
            obbTree.SetDataSet(mesh)
            obbTree.BuildLocator()
            
            pointsVTKintersection = vtk.vtkPoints()
            obbTree.IntersectWithLine(pSource, pTarget, pointsVTKintersection, None)
            
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
            self.cam.Elevation(50)
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
        self.p1.renderthis(warunek)
        self.SetTitle("STL File Viewer: "+self.p1.filename)
        self.statusbar.SetStatusText("Use W,S,F,R keys and mouse to interact with the model ")
        
    def Xview_position(self,event): 
        #self.p1.cam.Elevation(10)
        #self.p1.cam.Azimuth(0)
        warunek=1
        #self.p1.ren.SetBackground(1,1,1)
        self.p1.renderthis(warunek)
        print "Xview"
        #self.p1.ren.Render()
        
        
    def Yview_position(self,event):        
        self.p1.cam.Elevation(0)
        self.p1.cam.Azimuth(10) 
        #self.p1.ren.SetBackground(1,1,0)
        self.p1.widget.Render()
        print "Yview"
        #self.p1.ren.Render()
       
        
    
 
         
app = wx.App(redirect=False)
frame = VTKFrame(None,"STL File Viewer")
frame.Show()
app.MainLoop()
    

