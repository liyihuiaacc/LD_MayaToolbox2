import os
import shutil
import maya.cmds as cmds
def sourceToTarget(root_src_dir,root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)

def getMayaScriptPath():
    mayaScriptPath = os.environ['MAYA_SCRIPT_PATH']
    mayaScriptPath = mayaScriptPath.split(';')
    for eachPath in mayaScriptPath:
        if eachPath.endswith('maya/scripts'):
            mayaScriptPath = eachPath
    return mayaScriptPath
    
def resetPref():
    mayaScriptPath = getMayaScriptPath()
    mayaDocPath = mayaScriptPath[:-8]
    mayaVersion = cmds.about(v=1)
    try:
        if int(mayaVersion)<2016:
            return
    except:
        return 
    mayaVersionPath = mayaDocPath+'/'+mayaVersion
    tempVersionPath = mayaDocPath+'/temp/'+mayaVersion
    if not os.path.isdir(tempVersionPath):
        os.mkdir(tempVersionPath)
    # first copy the files to temp
    hotkeyPath = '/prefs/hotkeys'
    shelvesPath = '/prefs/shelves'
    iconPath = '/prefs/icons'
    scriptsPath = '/scripts'
    userNamedCmdPath = '/prefs/userNamedCommands.mel'
    userRunTimeCmdPath = '/prefs/userRunTimeCommands.mel'
    allPath = [hotkeyPath, iconPath, shelvesPath, scriptsPath, userNamedCmdPath, userRunTimeCmdPath]
    srcAllPath = []
    tempAllPath = []
    
    for i in range(len(allPath)):
        srcAllPath.append(mayaVersionPath + allPath[i])
        tempAllPath.append(tempVersionPath + allPath[i])
    for i in range(len(srcAllPath)):
        try:
            if os.path.isdir(srcAllPath[i]):
                sourceToTarget(srcAllPath[i],tempAllPath[i])
            else:
                shutil.copy(srcAllPath[i],tempAllPath[i])
        except:
            pass
    shutil.rmtree(mayaVersionPath)
    os.mkdir(mayaVersionPath)
    
    for i in range(len(tempAllPath)):
        try:
            if os.path.isdir(tempAllPath[i]):
                sourceToTarget(tempAllPath[i],srcAllPath[i])
            else:
                shutil.copy(tempAllPath[i],srcAllPath[i])
        except:
            pass
    shutil.rmtree(tempVersionPath)
    # call maya.exe
    mayaPath =  os.environ['MAYA_LOCATION']
    mayaExePath = mayaPath+"/bin/maya.exe"
    os.startfile(mayaExePath)
