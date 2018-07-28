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
ldmt_uifile = LDMTPATH + '/ldmt_ui/ldmt_display.ui'
ldmt_list_form, ldmt_list_base = load_ui_type(ldmt_uifile)
ldmt_window_name = 'ldmt_display'
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
        self.btn_count.clicked.connect(self.count)
        self.btn_edgeId.clicked.connect(self.edgeId)
        self.btn_faceId.clicked.connect(self.faceId)
        self.btn_faceNormal.clicked.connect(self.faceNormal)
        self.btn_normalSize.clicked.connect(self.normalSize)
        self.btn_reset.clicked.connect(self.reset)
        self.btn_tangent.clicked.connect(self.tangent)
        self.btn_texBorder.clicked.connect(self.texBorder)
        self.btn_triangle.clicked.connect(self.triangle)
        self.btn_uvId.clicked.connect(self.uvId)
        self.btn_vertId.clicked.connect(self.vertId)
        self.btn_vertNormal.clicked.connect(self.vertNormal)
    def count(self):
        mel.eval("TogglePolyCount;")
    def edgeId(self):
        mel.eval('ToggleEdgeIDs;')
    def faceId(self):
        mel.eval('ToggleFaceIDs;')
    def faceNormal(self):
        mel.eval('ToggleFaceNormalDisplay;')
    def normalSize(self):
        mel.eval('ChangeNormalSize;')
    def reset(self):
        mel.eval('PolyDisplayReset;')
    def tangent(self):
        mel.eval('ToggleTangentDisplay;')
    def texBorder(self):
        mel.eval('ToggleTextureBorderEdges;')
    def triangle(self):
        mel.eval('TogglePolygonFaceTriangles;')
    def uvId(self):
        mel.eval('ToggleCompIDs;')
    def vertId(self):
        mel.eval('ToggleVertIDs;')
    def vertNormal(self):
        mel.eval('ToggleVertexNormalDisplay;')

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