# -*- coding: UTF-8 -*-  

"""
Author:  Liumei
E-Mail:  liumei@iscas.ac.cn
"""

import time
import asyncore
import socket
import threading
import json
from usermonitor.hostname import *
from usermonitor.getcommandrecord import *
from usermonitor.manage_sensitive_command import *

def get_sys_time(data):
	return time.strftime('%Y-%m-%d %H:%M:%S')

switch = {
	"1001" : get_host_name,
	"1002" : get_sys_time,
	"3001": get_all_user_info,
	"3002": get_one_user_info,
	"3003": offlineTheUser,
	"3004": turnOnSensitiveCommandManagement,
	"3005": turnOffSensitiveCommandManagement
}

def is_json(myjson):  
	try:  
		json.loads(myjson)  
	except ValueError:  
		return False  
	return True

#服务器端数据响应类，接收数据并发回。
class EchoHandler(asyncore.dispatcher_with_send):

	#当socket有可读的数据的时候执行这个方法handle_read
	def handle_read(self):
		data = self.recv(1024)
		if data:
			print "receive from client"
			if is_json(data):
				j_data = json.loads(data)
				print j_data
				try:
					send_msg = switch[str(j_data['msg_id'])](j_data)
				except err:
					print send_msg
				self.send(send_msg)
			else:
				print data
						

			'''
			#test for json
			send_msg = {'msg_id' : 2002,
						'msg_data':[
						{'user-name' : 'Yetis','ip' : '192.168.160.1'},
						{'user-name' : 'Yetis','ip' : '192.168.160.2'}
						]
						}
			j_send_msg = json.dumps(send_msg)
			self.send(j_send_msg)
			'''



#响应服务器端程序，负责监听一个端口，并响应客户端发送的消息然后原样返回给客户端。
#
#asyncore.dispatcher类:一个底层套接字对象的简单封装。这个类有少数由异步循环调用的，用来事件处理的函数。
class EchoServer(asyncore.dispatcher):  

	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)		
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)

	#其中handle_accept()方法定义当一个连接到来的时候要执行的操作，这里指定了使用一个Handler来出来发送来的数据。
	def handle_accept(self):
		conn, addr = self.accept()
		print 'Incoming connection from %s' % repr(addr)
		self.handler = EchoHandler(conn)


class EchoServerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		server = EchoServer('localhost', 9999)
		asyncore.loop()  #asyncore.loop(…) - 用于循环监听网络事件,loop()函数负责检测一个字典，字典中保存dispatcher的实例。



#开始运行
EchoServerThread().start()
# time.sleep(2)
