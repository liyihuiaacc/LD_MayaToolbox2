'''
Don't edit the line above, it should be set by ldmt_setup.py automatically according to
your installation path.
'''
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2
import ConfigParser
import os
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
    
PM_startTime = cmds.timerX()
PM_timeAdder = 0
MAYA_version = cmds.about(v=1)
MAYA_version_float = float(MAYA_version.split(' ')[0])

'''
GLobal Environment
'''
def tag():
    return "Liu Dian xgits@outlook.com"
def getPath(whatPath):
    if whatPath == 'MAYA_SCRIPT_PATH':
        MAYA_SCRIPT_PATH = os.environ['MAYA_SCRIPT_PATH']
        MAYA_SCRIPT_PATH = MAYA_SCRIPT_PATH.split(';')
        for eachPath in MAYA_SCRIPT_PATH:
            if eachPath.endswith('maya/scripts'):
                return eachPath
    elif whatPath == 'LDMT':
        MAYA_SCRIPT_PATH = os.environ['MAYA_SCRIPT_PATH']
        MAYA_SCRIPT_PATH = MAYA_SCRIPT_PATH.split(';')
        for eachPath in MAYA_SCRIPT_PATH:
            if eachPath.endswith('maya/scripts'):
                MAYA_SCRIPT_PATH = eachPath
        return MAYA_SCRIPT_PATH + '/' + 'LDMT'

'''
Config
'''

def getLdmtConfig(section,option):
    cf = ConfigParser.ConfigParser()
    FOLDERNAME = getPath('LDMT').split('/')[-1]
    cfPath = getPath("MAYA_SCRIPT_PATH") + "/"  + FOLDERNAME + "/ldmt_config.ini"
    cf.read(cfPath)
    return cf.get(section,option)
## math ##

def round(number,pre):
    if number > 0:
        return float(int(number*10**pre+0.5))/10**pre
    else:
        return float(int(number*10**pre-0.5))/10**pre
def distance(pointA,pointB):
    return ((pointB[0]-pointA[0])**2+(pointB[1]-pointA[1])**2+(pointB[2]-pointA[2])**2)**(0.5)
## Plugins ##
def existsCmd(command):
    if not mel.eval('exists "'+command+'"'):
        return 0
    else:
        return 1
## Hotkeys ##
def getOrCreateCustomHotkeySet():
    allHotkey= cmds.hotkeySet( q=1, hsa=1 )
    currentHotkey = cmds.hotkeySet( q=1, current=1 )
    if currentHotkey == 'Maya_Default' and len(allHotkey)==1:
        cmds.hotkeySet( "MyHotkeySet", current=1 )
    elif currentHotkey == 'Maya_Default':
        for i in allHotkey:
            if i != "Maya_Default":
                cmds.hotkeySet(i,e=1,current=1)
    currentHotkey = cmds.hotkeySet( q=1, current=1 )
    return currentHotkey
## Tranforms ##
def freeze(sel):
    cmds.makeIdentity(sel,apply=True, t=1, r=1, s=1, n=0)
def movePivotToCenter(sel):
    selBB = cmds.polyEvaluate(sel,b=1)
    selBB_diff_x = selBB[0][1]-selBB[0][0]
    selBB_diff_y = selBB[1][1]-selBB[1][0]
    selBB_diff_z = selBB[2][1]-selBB[2][0]
    selBB_center_x = (selBB[0][1]+selBB[0][0])/2
    selBB_center_y = (selBB[1][1]+selBB[1][0])/2
    selBB_center_z = (selBB[2][1]+selBB[2][0])/2
    cmds.move(selBB_center_x, selBB_center_y, selBB_center_z, sel+".scalePivot", sel+".rotatePivot", absolute=True)
def moveObjToZero(sel):
    cmds.move(0,0,0,sel,rpr=1)
## Select ##
def ls( index="all", type = "transform" ):
    # if index is str and not indicating index, then we think this is a type and return all index
    if index != "all" and index != 0:
        type = index
    # specify each type
    if type == "transform":
        sel = cmds.ls( sl=1, type = type )
    elif type in ["poly","polygon","polymesh","mesh","obj"]:
        sel = cmds.ls (sl=1, type ="transform")
        sel = cmds.filterExpand(sel,sm=12)
    elif type in ["c","cr","curve","nurbsCurve"]:
        sel = cmds.ls (sl=1, type ="transform")
        sel = cmds.filterExpand(sel,sm=9)
    # specify index
    if index == "all" or isinstance(index,(str)):
        if sel == None:
            msg("Nothing Selected")
            return None
        return sel
    elif isinstance(index,(int)):
        if sel == None:
            msg("Nothing Selected")
            return None
        return sel[index]
