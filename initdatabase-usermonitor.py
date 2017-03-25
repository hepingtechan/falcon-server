# -*- coding: UTF-8 -*-

#在程序安装时初始化数据库, 创建表格及默认配置

import sqlite3

#
DB_tables = [
    ('CURRENT_LOGIN_USER','''(USER_ID INTEGER PRIMARY KEY NOT NULL,
           USER_NAME      TEXT        NOT NULL,
           LOGIN_TIME     DATETIME    NOT NULL,
           LOGIN_IP       CHAR(15)    NOT NULL,
           LOGIN_METHOD   CHAR(10)    NOT NULL,
           TTY_NUMBER     TEXT        NOT NULL);'''),
    ('USER_LOGIN_RECORD','''(LOGIN_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
           USER_NAME      TEXT        NOT NULL,
           LOGIN_TIME     DATETIME    NOT NULL,
           LOGIN_IP       CHAR(15)    NOT NULL,
           LOGIN_METHOD   CHAR(10)    NOT NULL);'''),
    ('USER','''(USER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
           USER_NAME      TEXT        NOT NULL,
           SECURITY_SCORE TINYINT(3));'''),
    ('COMMAND_OPERATION_RECORD', '''(OPERATION_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
           USER_NAME      TEXT        NOT NULL,
           OPERATION_TIME DATETIME    NOT NULL,
           COMMAND_NAME   CHAR(100)   NOT NULL);'''),
    ('IP_LOGIN_RECORD', '''(IP_LOGIN_RECORD_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
           USER_NAME      TEXT        NOT NULL,
           LOGIN_IP             CHAR(15)    NOT NULL);'''),
    ('LOGIN_IP_BLACKLIST', '''(LOGIN_IP_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
           LOGIN_IP       CHAR(15)    NOT NULL);'''),
    ('LOGIN_IP_WHITELIST', '''(LOGIN_IP_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
           LOGIN_IP       CHAR(15)    NOT NULL);''')]


class InitDB(object):
	"""初始化数据库表"""
	def __init__(self, tables, db_file):
		self.db_tables = tables
		self.db_file = db_file
		self.setupDBcon()
		self.initDBTables()

	def __del__(self):
		if self.con:
			print 'db disconnect!'
			self.con.close()

	def setupDBcon(self):
		self.con = sqlite3.connect(self.db_file)
		self.cur = self.con.cursor()

	def initDBTables(self):
		self.dropTables() # noted by huangxiaofang 20170227
		self.createTables()

	def dropTables(self):
		print 'drop tables!'
		for table in self.db_tables:
			try:
				self.cur.execute("DROP TABLE IF EXISTS %s"%table[0])
			except Exception,e:
				print Exception, ':', e
				continue

	def createTables(self):
		print 'create tables!'
		for table in self.db_tables:
			try:
				self.cur.execute("CREATE TABLE IF NOT EXISTS %s %s"%(table[0], table[1]))
			except Exception,e:
				print Exception, ':', e
				continue


if __name__ == '__main__':
    #a = InitDB(DB_tables, 'server/database/test.db') # noted by huangxiaofang 20170227
    a = InitDB(DB_tables, 'database/user-monitor.db') # added by huangxiaofang 20170227



