import os
import math
from ldmt_function.ldmt_loadUIFile import get_maya_window, load_ui_type
import maya.OpenMayaUI as omui
from ldmt_core import ldmt_cmds as ld
from functools import partial
import maya.cmds as cmds
import maya.mel as mel

try:
    from PySide2.QtCore import * 
    from PySide2.QtGui import * 
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance 
except ImportError:
    from PySide.QtCore import * 
    from PySide.QtGui import * 
    from PySide.QtUiTools import *
    from PySide import __version__
    from shiboken import wrapInstance 

import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import random
import ast

LDMTPATH = ld.getPath('LDMT')
ldmt_uifile = LDMTPATH + '/ldmt_ui/ldmt_textureRender.ui'
ldmt_list_form, ldmt_list_base = load_ui_type(ldmt_uifile)
ldmt_window_name = 'ldmt_textureRender'
ldmt_button_name = 'btn_'+ldmt_window_name.split('_')[1]

'''
#UI
'''
class ldmt_cls(ldmt_list_form, ldmt_list_base):
    def __init__(self, parent = get_maya_window()):
        super(ldmt_cls, self).__init__(parent)
        self.window_name = ldmt_window_name
        self.setupUi(self)
        self.move(QCursor.pos() + QPoint(20,20))
        # update status bar so it's not only show in help line window.
        self.setupBtn()
        self.statusbar.showMessage(ld.tag())
        self.installStartBar()
        
    def setupBtn(self):
        self.btn_cameraFromPlane.clicked.connect(self.cameraFromPlane)
        self.btn_clearCamera.clicked.connect(self.clearCamera)

    def cameraFromPlane(self):
        try:
            sel = cmds.ls(sl=1,o=1)
            sel = sel[0]
        except:
            f_printMessage("Select A Plane First!")
            return
        sel_bb = cmds.polyEvaluate(sel,b=1)
        sel_center = [(sel_bb[0][1]+sel_bb[0][0])/2, (sel_bb[1][1]+sel_bb[1][0])/2, (sel_bb[2][1]+sel_bb[2][0])/2]
        planeOrtho = self.ifPlaneOrtho(sel)
        if planeOrtho == "PlaneIsNotOrtho":
            f_printMessage("The Plane Is Not Aligned To Any Axis!")
            return
        mel.eval("FreezeTransformations;")
        normalDirection = cmds.polyNormalPerVertex(sel+'.vtx[0]',q=1,xyz=1)

        #get normal direction of plan
        for xyz in range(3):
            if abs(normalDirection[xyz]) > 0.999:
                normalDirection_xyz = xyz
                break
        cameraTarget = [0,0,-1]
        cameraTargetZ = normalDirection[xyz]*(-1)
        cameraWidth = 2
        if normalDirection_xyz == 0:
            cameraTarget = [cameraTargetZ,sel_center[1],sel_center[2]]
            cameraWidth = sel_bb[2][1]-sel_bb[2][0]
        elif normalDirection_xyz ==1:
            cameraTarget = [sel_center[0],cameraTargetZ,sel_center[2]] 
            cameraWidth = sel_bb[0][1]-sel_bb[0][0]
        elif normalDirection_xyz ==2:
            cameraTarget = [sel_center[0],sel_center[1],cameraTargetZ] 
            cameraWidth = sel_bb[0][1]-sel_bb[0][0]
        targetCamera = cmds.camera(n="ldmt_renderCamera#",orthographic = 1)
        targetCamera = targetCamera[0]
        cmds.lookThru(targetCamera)
        cmds.viewLookAt(targetCamera, pos = [cameraTarget[0],cameraTarget[1],cameraTarget[2]+10000])
        cmds.camera(targetCamera,e=1,ow=cameraWidth)

    def ifPlaneOrtho(self,sel):
        selList = om2.MSelectionList()
        selList.add(sel)
        selPath = selList.getDagPath(0)
        selVtxIter = om2.MItMeshVertex(selPath)
        cornerPositions = []
        while not selVtxIter.isDone():
            numConnectedFaces = selVtxIter.numConnectedEdges()
            if numConnectedFaces == 2:
                cornerPositions.append(selVtxIter.position(space = om2.MSpace.kWorld))
            selVtxIter.next()
        if len(cornerPositions)!=4:
            return "PlaneIsNotOrtho"
        else:
            YZ = 0
            XZ = 0
            XY = 0
            averageX = (cornerPositions[0][0]+cornerPositions[1][0]+cornerPositions[2][0]+cornerPositions[3][0])/4
            averageY = (cornerPositions[0][1]+cornerPositions[1][1]+cornerPositions[2][1]+cornerPositions[3][1])/4
            averageZ = (cornerPositions[0][2]+cornerPositions[1][2]+cornerPositions[2][2]+cornerPositions[3][2])/4
            for cornerIndex in range(4):
                if abs(cornerPositions[cornerIndex][0]-averageX)<0.000001:
                    YZ += 1
                if abs(cornerPositions[cornerIndex][1]-averageY)<0.000001:
                    XZ += 1
                if abs(cornerPositions[cornerIndex][2]-averageZ)<0.000001:
                    XY += 1
            if YZ == 4:
                return "YZ"
            elif XZ == 4:
                return "XZ"
            elif XY == 4:
                return "XY"
            else:
                return "PlaneIsNotOrtho"

    def clearCamera(self):
        camerasList = cmds.listCameras()
        for eachCamera in camerasList:
            if not eachCamera in ['front','side','top','persp'] and eachCamera.startswith("ldmt_renderCamera"):
                cmds.delete(eachCamera)
    def installStartBar(self):
        allQWidgets = self.findChildren(QWidget)
        for i in allQWidgets:
            i.installEventFilter(self)

    def eventFilter(self, obj, event ):
        '''Connect signals on mouse over''' 
        if event.type() == QEvent.Enter:
            self.oldMessage = ld.tag()
            self.statusbar.showMessage(' '+obj.statusTip(),0) 
        elif event.type() == QEvent.Leave:
            self.statusbar.showMessage(' '+self.oldMessage, 0)
            pass 
            event.accept()
        return False 

    def closeEvent(self,event):
        ld.turnToolBtnOff(self,ldmt_button_name)
        cmds.deleteUI(ldmt_window_name)

def ldmt_show():
    if cmds.window(ldmt_window_name,ex=1):
        if cmds.window(ldmt_window_name,q=1,vis=1):
            cmds.window(ldmt_window_name,e=1,vis=0)
        else:
            cmds.window(ldmt_window_name,e=1,vis=1)
    else:
        ui = ldmt_cls()
        ui.show()

if __name__ == '__main__':
    ldmt_show()