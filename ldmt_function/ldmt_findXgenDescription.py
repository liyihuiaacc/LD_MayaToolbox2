import xgenm as xg
import xgenm.ui as xgui
from ldmaya import ldmaya as ld
def findXgenDescription():
    sel = ld.ls(0)
    description = xg.geometryPatches(sel)
    description = description[0].split('_')[1]
    abc = xgui.createDescriptionEditor()
    abc.setCurrentDescription(str(description))
    return description