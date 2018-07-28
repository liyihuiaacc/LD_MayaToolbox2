#Liu Dian Xgits.com
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import maya.mel as mel
'''
ribbon unfolder
target is to unfold ribbon like faces from mesh
'''

def main():
    if not mel.eval('exists "u3dUnfold"'):
        cmds.loadPlugin('Unfold3D')
        
    selFaces = cmds.ls(sl=1)
    selFaces = cmds.ls(selFaces,fl=1)
    selObj = selFaces[0].split('.')[0]

    faceUnwarp(selFaces)
    selUVs = cmds.polyListComponentConversion(selFaces,ff=1,tuv=1)

    faceDic = getDic(selFaces)
    vtxid_uvid = faceDic[0]
    vtxid_edgeid = faceDic[1]
    edgeid_vtxid = faceDic[2]
    vtxid_faceid = faceDic[3]
    faceid_numTriangles = faceDic[4]
    edgeid_length = faceDic[5]

    triangles = 0
    for faceid in faceid_numTriangles:
        if faceid_numTriangles[faceid] == 1:
            triangles += 1
            
    startVtxid = -1
    for vtxid in vtxid_faceid:
        if len(vtxid_faceid[vtxid]) == 1 and faceid_numTriangles[vtxid_faceid[vtxid][0]] == 1:
            startVtxid = vtxid
    if startVtxid == -1:
        for vtxid in vtxid_faceid:
            if len(vtxid_faceid[vtxid]) == 1:
                startVtxid = vtxid
    vtxCount = len(vtxid_uvid)
    vtxLine0 = []
    vtxLine1 = []

    if triangles == 2 or triangles == 1:
        maxCount = vtxCount/2
        nextEdge0 = vtxid_edgeid[startVtxid][0]
        nextEdge1 = vtxid_edgeid[startVtxid][1]
        currentVtx0 = startVtxid
        currentVtx1 = startVtxid

            
        tempCount = 0
        while tempCount < maxCount:
            tempCount += 1
            nextVtxes = edgeid_vtxid[nextEdge0]
            for i in nextVtxes:
                if i != currentVtx0:
                    currentVtx0 = i
                    break
            vtxLine0.append(currentVtx0)
            nextEdges = vtxid_edgeid[currentVtx0]
            for i in nextEdges:
                if i != nextEdge0:
                    nextEdge0 = i
                    break
                    
        tempCount = 0
        while tempCount < maxCount:
            tempCount += 1
            nextVtxes = edgeid_vtxid[nextEdge1]
            for i in nextVtxes:
                if i != currentVtx1:
                    currentVtx1 = i
                    break
            vtxLine1.append(currentVtx1)
            nextEdges = vtxid_edgeid[currentVtx1]
            for i in nextEdges:
                if i != nextEdge1:
                    nextEdge1 = i
                    break
                    
        vtxLineIntersect = list(set(vtxLine0).intersection(set(vtxLine1)))

        vtxLine0String = []

        for i in vtxLine0:
            if not i in vtxLineIntersect:
                uvid = vtxid_uvid[i]
                vtxLine0String.append( selObj + '.map[' + str(uvid) + ']')
                
        vtxLine1String = []   
        for i in vtxLine1:
            if not i in vtxLineIntersect:
                uvid = vtxid_uvid[i]
                vtxLine1String.append( selObj + '.map[' + str(uvid) + ']')
                
        cmds.select(selFaces,r=1)    
        
        uvbb = cmds.polyEvaluate(selUVs,bc2=1)
        if (uvbb[0][1]-uvbb[0][0]) > (uvbb[1][1]-uvbb[1][0]) :
            cmds.polyEditUV(rot=1,angle=90)
                
        uvbb0 = cmds.polyEvaluate(vtxLine0String,bc2=1)
        uvbb1 = cmds.polyEvaluate(vtxLine1String,bc2=1)
        if uvbb0[0][0]<uvbb1[0][0]:
            cmds.polyEditUV(vtxLine0String, u=-1,r=0)
            cmds.polyEditUV(vtxLine1String, u=-0.9,r=0)
        else:
            cmds.polyEditUV(vtxLine0String, u=-0.9,r=0)
            cmds.polyEditUV(vtxLine1String, u=-1,r=0)    
        cmds.select(selUVs,r=1)
        cmds.select(vtxLine0String,d=1)
        cmds.select(vtxLine1String,d=1)
        cmds.unfold(i=5000,ss=0.001,gb=0,gmb=0.5,pub=0,ps=0,oa=0,us=0)
        cmds.unfold(selUVs,i=5000,ss=0,gb=0,gmb=0,pub=0,ps=0,oa=1,us=0)
        
    else:
        maxCount = vtxCount/2
        nextEdge0 = vtxid_edgeid[startVtxid][0]
        nextEdge1 = vtxid_edgeid[startVtxid][1]
        currentVtx0 = startVtxid
        currentVtx1 = startVtxid

            
        tempCount = 0
        while tempCount < maxCount:
            tempCount += 1
            nextVtxes = edgeid_vtxid[nextEdge0]
            for i in nextVtxes:
                if i != currentVtx0:
                    currentVtx0 = i
                    break
            vtxLine0.append(currentVtx0)
            nextEdges = vtxid_edgeid[currentVtx0]
            for i in nextEdges:
                if i != nextEdge0:
                    nextEdge0 = i
                    break
                    
        tempCount = 0
        while tempCount < maxCount:
            tempCount += 1
            nextVtxes = edgeid_vtxid[nextEdge1]
            for i in nextVtxes:
                if i != currentVtx1:
                    currentVtx1 = i
                    break
            vtxLine1.append(currentVtx1)
            nextEdges = vtxid_edgeid[currentVtx1]
            for i in nextEdges:
                if i != nextEdge1:
                    nextEdge1 = i
                    break
                    
        vtxLineIntersect = list(set(vtxLine0).intersection(set(vtxLine1)))

        vtxLine0String = []

        for i in vtxLine0:
            if not i in vtxLineIntersect:
                uvid = vtxid_uvid[i]
                vtxLine0String.append( selObj + '.map[' + str(uvid) + ']')
                
        vtxLine1String = []   
        for i in vtxLine1:
            if not i in vtxLineIntersect:
                uvid = vtxid_uvid[i]
                vtxLine1String.append( selObj + '.map[' + str(uvid) + ']')
                    
        uvbb = cmds.polyEvaluate(selUVs,bc2=1)
        cmds.select(selFaces,r=1)
        if (uvbb[0][1]-uvbb[0][0]) > (uvbb[1][1]-uvbb[1][0]) :
            cmds.polyEditUV(rot=1,angle=90)
        cmds.unfold(selUVs,i=5000,ss=0,gb=0,gmb=0,pub=0,ps=0,oa=1,us=0)
        
        
    uvbb = cmds.polyEvaluate(selUVs,bc2=1)
    scale = 1/(uvbb[1][1]-uvbb[1][0])
    moveV = 0.5-(uvbb[1][1]+uvbb[1][0])/2
    cmds.polyEditUV(selUVs,v=moveV)
    cmds.polyEditUV(selUVs,s=1,su=scale,sv=scale,pu=-1,pv=0.5)
    length_vtxes = cmds.polyListComponentConversion(vtxLine0String,fuv=1,tv=1)
    length_edges = cmds.polyListComponentConversion(length_vtxes,fv=1,te=1,internal=1)
    cmds.select(vtxLine0String,r=1)
    edgeuvbb = cmds.polyEvaluate(vtxLine0String,bc2=1)
    uvheight = edgeuvbb[1][1] - edgeuvbb[1][0]
    edgesLength = 0
    length_edges = cmds.ls(length_edges,fl=1)
    for edgeid in length_edges:
        edgesLength += edgeid_length[int(edgeid.split('[')[1][:-1])]
    densityScale = edgesLength/uvheight
    cmds.polyEditUV(selUVs,s=1,su=densityScale,sv=densityScale,pu=-1,pv=0.5)
    cmds.select(selUVs,r=1)

