import sys, os
import shutil
import subprocess
sys.path.append('.')
from server.usermonitor.config import HOME_DIR, GLOBAL_BASHRC_PATH, ALIAS_RM, UNALIAS_RM

# global alias and unalias
def modify_rm_implement():
    alias_rm(GLOBAL_BASHRC_PATH)

def recovery_rm_implement():
    unalias_rm(GLOBAL_BASHRC_PATH)

def alias_rm(filePath):
    addOneLine(filePath, ALIAS_RM)
    deleteOneLine(filePath, UNALIAS_RM)
    sourceTheFile(filePath)

def unalias_rm(filePath):
    addOneLine(filePath, UNALIAS_RM)
    sourceTheFile(filePath)

# for user
def generateAllUserBashrcPath():
    parentDir = HOME_DIR
    userBashrcPathList = []
    userNames = os.listdir(parentDir)
    if len(userNames) > 0:
        for userName in userNames:
            fullUserBashrcPath = os.path.join(parentDir, userName, '.bashrc')
            userBashrcPathList.append(fullUserBashrcPath)
    return userBashrcPathList

def modify_rm_implement_users(userBashrcPathList):
    for userBashrcPath in userBashrcPathList:
        addOneLine(userBashrcPath, ALIAS_RM)
        sourceTheFile(userBashrcPath)

def recovery_rm_implement_users(userBashrcPathList):
    for userBashrcPath in userBashrcPathList:
        deleteOneLine(userBashrcPath, ALIAS_RM)
        sourceTheFile(userBashrcPath)

# common
def addOneLine(filePath, alias):
    with open(filePath, 'r') as f:
        for line in f.readlines():
            if alias in line:
                return
    with open(filePath, 'a') as f:
        f.write(alias)

def deleteOneLine(filePath, alias):
    outfilePath = os.path.dirname(filePath) + 'outfile.delete'
    with open(filePath, 'r') as f:
        with open(outfilePath, 'w') as outf:
            for line in f.readlines():
                if alias not in line:
                    outf.write(line)
    shutil.move(outfilePath, filePath)

def sourceTheFile(filePath):
    shellCommand =  "source " + filePath
    subprocess.Popen(shellCommand, shell=True, executable='/bin/bash')

if __name__ == '__main__':
    userBashrcPathList = generateAllUserBashrcPath()
    filePath = GLOBAL_BASHRC_PATH
    alias_rm(filePath)
    unalias_rm(filePath)
