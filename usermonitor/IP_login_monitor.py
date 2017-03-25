import sys, os
import shutil
sys.path.append('../..')
sys.path.append('.') # for test
from server.sql import *
from user_monitor_sql import *
#from user_monitor_sql import getIPLoginRecord, insertIntoBlacklist, insertIntoIPLoginRecord, ifExistIPLoginRecord, selectOneLoginIP, deleteFromBlacklist
from config import DATABASE_PATH, HOSTS_ALLOW_PATH, HOSTS_DENY_PATH

def deleteOneLine(filePath, keywords):
    keywords = ':' + keywords + ':'
    dirName = os.path.dirname(filePath)
    outfilePath = dirName + '/outfile.allow'
    with open(filePath, 'r') as f:
        with open(outfilePath, 'w') as outf:
            for line in f.readlines():
                if keywords not in line:
                    #print 'write into ...'
                    outf.write(line)
    shutil.move(outfilePath, filePath)

def ifExistOneLine(filePath, keywords):
    keywords = ':' + keywords + ':'
    with open(filePath, 'r') as f:
        for line in f.readlines():
            if keywords in line:
                return True
    return False

def updateIPLoginRecord(db, userName, loginIP):
    exist = ifExistIPLoginRecord(db, userName, loginIP)
    #print "exist in IP_login_monitor userName, loginIP, exsit: %s, %s, %s" % (userName, loginIP, exist)
    if not exist:
        #print 'not exist'
        insertIntoIPLoginRecord(db, userName, loginIP)

def getIPLoginRecordSet(db):
    IPLoginRecord = getIPLoginRecord(db)
    return IPLoginRecord

def denyLoginIP(db, loginIP):
    # delete loginIP from /etc/hosts.allow
    #open("outfile.allow", "w").write(''.join(map(lambda x: loginIP in x and "\n" or x, open("/etc/hosts.allow", "r"))))
    deleteOneLine(HOSTS_ALLOW_PATH, loginIP)

    # add loginIP into /etc/hosts.deny
    if not ifExistOneLine(HOSTS_DENY_PATH, loginIP):
        newLine = 'sshd:'+loginIP+':deny'
        os.popen('echo ' + newLine + ' >> /etc/hosts.deny')

    # add loginIP into blacklist
    if not selectOneLoginIP(db, loginIP):
        #print 'add IP into blacklist'
        addIPIntoBlacklist(db, loginIP)

def allowLoginIP(loginIP):
    # add loginIP into /etc/hosts.allow
    if not ifExistOneLine(HOSTS_ALLOW_PATH, loginIP):
        newLine = 'sshd:'+loginIP+':allow'
        os.popen('echo ' + newLine + ' >> /etc/hosts.allow')
    # delete loginIP from blacklist
    if selectOneLoginIP(db, loginIP):
        #print 'in blacklist.'
        deleteIPFromBlacklist(db, loginIP)

# IP white list, interaction with database
def addIPIntoWhitelist(db, loginIP):
    insertIntoWhitelist(db, loginIP)

def deleteIPFromWhitelist(db, loginIP):
    deleteFromWhitelist(db, loginIP)

# IP black list, interaction with database
def addIPIntoBlacklist(db, loginIP):
    insertIntoBlacklist(db, loginIP)

def deleteIPFromBlacklist(db, loginIP):
    deleteFromBlacklist(db, loginIP)

if __name__ == '__main__':
    db = DBhandle(DATABASE_PATH)
    #IP = getIPLoginRecord(db)
    #addIPIntoBlacklist(db, '192.168.4.23')
    #insertIntoIPLoginRecord(db, 'llf', '192.168.4.21')
    #re = ifExistIPLoginRecord(db, 'llf', '192.168.95.138')
    #print re
    #allowLoginIP('192.168.95.1')
    #denyLoginIP(db, '192.168.95.1')
    #insertIntoWhitelist(db, '192.168.95.1')
    deleteFromWhitelist(db, '192.168.95.1')
