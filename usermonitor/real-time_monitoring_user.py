#!/usr/bin/env python
#coding:utf8
import sys, os, time
sys.path.append('.')
from server.sql import *
from config import DATABASE_PATH, MONTH_ENGLISH_TO_DIGIT
from current_login_user_monitor import getCurrentLoginUserFromWho, updateCurrentLoginUser
from user_login_record import updateLoginRecordFromLast
from user_command_operation_record import updateCommandOperationRecord

def test():
    import time
    while 1:
        print time.ctime(time.time())
        time.sleep(10)

def realTimeMonitoringUser():
    db = DBhandle(DATABASE_PATH)
    oldCurrentLoginUser = None
    userBashHistoryCount = {}
    while 1:
        # update currentLoginUser
        newCurrentLoginUser = getCurrentLoginUserFromWho()
        if newCurrentLoginUser != oldCurrentLoginUser:
            updateCurrentLoginUser(db, newCurrentLoginUser)
            oldCurrentLoginUser = newCurrentLoginUser

        # update users' loginRecord
        updateLoginRecordFromLast(db)

        # update command operation record
        updateCommandOperationRecord(db, userBashHistoryCount)
        time.sleep(1)

if __name__ == '__main__':
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit()
    except OSError, e:
        print >> sys.stderr, 'fork #1 failed: %d (%d)' % (e.errno, e.strerror)
        sys.exit(1)
    # test function test()
    #test()
    realTimeMonitoringUser()
