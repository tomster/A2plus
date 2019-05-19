#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2018 kbwbe                                              *
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
            obj.addProperty("App::PropertyString", "rigid", "a2p_dockRef")
            obj.setEditorMode('rigid', 1)
        if not "size" in propList:
            obj.addProperty("App::PropertyFloat", "size","a2p_dockRef")
            obj.size = 10.0 #default size
        self.type = "a2p_constraintDockRef"
        
    def onDocumentRestored(self,obj):
        a2p_MatingReference.setProperties(self,obj)
        
    def execute(self, obj):
        v0 = FreeCAD.Vector(0.0,0.0,0.0)
        vx = FreeCAD.Vector(obj.size,0.0,0.0)
        vy = FreeCAD.Vector(0.0,obj.size,0.0)
        vz = FreeCAD.Vector(0.0,0.0,obj.size)
        
        obj.Shape = Part.Shape(
            [
                Part.LineSegment(v0,vx),
                Part.LineSegment(v0,vy),
                Part.LineSegment(v0,vz)
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
