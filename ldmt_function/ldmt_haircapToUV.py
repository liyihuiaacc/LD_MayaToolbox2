import maya.cmds as cmds
import maya.api.OpenMaya as om2

def haircapToUV():
    sel=cmds.ls(sl=1,o=1)
    sel=sel[0]
    duplicatedSelToMorph = cmds.duplicate(sel)
    duplicatedSelToMorph = duplicatedSelToMorph[0]
    faceArea = cmds.polyEvaluate(sel+'.f[*]',fa=1)
    selList = om2.MSelectionList()
    selList.add(sel)
    selPath = selList.getDagPath(0)
    myMesh = om2.MFnMesh(selPath)
    space = om2.MSpace.kWorld

    myMesh_itVertex = om2.MItMeshVertex(selPath)
    points = om2.MPointArray()
    while not myMesh_itVertex.isDone():
        vertIndex = myMesh_itVertex.index()
        gotUV = myMesh_itVertex.getUV()
        points.append((gotUV[0],gotUV[1],0))
        myMesh_itVertex.next()
    myMesh.setPoints(points,space)

    faceArea_morphed = cmds.polyEvaluate(sel+'.f[*]',fa=1)
    scaleValue = (sum(faceArea)/sum(faceArea_morphed))**(0.5)
    polyPlane = cmds.polyPlane()
    cmds.rotate('90deg', 0, 0, polyPlane[0] )
    cmds.move(0.5,0.5,polyPlane[0])
    cmds.move(0,0,0,polyPlane[0]+".scalePivot",polyPlane[0]+".rotatePivot", absolute=1)
    cmds.scale(scaleValue,scaleValue,scaleValue,polyPlane[0])

    cmds.move(0,0,0,sel+".scalePivot",sel+".rotatePivot", absolute=1)
    cmds.scale(scaleValue,scaleValue,scaleValue,sel)

    cmds.blendShape(duplicatedSelToMorph,sel,o="world")
