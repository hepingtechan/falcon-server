import sys
sys.path.append('../..')
from server.sql import *
from config import DATABASE_PATH

# command operation record
def insertIntoCommandOperationRecord(db, userName, operationTime, commandName):
    sql = "INSERT INTO COMMAND_OPERATION_RECORD (USER_NAME, OPERATION_TIME, COMMAND_NAME) VALUES ('%s', '%s', '%s')" % (userName, operationTime, commandName)
    db.execute(sql)

def getCurrentLoginUser(db):
    sql = "SELECT DISTINCT USER_NAME FROM CURRENT_LOGIN_USER"
    cur = db.execute(sql)
    return cur.fetchall()

def getAllCommandOperationRecord(db):
    sql = "SELECT * from COMMAND_OPERATION_RECORD"
    cur = db.execute(sql)
    return cur.fetchall()

def emptyCommandOperationRecord(db):
    sql = "DELETE FROM COMMAND_OPERATION_RECORD"
    cur = db.execute(sql)

# ip login irecord
def getNewestLoginRecord(db):
    sql = "SELECT * from USER_LOGIN_RECORD order by LOGIN_ID desc limit 0,1"
    cur = db.execute(sql)
    return cur.fetchall()

def ifExistIPLoginRecord(db, userName, loginIP):
    sql = "SELECT * FROM IP_LOGIN_RECORD WHERE USER_NAME='%s' and LOGIN_IP='%s'" % (userName, loginIP)
    cur = db.execute(sql)
    return cur.fetchall()

def insertIntoIPLoginRecord(db, userName, loginIP):
    sql = "INSERT INTO IP_LOGIN_RECORD (USER_NAME, LOGIN_IP) VALUES ('%s', '%s')" % (userName, loginIP)
    db.execute(sql)

def insertIntoWhitelist(db, loginIP):
    sql = "INSERT INTO LOGIN_IP_WHITELIST (LOGIN_IP) VALUES ('%s')" % loginIP
    db.execute(sql)

def deleteFromWhitelist(db, loginIP):
    sql = "DELETE FROM LOGIN_IP_WHITELIST WHERE LOGIN_IP='%s'" % loginIP
    db.execute(sql)

def insertIntoBlacklist(db, loginIP):
    sql = "INSERT INTO LOGIN_IP_BLACKLIST (LOGIN_IP) VALUES ('%s')" % loginIP
    db.execute(sql)

def deleteFromBlacklist(db, loginIP):
    sql = "DELETE FROM LOGIN_IP_BLACKLIST WHERE LOGIN_IP='%s'" % loginIP
    db.execute(sql)

def selectOneLoginIP(db, loginIP):
    sql = "SELECT LOGIN_IP FROM LOGIN_IP_BLACKLIST WHERE LOGIN_IP='%s'" % loginIP
    cur = db.execute(sql)
    return cur.fetchall()

def getIPLoginRecord(db):
    sql = "SELECT LOGIN_IP, LOGIN_TIME FROM USER_LOGIN_RECORD"
    cur = db.execute(sql)
    return cur.fetchall()

# current login user
def emptyCurrentLoginUser(db):
    sql = "DELETE FROM CURRENT_LOGIN_USER"
    db.execute(sql)

def insertIntoCurrentLoginUser(db, userID, userName, loginTime, loginIP, loginMethod, ttyNumber):
    sql = "INSERT INTO CURRENT_LOGIN_USER (USER_ID, USER_NAME, LOGIN_TIME, LOGIN_IP, LOGIN_METHOD, TTY_NUMBER) \
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (userID, userName, loginTime, loginIP, loginMethod, ttyNumber)
    db.execute(sql)

# user login record
def insertIntoUserLoginRecord(db, userName, loginTime, loginIP, loginMethod):
    sql = "INSERT INTO USER_LOGIN_RECORD (USER_NAME, LOGIN_TIME, LOGIN_IP, LOGIN_METHOD) \
        VALUES ('%s', '%s', '%s', '%s')" % (userName, loginTime, loginIP, loginMethod)
    db.execute(sql)

if __name__ == '__main__':
    db = DBhandle(DATABASE_PATH)
    #insertIntoUserLoginRecord(db, 'llf', '2017-03-08 18:49', '192.178.3.23', 'local')
    #insertIntoCurrentLoginUser(db, 'llf', '2017-03-08 18:49', '192.178.3.23', 'local', 'pts/34')
    emptyCurrentLoginUser(db)