def faceUnwarp(selFaces):
    selEdges = cmds.polyListComponentConversion(selFaces,ff=1,te=1)
    selEdges = cmds.ls(selEdges, fl=1)
    selBorderEdges = cmds.polyListComponentConversion(selFaces,bo=1,ff=1,te=1)
    selBorderEdges = cmds.ls(selBorderEdges, fl=1)
    selInnerEdges = list( set(selEdges) - set(selBorderEdges))
    cmds.polyMapCut(selEdges,ch=1)
    cmds.polyForceUV(selFaces,unitize=1)
    cmds.polyMapSewMove(selInnerEdges)
    
def getDic(selFaces):
    sel = selFaces[0].split('.')[0]
    selList = om2.MSelectionList()
    selList.add(sel)
    selPath = selList.getDagPath(0)
    selFaceIter = om2.MItMeshPolygon(selPath)
    selVtxIter = om2.MItMeshVertex(selPath)
    selEdgeIter = om2.MItMeshEdge(selPath)

    selFaceids = getId(selFaces)

    #get faceid_uvid
    faceid_uvid = {}
    faceid_vtxid = {}
    faceid_edgeid = {}
    faceid_numTriangles = {}
    while not selFaceIter.isDone():  # get {[[uvid1,uvid2,uvid3,uvid4], ...] }
        faceIndex = selFaceIter.index() 
        if faceIndex in selFaceids:
            verts = selFaceIter.getVertices()
            uvids=[]
            for index in xrange(len(verts)):        
                uvids.append(selFaceIter.getUVIndex(index)) #necessary for uvedgeid
            faceid_uvid[faceIndex] = uvids
            faceid_vtxid[faceIndex] = selFaceIter.getVertices()
            faceid_edgeid[faceIndex] = selFaceIter.getEdges()
            faceid_numTriangles[faceIndex] = selFaceIter.numTriangles()
        selFaceIter.next(None)
        
    selUvs = cmds.polyListComponentConversion(selFaces, ff=1, tuv=1)
    selUvs = cmds.ls(selUvs,fl=1)
    selUvids = getId(selUvs)
    selVtxes = cmds.polyListComponentConversion(selFaces, ff=1, tv=1)
    selVtxes = cmds.ls(selVtxes,fl=1)
    selVtxids = getId(selVtxes)

    vtxid_uvid = {}
    vtxid_edgeid = {}
    vtxid_faceid = {}
    selEdges = cmds.polyListComponentConversion(selFaces, ff=1, te=1, bo=1)
    selEdges = cmds.ls(selEdges,fl=1)
    selEdgeids = getId(selEdges)

    edgeid_vtxid = {}
    edgeid_length = {}
    while not selEdgeIter.isDone():
        edgeIndex = selEdgeIter.index()
        if selEdgeIter.onBoundary():
            selEdgeids.append(edgeIndex)
        if edgeIndex in selEdgeids:
            edgeid_vtxid[edgeIndex] = [selEdgeIter.vertexId(0) , selEdgeIter.vertexId(1)]
            edgeid_length[edgeIndex] = selEdgeIter.length()
        selEdgeIter.next()
        
    while not selVtxIter.isDone():
        vtxIndex = selVtxIter.index()
        if vtxIndex in selVtxids:
            uvids = selVtxIter.getUVIndices()
            for uvid in uvids:
                if uvid in selUvids:
                    vtxid_uvid[vtxIndex] = uvid
            edges = selVtxIter.getConnectedEdges()
            for edge in edges:
                if edge in selEdgeids:
                    try:
                        vtxid_edgeid[vtxIndex].append(edge)
                    except:
                        vtxid_edgeid[vtxIndex] = [edge]
            connectedFaces = selVtxIter.getConnectedFaces()
            faces = []
            for face in connectedFaces:
                if face in selFaceids:
                    faces.append(face)
            vtxid_faceid[vtxIndex] = faces
        selVtxIter.next()
    return vtxid_uvid, vtxid_edgeid, edgeid_vtxid, vtxid_faceid, faceid_numTriangles, edgeid_length
    
    #get vtxid_uvid
    
def getId(stringArray):
    idArray = []
    for i in stringArray:
        idArray.append(int(i.split('[')[1][:-1]))
    return idArray
        
if __name__ == "__main__":
    main()
