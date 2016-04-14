# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 12:33:52 2016

@author: ksiezykm
"""
import numpy as np
from struct import unpack
from math import sqrt

def odczyt_STL(filename,normals,licznik_forcing,fnix,fniy,fniz,fncx,fncy,fncz):
        
        fp = open(filename, 'rb')
        Header = fp.read(80)
        nn = fp.read(4)
        Numtri = unpack('i', nn)[0]
        #print nn
        record_dtype = np.dtype([
                       ('normals', np.float32,(3,)),  
                       ('Vertex1', np.float32,(3,)),
                       ('Vertex2', np.float32,(3,)),
                       ('Vertex3', np.float32,(3,)) ,              
                       ('atttr', '<i2',(1,) )
        ])
        data = np.fromfile(fp , dtype = record_dtype , count =Numtri)
        fp.close()
 
        Normals = data['normals']
        Vertex1 = data['Vertex1']
        Vertex2 = data['Vertex2']
        Vertex3 = data['Vertex3']
 
        p = np.append(Vertex1,Vertex2,axis=0)
        p = np.append(p,Vertex3,axis=0) #list(v1)
        Points =np.array(list(set(tuple(p1) for p1 in p)))
     
       # for i in range(0,Numtri):
         #   normals.append(Normals[i])
           # print i,normals[i]
            
            
        
        
        for i in range(0,licznik_forcing):
            warunek_odl=1000000.0
            for j in range(0,Numtri):
                odl_1=sqrt(pow((fncx[i]-Vertex1[j][0]),2)+pow((fncy[i]-Vertex1[j][1]),2)+pow((fncz[i]-Vertex1[j][2]),2))
                odl_2=sqrt(pow((fncx[i]-Vertex2[j][0]),2)+pow((fncy[i]-Vertex2[j][1]),2)+pow((fncz[i]-Vertex2[j][2]),2))
                odl_3=sqrt(pow((fncx[i]-Vertex3[j][0]),2)+pow((fncy[i]-Vertex3[j][1]),2)+pow((fncz[i]-Vertex3[j][2]),2))
                
                odl=(odl_1+odl_2+odl_3)/3.0
                
                if odl<warunek_odl:
                    warunek_odl=odl
                    najblizszy_trojkat=j
                    
            #print i,najblizszy_trojkat,fncx[i],fncy[i],fncz[i],Vertex1[najblizszy_trojkat][0],Vertex2[najblizszy_trojkat][1],Vertex1[najblizszy_trojkat][2]
            normals.append(Normals[najblizszy_trojkat])    
                
            
        #print Header,Points,Normals,Vertex1,Vertex2,Vertex3
        #print Vertex1
        #zapis2 = open('Normals.txt', 'w')
        #zapis2.write(Normals)
        #zapis2.close()