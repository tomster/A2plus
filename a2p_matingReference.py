#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2019 kbwbe                                              *
#*                                                                         *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

import FreeCAD
import FreeCADGui
from FreeCAD import Base
import Part

#==============================================================================
class a2p_MatingReference(object):
    '''
    An object which can be referenced by a2p constraints
    '''
    def __init__(self, obj):
        obj.Proxy = self
        a2p_MatingReference.setProperties(self,obj)

    def setProperties(self,obj):
        propList = obj.PropertiesList
        if not "rigid" in propList:
            obj.addProperty("App::PropertyString", "rigid", "a2p_matingRef")
            obj.setEditorMode('rigid', 1)
        if not "size" in propList:
            obj.addProperty("App::PropertyFloat", "size","a2p_matingRef")
            obj.size = 5.0 #default size
        self.type = "a2p_constraintDockRef"
        
    def onDocumentRestored(self,obj):
        a2p_MatingReference.setProperties(self,obj)
        
    def execute(self, obj):
        s = obj.size

        v0 = FreeCAD.Vector(0.0,0.0,0.0)
        vx = FreeCAD.Vector(s,0.0,0.0)
        vy = FreeCAD.Vector(0.0,s,0.0)
        vz = FreeCAD.Vector(0.0,0.0,s)
        
        axisShape = Part.Shape(
            [
                Part.LineSegment(v0,vx),
                Part.LineSegment(v0,vy),
                Part.LineSegment(v0,vz)
                ]
            )

        
        xy_v0 = FreeCAD.Vector(s*0.2,s*0.2,0.0)
        xy_v1 = FreeCAD.Vector(s,s*0.2,0.0)
        xy_v2 = FreeCAD.Vector(s,s,0.0)
        xy_v3 = FreeCAD.Vector(s*0.2,s,0.0)
        
        xy_l0 = Part.LineSegment(xy_v0, xy_v1)
        xy_l1 = Part.LineSegment(xy_v1, xy_v2)
        xy_l2 = Part.LineSegment(xy_v2, xy_v3)
        xy_l3 = Part.LineSegment(xy_v3, xy_v0)
        
        s1 = Part.Shape([xy_l0, xy_l1, xy_l2, xy_l3])
        w = Part.Wire(s1.Edges)
        fxy = Part.Face(w)
        
        yz_v0 = FreeCAD.Vector(0.0,s*0.2,s*0.2)
        yz_v1 = FreeCAD.Vector(0.0,s,s*0.2)
        yz_v2 = FreeCAD.Vector(0.0,s,s)
        yz_v3 = FreeCAD.Vector(0.0,s*0.2,s)
        
        yz_l0 = Part.LineSegment(yz_v0, yz_v1)
        yz_l1 = Part.LineSegment(yz_v1, yz_v2)
        yz_l2 = Part.LineSegment(yz_v2, yz_v3)
        yz_l3 = Part.LineSegment(yz_v3, yz_v0)
        
        s2 = Part.Shape([yz_l0, yz_l1, yz_l2, yz_l3])
        w = Part.Wire(s2.Edges)
        fyz = Part.Face(w)
        
        xz_v0 = FreeCAD.Vector(s*0.2,0.0,s*0.2)
        xz_v1 = FreeCAD.Vector(s,0.0,s*0.2)
        xz_v2 = FreeCAD.Vector(s,0.0,s)
        xz_v3 = FreeCAD.Vector(s*0.2,0.0,s)
        
        xz_l0 = Part.LineSegment(xz_v0, xz_v1)
        xz_l1 = Part.LineSegment(xz_v1, xz_v2)
        xz_l2 = Part.LineSegment(xz_v2, xz_v3)
        xz_l3 = Part.LineSegment(xz_v3, xz_v0)
        
        s3 = Part.Shape([xz_l0, xz_l1, xz_l2, xz_l3])
        w = Part.Wire(s3.Edges)
        fxz = Part.Face(w)
        
        obj.Shape = Part.makeCompound(
            [
                axisShape,
                fxy,
                fyz,
                fxz
                ]
            )
        
    def onChanged(self, obj, prop):
        pass
            
#==============================================================================
class VP_a2p_MatingReference(object):
    
    def __init__(self,vobj):
        vobj.Proxy = self

    def attach(self, vobj):
        self.ViewObject = vobj
        self.Object = vobj.Object
        
    def claimChildren(self):
        return []

    def getDisplayModes(self,obj):
        '''Return a list of display modes.'''
        modes=[]
        modes.append("As is")
        modes.append("Flat lines")
        modes.append("Wireframe")
        return modes

    def setDisplayMode(self,mode):
        return mode

    def getDefaultDisplayMode(self):
        return "Flat Lines"    

    def onDelete(self, viewObject, subelements): # subelements is a tuple of strings
        if FreeCAD.activeDocument() != viewObject.Object.Document:
            return False # only delete objects in the active Document anytime !!
        return True

    def getIcon(self):
        return ":/icons/a2p_LCS_group.svg" # to be changed...

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None

#==============================================================================
