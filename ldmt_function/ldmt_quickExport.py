import os
import math
from ldmt_function.ldmt_loadUIFile import get_maya_window, load_ui_type
import maya.OpenMayaUI as omui
from ldmt_core import ldmt_cmds as ld
from functools import partial
import maya.cmds as cmds
import maya.mel as mel
from functools import partial

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
ldmt_uifile = LDMTPATH + '/ldmt_ui/ldmt_quickExport.ui'
ldmt_list_form, ldmt_list_base = load_ui_type(ldmt_uifile)
ldmt_window_name = 'ldmt_quickExport'
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
        self.btn_export.clicked.connect(self.quickExport)
    def quickExport(self):
        currentFormat = self.box_format.currentText()
        print(currentFormat)
        fullpath = cmds.file(query=1 ,location=1)

        if fullpath == 'unknown':
            mayaPath = mel.eval('getenv MAYA_LOCATION')
            exportPath = mayaPath+'/bin/'
        else:
            filename = cmds.file(q=1,sn=1,shn=1)
            exportPath = fullpath[:-len(filename)]
        # subprocess.Popen('explorer '+ filepath +'', shell=True)
        sel = cmds.ls(sl=1,o=1)
        exportFolder = exportPath+"models/"
        if not os.path.exists(exportFolder):
            os.mkdir(exportFolder)
        exportName = exportFolder+sel[0].split('|')[-1]

        if currentFormat == 'OBJ':
            if cmds.pluginInfo("objExport",q=1,l=1) !=1: 
                mds.loadPlugin("objExport",qt=1)
            cmds.file(exportName, force=True, options='groups=1;ptgroups=1;materials=1;smoothing=1;normals=1', type='OBJexport', pr=True, es=True)

        elif currentFormat == 'FBX':
            if cmds.pluginInfo("fbxmaya",q=1,l=1) !=1: 
                mds.loadPlugin("fbxmaya",qt=1)
            fbxExportName = exportName+".fbx"
            mel.eval('FBXExportScaleFactor 1;')
            mel.eval('FBXExportInAscii -v 1;')
            mel.eval('FBXExportSmoothingGroups -v 1;')
            mel.eval('FBXExportSmoothMesh -v 1;')
            mel.eval('FBXExportTriangulate -v 0;')
            mel.eval('FBXExportUpAxis y;')
            mel.eval('FBXExport -f "'+ fbxExportName +'" -s;')
            
        elif currentFormat == 'UE4':
            if cmds.pluginInfo("fbxmaya",q=1,l=1) !=1: 
                mds.loadPlugin("fbxmaya",qt=1)
            fbxExportName = exportName+".fbx"
            mel.eval('FBXExportScaleFactor 1;')
            mel.eval('FBXExportInAscii -v 1;')
            mel.eval('FBXExportSmoothingGroups -v 1;')
            mel.eval('FBXExportSmoothMesh -v 1;')
            mel.eval('FBXExportTriangulate -v 1;')
            mel.eval('FBXExportUpAxis y;')
            mel.eval('FBXExport -f "'+ fbxExportName +'" -s;')
        mel.eval('system("load '+ exportFolder +'");')

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