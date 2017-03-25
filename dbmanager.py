#-*-coding:UTF-8-*-
#用于操作数据库，对数据库进行增删改查
import sqlite3



#insert方法
def insert(TABLE_NAME,FILE_PATH):
	try:
		conn = sqlite3.connect('database/fidr.db')
		cursor = conn.cursor()
	except Exception,e:
		print "连接失败"
		return

	sql = "INSERT INTO '"+TABLE_NAME+"' (PATH) VALUES('"+FILE_PATH+"')"

	try:
		cursor.execute(sql);
	except sqlite3.Error,e:
		print "添加数据失败"
		return

	conn.commit()
	conn.close()


#delete方法
def delete(TABLE_NAME,FILE_PATH):
	conn = sqlite3.connect('database/fidr.db')
	cursor = conn.cursor()

	sql = "DELETE FROM '"+TABLE_NAME+"' WHERE PATH='"+FILE_PATH+"'"
	try:
		cursor.execute(sql);
	except sqlite3.Error,e:
		print "删除数据失败"
		return

	conn.commit()
	conn.close()


#select方法
def select(TABLE_NAME,FILE_PATH):
	conn = sqlite3.connect('database/fidr.db')
	cursor = conn.cursor()

	sql = "SELECT PATH FROM '"+TABLE_NAME+"' WHERE ID=4"
	try:
		cursor.execute(sql)
		rows = cursor.fetchall()
		
		for r in rows:
			print type(r)
			print r
	except sqlite3.Error,e:
		print "查询数据失败"
		return

	conn.commit()
	conn.close()


#update方法
def update(TABLE_NAME,FILE_PATH):
	conn = sqlite3.connect('database/fidr.db')
	cursor = conn.cursor()

	sql = "UPDATE '"+TABLE_NAME+"' SET PATH ='"+FILE_PATH+"'WHERE ID=0"
	try:
		cursor.execute(sql);
	except sqlite3.Error,e:
		print "修改数据失败"
		return

	conn.commit()
	conn.close()

if __name__ == '__main__':
	TABLE_NAME= 'FDIRMONITOR'

	FILE_PATH='/home/lib/..'

	a = insert(TABLE_NAME,FILE_PATH)
