import os
import math
from ldmt_function.ldmt_loadUIFile import get_maya_window, load_ui_type
import maya.OpenMayaUI as omui
from ldmt_core import ldmt_cmds as ld
from ldmt_function import ldmt_morphToUV
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
ldmt_uifile = LDMTPATH + '/ldmt_ui/ldmt_marvelousTool.ui'
ldmt_list_form, ldmt_list_base = load_ui_type(ldmt_uifile)
ldmt_window_name = 'ldmt_marvelousTool'
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
        self.btn_flatten.clicked.connect(self.flatten)
        self.btn_makePairs.clicked.connect(self.makePairs)
        self.slider_blendshape.setMinimum(0)
        self.slider_blendshape.setMaximum(100)
        self.slider_blendshape.valueChanged.connect(self.blendshapeChange)
        # self.btn_makePairs.clicked.connect(self.makePairs)

    def blendshapeChange(self):
        blendValue = float(self.slider_blendshape.value())/100
        sel = cmds.ls(sl=1,o=1)
        for i in sel:
            selShape = cmds.listRelatives(i,s=1)
            selShape = selShape[0]
            wrapNode = cmds.listConnections(selShape,type="wrap")
            wrapNode = wrapNode[0]
            wrapNode_connections = cmds.listConnections(wrapNode)
            patternName = ''
            for j in wrapNode_connections:
                if j.endswith('_pattern'):
                    patternName = j
            patternShape = cmds.listRelatives(patternName,s=1)
            patternShape = patternShape[0]
            blendshapeNode = cmds.listConnections(patternShape,type="blendShape")
            cmds.blendShape(blendshapeNode,e=1,w=(0,blendValue))

    def flatten(self):
        from ldmt_function import ldmt_morphToGarment
        from ldmt_function import ldmt_normalFacet
        sel = cmds.ls(sl=1,o=1)
        selBB = cmds.polyEvaluate(b=1)
        garmentHeight = selBB[1][1]-selBB[1][0]
        garmentMaxX = selBB[0][1]
        patternList = []
        for i in sel:
            pattern = ldmt_morphToGarment.runMorph2UV(i)
            newName = i+'_pattern'
            patternList.append(newName)
            cmds.rename(pattern,newName)
        cmds.select(patternList)
        ldmt_normalFacet.normalFacet()
        cmds.scale(garmentHeight,garmentHeight,garmentHeight)
        cmds.move(garmentMaxX,0,0)
        cmds.group(sel,n="ldmt_marvelousTool_garments#")
        cmds.group(patternList,n="ldmt_marvelousTool_patterns#")

    def makePairs(self):
        sel = cmds.ls(os=1)
        garments = cmds.listRelatives(sel[0]) # len(garments)
        patterns = cmds.listRelatives(sel[1]) # len(patterns) 
        retopos = cmds.listRelatives(sel[2])  # len(retopos)
        retopos_BB_width   = {}
        retopos_BB_length  = {}
        retopos_BB_center  = {}
        patterns_BB_width  = {}
        patterns_BB_length = {}
        patterns_BB_center = {}
        # In case that uv doesn't exists.
        cmds.select(retopos,r=1)
        mel.eval("performPolyAutoProj 0;")
        cmds.select(sel,r=1)
        # In case wrong bb
        for i in retopos:
            cmds.polyMergeVertex(i, d=0.001)
        # Matching
        for i in retopos:
            BB = cmds.polyEvaluate(i,b=1)
            retopos_BB_width[i]   = BB[0][1] - BB[0][0]
            retopos_BB_length[i]  = BB[1][1] - BB[1][0]
            retopos_BB_center[i]  = [(BB[0][1] + BB[0][0])/2, (BB[1][1] + BB[1][0])/2]
        for i in patterns:
            BB = cmds.polyEvaluate(i,b=1)
            patterns_BB_width[i]   = BB[0][1] - BB[0][0]
            patterns_BB_length[i]  = BB[1][1] - BB[1][0]
            patterns_BB_center[i]  = [(BB[0][1] + BB[0][0])/2, (BB[1][1] + BB[1][0])/2]
        pair_pattern_retopo={}  # len(pair_pattern_retopo)
        for i in patterns:
            for j in retopos:
                if      abs(patterns_BB_width[i] - retopos_BB_width[j])         < 1 \
                    and abs(patterns_BB_length[i] - retopos_BB_length[j])       < 1 \
                    and abs(patterns_BB_center[i][0] - retopos_BB_center[j][0]) < 1 \
                    and abs(patterns_BB_center[i][1] - retopos_BB_center[j][1]) < 1:
                    pair_pattern_retopo[i] = j
        for i in pair_pattern_retopo:
            cmds.transferAttributes(i,pair_pattern_retopo[i],transferUVs=1)
        for i in pair_pattern_retopo:
            cmds.select(pair_pattern_retopo[i],i,r=1)
            cmds.CreateWrap()
        for i in pair_pattern_retopo:
            pairGarment = i[:-8]
            pattern = i
            blendObjs = [pairGarment,pattern]  # 0: target 1: origin
            blendName = cmds.blendShape(blendObjs,o='world',n='clothTransfer#')
            cmds.hide(sel[1])
            cmds.displaySurface(sel[0],x=1)
        cmds.hide(sel[1])
        cmds.displaySurface(sel[0],x=1)
        layerName = cmds.createDisplayLayer( n = "garment#", e=1)
        cmds.editDisplayLayerMembers(layerName,sel[0])
        cmds.setAttr(layerName+'.displayType',2)

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