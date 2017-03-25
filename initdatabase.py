# -*- coding: UTF-8 -*-  

#在程序安装时初始化数据库, 创建表格及默认配置

import sqlite3

#
DB_tables = [
	('COMPANY', '''(ID INT PRIMARY KEY     NOT NULL,
	       NAME           TEXT    NOT NULL,
	       AGE            INT     NOT NULL,
	       ADDRESS        CHAR(50),
	       SALARY         REAL);'''),
	('SERVICE', '''(ID INT PRIMARY KEY     NOT NULL,
	       NAME           TEXT    NOT NULL,
	       AGE            INT     NOT NULL,
	       ADDRESS        CHAR(50),
	       SALARY         REAL);''')
]


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
		self.dropTables()
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
	a = InitDB(DB_tables, 'server/database/test.db')
	

	