## Warning ##
def msg(msg="Heads Up!"):
    global PM_startTime
    global PM_timeAdder
    PM_offset = 0
    PM_time = cmds.timerX(startTime = PM_startTime)
    PM_startTime = cmds.timerX()
    if PM_time<1.5:
        PM_offset = 10+20*(PM_timeAdder)
        PM_timeAdder = PM_timeAdder+1 
    else:
        PM_offset = 10
        PM_timeAdder = 0 
    if MAYA_version_float >= 2014:
        cmds.inViewMessage(
        amg = "<span style=\"color:#ffffff\">"+ msg +"</span>",
        fade = 1, fit = 150, fst = 800, fot = 150, fof = PM_offset, bkc = 0x2288ff, 
        pos = "topCenter", fontSize = 10, a = 0, ta = 0.68)
    print(msg)
# Get Mesh Info
def get(sel,what):
    if what == "uvid_uv":
        selMesh = MFnMesh(sel)
        uvid_uv = []
        uvArray = selMesh.getUVs()
        for i in xrange(len(uvArray[0])):
            uvid_uv.append([uvArray[0][i],uvArray[1][i]])
        return uvid_uv
    elif what == "vtxid_uvid":
        vtxid_uvid = []
        selVtxIter = MItMeshVertex(sel)
        while not selVtxIter.isDone():
            vtxid_uvid.append(list(set(selVtxIter.getUVIndices()))[0])
            selVtxIter.next()
        return vtxid_uvid
    elif what == "bb":
        return cmds.polyEvaluate(sel,b=1)
#API
def getDagPath(sel):
    selList = om2.MSelectionList()
    selList.add(sel)
    selPath = selList.getDagPath(0)
    return selPath
def MFnMesh(sel):
    selPath = getDagPath(sel)
    selMesh = om2.MFnMesh(selPath)
    return selMesh
def MItMeshVertex(sel):
    selPath = getDagPath(sel)
    selVtxIter = om2.MItMeshVertex(selPath)
    return selVtxIter
def MItMeshEdge(sel):
    selPath = getDagPath(sel)
    selEdgeIter = om2.MItMeshEdge(selPath)
    return selEdgeIter
def MItMeshPolygon(sel):
    selPath = getDagPath(sel)
    selPolyIter = om2.MItMeshPolygon(selPath)
    return selPolyIter
def MItMeshFaceVertex(sel):
    selPath = getDagPath(sel)
    selFaceIter = om2.MItMeshFaceVertex(selPath)
    return selFaceIter
#UVSet
def switchUVSet(sel):
    allUVSets = cmds.polyUVSet(sel,q=1,auv=1)
    firstUVSetName = allUVSets[0]
    secondUVSetName = allUVSets[1]
    currentUVSetName = cmds.polyUVSet(q=1,cuv=1)
    otherUVSetName = list( set(allUVSets).difference(set(currentUVSetName)))
    try:
        cmds.polyUVSet(sel,uvs = firstUVSetName, nuv=secondUVSetName, reorder=1)
    except:
        newUVSet = cmds.polyUVSet(sel,cr=1)
        newUVSet = newUVSet[0]
        cmds.polyUVSet(sel, uvs = firstUVSetName ,nuv= newUVSet, cp=1)
        cmds.polyUVSet(sel, uvs = secondUVSetName ,nuv= firstUVSetName, cp=1)
        cmds.polyUVSet(sel, uvs = newUVSet ,nuv= secondUVSetName, cp=1)
        cmds.polyUVSet(sel, uvs = newUVSet, d=1)
    if currentUVSetName == firstUVSetName:
        cmds.polyUVSet(sel,uvs = secondUVSetName , e=1,cuv=1)
    else:
        cmds.polyUVSet(sel,uvs = firstUVSetName , e=1,cuv=1)
    cmds.polyUVSet(sel,currentUVSet=1,uvSet=otherUVSetName)
#UI

def turnToolBtnOff(self,buttonName):
    windowName = self.window_name
    mainWindow = self.parentWidget() 
    ldmt_mainWindow = mainWindow.findChild(QMainWindow,'LDMT_mainUI')
    exec("buttonObj = ldmt_mainWindow.ui.%s"%(buttonName))
    buttonObj.setStyleSheet('\
    QPushButton{\
    border:1px solid rgb(30,30,30);\
    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(175, 175,175, 235), stop:1 rgba(235, 235, 235, 195));\
    color:rgb(25,25,25);}\
    QPushButton:hover{\
    border:1px solid rgb(30,30,30);\
    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(190, 190, 190, 225), stop:1 rgba(245, 245, 245, 195));\
    color:rgb(25,25,25);\
    }\
    QPushButton:pressed{ \
    border:1px solid rgb(30,30,30);\
    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(215, 215, 215, 195), stop:1 rgba(155, 155,155, 235));\
    color:rgb(25,25,25);}\
    ')
def showAttributeEditor():
    mel.eval("AttributeEditor;")
def showChannelBox():
    mel.eval("AttributeEditor;")
    cmds.ShowAttributeEditorOrChannelBox()

