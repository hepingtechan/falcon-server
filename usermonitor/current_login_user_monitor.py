import sys, os
from user_monitor_library import getLocalHostAddr
from user_monitor_sql import emptyCurrentLoginUser, insertIntoCurrentLoginUser

'''
def getLocalHostAddr():
    localHostAddr = os.popen("ifconfig eth0 | grep 'inet addr' \
                             | awk '{print $2}' | awk -F: '{print $2}'").readlines()
    localHostAddr = localHostAddr[0].split()
    return localHostAddr[0]
'''

def offlineTheUser(ttyNumber):
    pid = os.popen('ps -ef | grep %s' % ttyNumber).readlines()[0].split()[1]
    #print 'pid: %s' % pid
    os.popen('kill -9 %s' % pid)

def getCurrentLoginUserFromWho():
    currentLoginUser = os.popen('who').readlines()
    return currentLoginUser

def updateCurrentLoginUser(db, newCurrentLoginUser):
    emptyCurrentLoginUser(db)
    userID = 0
    #usersInfo = os.popen('who').readlines()
    localHostAddr = getLocalHostAddr()
    for userInfo in newCurrentLoginUser:
        userID += 1
        userInfo = userInfo.split()
        ttyNumber = userInfo[1]
        userName = userInfo[0]
        loginTime = userInfo[2] + ' ' + userInfo[3]
        loginIP = userInfo[4][1:-1]
        loginMethod = 'remote'
        if loginIP == ':0':
            loginIP = localHostAddr
            loginMethod = 'local'
        insertIntoCurrentLoginUser(db, userID, userName, loginTime, loginIP, loginMethod, ttyNumber)

if __name__ == '__main__':
    ttyNumber = 'pts/35'
    offlineTheUser(ttyNumber)
