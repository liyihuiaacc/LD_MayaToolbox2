import maya.cmds as cmds
import maya.mel as mel
def normalFacet():
    sel = cmds.ls(sl=1,o=1)
    cmds.polyNormalPerVertex(sel,ufn=1)
    mel.eval('SetToFaceNormals;')
    mel.eval('DeleteHistory;')
