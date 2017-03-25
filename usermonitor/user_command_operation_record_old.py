import sys
import sqlite3
sys.path.append('../..')
sys.path.append('.')
from server.sql import *
from user_monitor_sql import *
from config import DATABASE_PATH

def generateBashHistoryPath(currentLoginUser):
    bashHistoryPath = {}
    for userName in currentLoginUser:
        strName = ''.join(userName)
        bashHistoryPath[strName] = '/home/'+strName+'/.bash_history'
    return bashHistoryPath

def getCurrentLoginUserFromDB(db):
    currentLoginUser = getCurrentLoginUser(db)
    return currentLoginUser

def initCommandOperationRecord(db, bashHistoryPath, userBashHistoryCount):
    defaultOperationTime = '2017-03-20 16:42:20'
    if not bashHistoryPath:
        return
    for userName in bashHistoryPath.keys():
        with open(bashHistoryPath[userName]) as f:
            lines = f.readlines()
            userBashHistoryCount[userName] = len(lines)
            for line in lines:
                commandName = line.strip('\n')
                insertIntoCommandOperationRecord(db, userName, defaultOperationTime, commandName)

def addNewCommandOperationRecord(db, bashHistoryPath, userBashHistoryCount):
    defaultOperationTime = '2017-03-20 16:42:20'
    if not bashHistoryPath:
        return
    for userName in bashHistoryPath.keys():
        with open(bashHistoryPath[userName]) as f:
            lines = f.readlines()
            count = len(lines)
            if userBashHistoryCount.has_key(userName):
                start = userBashHistoryCount[userName]
                lines = lines[start:]
            userBashHistoryCount[userName] = count
            for line in lines:
                commandName = line.strip('\n')
                insertIntoCommandOperationRecord(db, userName, defaultOperationTime, commandName)

def updateCommandOperationRecord(db, userBashHistoryCount):
    currentLoginUser = getCurrentLoginUserFromDB(db)
    bashHistoryPath = generateBashHistoryPath(currentLoginUser)
    allCommandRecord = getAllCommandOperationRecord(db)
    if not allCommandRecord:
        initCommandOperationRecord(db, bashHistoryPath, userBashHistoryCount)
    else:
        addNewCommandOperationRecord(db, bashHistoryPath, userBashHistoryCount)

if __name__ == '__main__':
    db = DBhandle(DATABASE_PATH)
    emptyCommandOperationRecord(db)
    #userBashHistoryCount = {}
    #updateCommandOperationRecord(db, userBashHistoryCount)
    #updateCommandOperationRecord(db, userBashHistoryCount)

