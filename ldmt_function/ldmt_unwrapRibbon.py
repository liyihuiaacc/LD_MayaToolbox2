import maya.cmds as cmds
def unwrapRibbon():
    selList = cmds.ls(sl=1,o=1)
    selListPoly = cmds.filterExpand(selList,sm=12)
    selListEdge = cmds.polyListComponentConversion(selListPoly,te=1)
    selListFace = cmds.polyListComponentConversion(selListPoly,tf=1)
    selListUV = cmds.polyListComponentConversion(selListPoly,tuv=1)

    selListEdge = map(lambda x: x+'.e[*]', selListPoly)
    for i in selListEdge:
        cmds.polyMapCut(i,ch=1)
    cmds.polyForceUV(selListFace,unitize=1)
    for i in selListEdge:
        cmds.polyMapSewMove(i)