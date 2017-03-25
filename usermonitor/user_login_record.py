import sys, os, types
sys.path.append("../..")
from server.sql import *
from user_monitor_sql import *
from user_monitor_library import getLocalHostAddr
from config import MONTH_ENGLISH_TO_DIGIT
from IP_login_monitor import updateIPLoginRecord

def formatLoginRecord(loginRecord, localHostAddr, currentYear):
    userName = loginRecord[0]
    if loginRecord[2] == ':0':
        loginIP = localHostAddr
        loginMethod = 'local'
    else:
        loginIP = loginRecord[2]
        loginMethod = 'remote'
    month = loginRecord[4]
    loginTime = currentYear + '-' + MONTH_ENGLISH_TO_DIGIT[month] + '-' + loginRecord[5] + ' ' + loginRecord[6]
    return userName, loginTime, loginIP, loginMethod

def addNewLoginRecordFromLast(db, newestLoginRecordFromDB, loginRecordFromLast, localHostAddr, currentYear):
    newLoginRecord = []
    for loginRecord in loginRecordFromLast:
        loginRecord = loginRecord.split()
        if loginRecord[0] == 'reboot':
            continue
        userName, loginTime, loginIP, loginMethod = formatLoginRecord(loginRecord, localHostAddr, currentYear)
        if userName == newestLoginRecordFromDB[1] and loginTime == newestLoginRecordFromDB[2] \
                and loginIP == newestLoginRecordFromDB[3] and loginMethod == newestLoginRecordFromDB[4]:
            break
        newLoginRecord.append([userName, loginTime, loginIP, loginMethod])
    if not newLoginRecord:
        return
    #print len(newLoginRecord)
    for i in range(len(newLoginRecord) - 1, -1, -1):
        insertIntoUserLoginRecord(db, newLoginRecord[i][0], newLoginRecord[i][1], newLoginRecord[i][2], newLoginRecord[i][3])
        updateIPLoginRecord(db, newLoginRecord[i][0], newLoginRecord[i][2])

def initLoginRecordFromLast(db, loginRecordFromLast, localHostAddr, currentYear):
    for loginRecord in loginRecordFromLast:
        loginRecord = loginRecord.split()
        if loginRecord[0] == 'reboot':
            continue
        userName, loginTime, loginIP, loginMethod = formatLoginRecord(loginRecord, localHostAddr, currentYear)
        insertIntoUserLoginRecord(db, userName, loginTime, loginIP, loginMethod)
        updateIPLoginRecord(db, userName, loginIP)

def updateLoginRecordFromLast(db):
    # select the latest data from USER_LOGIN_RECORD
    localHostAddr = getLocalHostAddr()
    currentYear = os.popen('date').readlines()[0].split()[-1]
    #cur = db.select('select * from USER_LOGIN_RECORD order by LOGIN_ID desc limit 0,1')
    #newestLoginRecordFromDB = cur.fetchall()
    newestLoginRecordFromDB = getNewestLoginRecord(db)
    loginRecordFromLast = os.popen('last').readlines()[:-2]
    if newestLoginRecordFromDB:
        addNewLoginRecordFromLast(db, newestLoginRecordFromDB[0], loginRecordFromLast, localHostAddr, currentYear)
    else:
        #print 'login record from DB is null!'
        loginRecordFromLast = loginRecordFromLast[::-1]
        initLoginRecordFromLast(db, loginRecordFromLast, localHostAddr, currentYear)
