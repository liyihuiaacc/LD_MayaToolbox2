#LDMT#LDMT beta
#Dont't Edit Anythin Within #LDMT (Including #LDMT)

import sys
import os
import maya.cmds as cmds
import maya.mel as mel

MAYA_SCRIPT_PATH = os.environ['MAYA_SCRIPT_PATH']
MAYA_SCRIPT_PATH = MAYA_SCRIPT_PATH.split(';')
for eachPath in MAYA_SCRIPT_PATH:
    if eachPath.endswith('maya/scripts'):
        MAYA_SCRIPT_PATH = eachPath
LDMTPATH = MAYA_SCRIPT_PATH + '/' + 'LDMT' 
sys.path.insert(0,LDMTPATH)
sys.path.insert(0,LDMTPATH+'/ldmt_function')

cmds.evalDeferred("import ldmt_ui")
cmds.evalDeferred("reload(ldmt_ui)")
cmds.evalDeferred("from ldmt_ui import *")
cmds.evalDeferred("ldmt_globalUI = show()") 

#LDMT