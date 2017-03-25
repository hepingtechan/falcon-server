# -*- coding: UTF-8 -*-  

import sqlite3

__all__ = ['DBhandle']

class DBhandle:
	def __init__(self, db):
		self.db = db
		try:
			self.conn = sqlite3.connect(db)
			self.cur = self.conn.cursor()
		except sqlite3.Error,e:
			print "database connect  failed:",e
			return       

	def __del__(self):
		if self.conn:
			self.conn.close()

	def disconnect(self):
		if self.conn:
			print 'db disconnect!'
			self.cur.close()

	def select(self,sql):
		try:
			self.cur.execute(sql)
		except sqlite3.Error,e:
			print "database execute sql failed:",e
		return self.cur

	def execute(self,sql):
		try:
			self.cur.execute(sql)
			self.conn.commit()
		except sqlite3.Error,e:
			print "database execute sql failed:",e
			self.conn.rollback() 
		return self.cur




if __name__ == '__main__':
	b = DBhandle('database/test.db')
	#modify
	cur = b.execute("DELETE from COMPANY where ID=2;")
	
	#select
	cu = b.select("select * from company")
	print cu.fetchall()
	# b.disconnect()

