import maya.cmds as cmds
import maya.api.OpenMaya as om2
from ldmaya import ldmaya as ld

def xgenRibbonAlignUV():
    sel = ld.ls('mesh')
    selLengthList = xgenRibbonAlignUV_getRibbonsLength(sel)
    selLengthArrayWithDiffV = selLengthList.values()
    selLengthArray = []
    for i in selLengthArrayWithDiffV:
        selLengthArray.append(i[0])
    selLengthArray.sort()
    maxLength = selLengthArray[-1]

    for each in sel:
        uvid_uv = ld.get(each,'uvid_uv')
        cmds.polyEditUV(each+'.map[*]', scaleV = -1 * 0.98 /selLengthList[each][1] * selLengthList[each][0]/maxLength, scaleU = 0.9)
        eachUV0 = cmds.polyEditUV(each+'.map[0]',q=1)
        vUp = 0.99 - eachUV0[1] 
        cmds.polyEditUV(each+'.map[*]', v = vUp, u = 0.05)
        
def xgenRibbonAlignUV_getRibbonsLength(sel):
    selLengthList = {}
    for eachRibbon in sel:
        selMesh = ld.MFnMesh(eachRibbon)
        space = om2.MSpace.kWorld
        pointsPos = selMesh.getPoints(space)
        
        subdivWidthDiffV = xgenRibbonAlignUV_getRibbonSubdiv(eachRibbon)
        subdivWidth = subdivWidthDiffV[0]
        diffV = subdivWidthDiffV[1]
        vtxNum = subdivWidthDiffV[2]
        vtxPairId = xgenRibbonAlignUV_getCurveVtxPair(subdivWidth,vtxNum)
        curvelength = 0
        for i in vtxPairId:
            vtxPointA = pointsPos[i[0]]
            vtxPointB = pointsPos[i[1]]
            curvelength += ld.distance(vtxPointA,vtxPointB)
        selLengthList[eachRibbon] = [curvelength,diffV]
    return selLengthList
    
def xgenRibbonAlignUV_getCurveVtxPair(subdivWidth,vtxNum):
    vtxPairId = []
    for i in range(vtxNum/(subdivWidth+1)-1):
        vtxPairId.append([i*(subdivWidth+1),(i+1)*(subdivWidth+1)]) 
    return vtxPairId

def xgenRibbonAlignUV_getRibbonSubdiv(sel):
    uvid_uv = ld.get(sel,'uvid_uv')
    subdivWidth = 1
    vtxNum = len(uvid_uv)
    for i in range(vtxNum):
        if (uvid_uv[i][0] - uvid_uv[vtxNum-1][0])<0.01:
            subdivWidth = i
            break
    diffV = uvid_uv[vtxNum-1][1]-uvid_uv[0][1]
    return subdivWidth,diffV,vtxNum