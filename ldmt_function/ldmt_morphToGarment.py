import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2
    
def morph2UV(baseObj):
    sel = baseObj
    selList = om2.MSelectionList()
    selList.add(sel)
    path = selList.getDagPath(0)
    myMesh = om2.MFnMesh(path)
    newPointArray = om2.MPointArray()
    space = om2.MSpace.kWorld
    myMesh_UVs = myMesh.getUVs()
    myMesh_points = myMesh.getPoints()
    # for i in range(myMesh.numVertices):
    myMesh_itVertex = om2.MItMeshVertex(path)
    points = om2.MPointArray()
    while not myMesh_itVertex.isDone():
        vertIndex = myMesh_itVertex.index()
        gotUV = myMesh_itVertex.getUV()
        point = om2.MPoint(gotUV[0],gotUV[1],0)
        points.append(point)
        myMesh_itVertex.next()
    myMesh.setPoints(points,space)
    
def runMorph2UV(sel):
    baseObjDup = cmds.duplicate(sel)
    baseObj = baseObjDup[0]
    morph2UV(baseObj)
    return baseObj