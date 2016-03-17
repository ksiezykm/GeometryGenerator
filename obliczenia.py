# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 13:21:08 2016

@author: ksiezykm
"""
import wx
import vtk
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
import numpy as np

def find_forcing_points(lwY,lwX,lwZ,maska3D,forcing_points,siatkaX,siatkaY,siatkaZ,boundary_points,mesh,intersection):
    
            obbTree = vtk.vtkOBBTree()
            obbTree.SetDataSet(mesh)
            obbTree.BuildLocator()
            
            
            for j in range(0,lwY):
                for i in range(0,lwX):
                    for k in range(0,lwZ):
                        mesh_point_forcing = [siatkaX[i+1],siatkaY[j+1],siatkaZ[k+1]]
                        if i<lwX-1:
                            if (maska3D[j][i][k] == 0) and (maska3D[j][i+1][k] == 1):
                                forcing_points.InsertNextPoint(mesh_point_forcing)
                                
                                pSource = [siatkaX[i+1],siatkaY[j+1],siatkaZ[k+1]]
                                pTarget = [siatkaX[i+2],siatkaY[j+1],siatkaZ[k+1]]
                                
                                pointsVTKintersection = vtk.vtkPoints()
                                obbTree.IntersectWithLine(pSource, pTarget, pointsVTKintersection, None)
            
                                pointsVTKIntersectionData = pointsVTKintersection.GetData()
                                noPointsVTKIntersection = pointsVTKIntersectionData.GetNumberOfTuples()
                                pointsIntersection = []
                                for idx in range(noPointsVTKIntersection):
                                    _tup = pointsVTKIntersectionData.GetTuple3(idx)
                                    pointsIntersection.append(_tup)
                                    
                                intersection.append(_tup)
                                #print pointsIntersection
                               
                        if j<lwY-1:
                            if (maska3D[j][i][k] == 0) and (maska3D[j+1][i][k] == 1):
                                forcing_points.InsertNextPoint(mesh_point_forcing)
                                
                                pSource = [siatkaX[i+1],siatkaY[j+1],siatkaZ[k+1]]
                                pTarget = [siatkaX[i+1],siatkaY[j+2],siatkaZ[k+1]]
                                
                                pointsVTKintersection = vtk.vtkPoints()
                                obbTree.IntersectWithLine(pSource, pTarget, pointsVTKintersection, None)
            
                                pointsVTKIntersectionData = pointsVTKintersection.GetData()
                                noPointsVTKIntersection = pointsVTKIntersectionData.GetNumberOfTuples()
                                pointsIntersection = []
                                for idx in range(noPointsVTKIntersection):
                                    _tup = pointsVTKIntersectionData.GetTuple3(idx)
                                    pointsIntersection.append(_tup)
                                    
                                intersection.append(_tup)
                                #print pointsIntersection
                                
                        if k<lwZ-1:
                            if (maska3D[j][i][k] == 0) and (maska3D[j][i][k+1] == 1):
                                forcing_points.InsertNextPoint(mesh_point_forcing)

                                pSource = [siatkaX[i+1],siatkaY[j+1],siatkaZ[k+1]]
                                pTarget = [siatkaX[i+1],siatkaY[j+1],siatkaZ[k+2]]
                                
                                pointsVTKintersection = vtk.vtkPoints()
                                obbTree.IntersectWithLine(pSource, pTarget, pointsVTKintersection, None)
            
                                pointsVTKIntersectionData = pointsVTKintersection.GetData()
                                noPointsVTKIntersection = pointsVTKIntersectionData.GetNumberOfTuples()
                                pointsIntersection = []
                                for idx in range(noPointsVTKIntersection):
                                    _tup = pointsVTKIntersectionData.GetTuple3(idx)
                                    pointsIntersection.append(_tup)
                                
                                intersection.append(_tup)
                                #print pointsIntersection                                
                                
                        if i>1:
                            if (maska3D[j][i][k] == 0) and (maska3D[j][i-1][k] == 1):
                                forcing_points.InsertNextPoint(mesh_point_forcing)
                                
                                pSource = [siatkaX[i+1],siatkaY[j+1],siatkaZ[k+1]]
                                pTarget = [siatkaX[i],siatkaY[j+1],siatkaZ[k+1]]
                                
                                pointsVTKintersection = vtk.vtkPoints()
                                obbTree.IntersectWithLine(pSource, pTarget, pointsVTKintersection, None)
            
                                pointsVTKIntersectionData = pointsVTKintersection.GetData()
                                noPointsVTKIntersection = pointsVTKIntersectionData.GetNumberOfTuples()
                                pointsIntersection = []
                                for idx in range(noPointsVTKIntersection):
                                    _tup = pointsVTKIntersectionData.GetTuple3(idx)
                                    pointsIntersection.append(_tup)
                                    
                                intersection.append(_tup)
                                #print pointsIntersection                                
                                
                        if j>1:
                            if (maska3D[j][i][k] == 0) and (maska3D[j-1][i][k] == 1):
                                forcing_points.InsertNextPoint(mesh_point_forcing)
                                
                                pSource = [siatkaX[i+1],siatkaY[j+1],siatkaZ[k+1]]
                                pTarget = [siatkaX[i+1],siatkaY[j],siatkaZ[k+1]]
                                
                                pointsVTKintersection = vtk.vtkPoints()
                                obbTree.IntersectWithLine(pSource, pTarget, pointsVTKintersection, None)
            
                                pointsVTKIntersectionData = pointsVTKintersection.GetData()
                                noPointsVTKIntersection = pointsVTKIntersectionData.GetNumberOfTuples()
                                pointsIntersection = []
                                for idx in range(noPointsVTKIntersection):
                                    _tup = pointsVTKIntersectionData.GetTuple3(idx)
                                    pointsIntersection.append(_tup)
                                
                                intersection.append(_tup)
                                #print pointsIntersection                                
                                
                        if k>1:
                            if (maska3D[j][i][k] == 0) and (maska3D[j][i][k-1] == 1):
                                forcing_points.InsertNextPoint(mesh_point_forcing)
                                
                                pSource = [siatkaX[i+1],siatkaY[j+1],siatkaZ[k+1]]
                                pTarget = [siatkaX[i+1],siatkaY[j+1],siatkaZ[k]]
                                
                                pointsVTKintersection = vtk.vtkPoints()
                                obbTree.IntersectWithLine(pSource, pTarget, pointsVTKintersection, None)
            
                                pointsVTKIntersectionData = pointsVTKintersection.GetData()
                                noPointsVTKIntersection = pointsVTKIntersectionData.GetNumberOfTuples()
                                pointsIntersection = []
                                for idx in range(noPointsVTKIntersection):
                                    _tup = pointsVTKIntersectionData.GetTuple3(idx)
                                    pointsIntersection.append(_tup)
                                    
                                intersection.append(_tup)
                                #print pointsIntersection
                        