# -*- coding: UTF-8 -*-  

import os
import time
import logging
from threading import *
from Queue import Queue, Empty

from  inotify import  WatchManager, Notifier, ThreadedNotifier,\
ProcessEvent,IN_DELETE, IN_CREATE,IN_MODIFY


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s [%(message)s]',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='a+')



class EventHandler(ProcessEvent):
	"""事件处理"""
	def process_IN_CREATE(self, event):
		print   "Create file: %s "  %   os.path.join(event.path,event.name)
		logging.info("Create file: %s " %os.path.join(event.path,event.name))
 
	def process_IN_DELETE(self, event):
		print   "Delete file: %s "  %   os.path.join(event.path,event.name)
		logging.info("Delete file: %s " %os.path.join(event.path,event.name))
 
	def process_IN_MODIFY(self, event):
		print   "Modify file: %s "  %   os.path.join(event.path,event.name)
		logging.info("Modify file: %s "  %   os.path.join(event.path,event.name))


class Event:
	"""事件对象"""
	def __init__(self, type_=None):
		self.type_ = type_      # 事件类型
		self.dict = {}          # 字典用于保存具体的事件数据


class FileMonitor():
	"""file event monitor"""

	def __init__(self):
		self.__wm = WatchManager()
		self.__notifier = ThreadedNotifier(self.__wm, EventHandler())
		## 事件对象列表
		self.__eventQueue = Queue()
		## 开关
		self.__active = False
		self.__thread = Thread(target = self.fileLoop)
		##对应的事件的响应函数
		self.__handlers = {}

		##添加msg_id对应的回调函数
		self.addEventCallback(1001, self.callback_addPath)
		self.addEventCallback(2001, self.callback_rmPath)

	#监听器的处理函数 
	def callback_addPath(self, event):
		logging.info("callback_add_path") 

		path = event.dict["path"]
		mask = event.dict["mask"]
		if os.path.exists(path) == False:
			print "path is not exist!"
			return -1	
		self.__wm.add_watch(path, mask, rec=True)

		logging.info("add  file: %s " %event.dict["path"])

	def callback_rmPath(self, event):
		logging.info("callback_rm_path")

		path = event.dict["path"]
		wd = self.__wm.get_wd(path)
		if wd == None:
			return
		self.__wm.rm_watch(wd)

		
	def eventProcess(self, event):
		"""处理事件"""
		# 检查是否存在对该事件进行监听的处理函数
		if event.type_ in self.__handlers:
		# 若存在，则按顺序将事件传递给处理函数执行
			for handler in self.__handlers[event.type_]:
				handler(event)

	def addEventCallback(self, type_, handler):
		"""绑定事件和监听器处理函数"""
		# 尝试获取该事件类型对应的处理函数列表，若无则创建
		try:
			handlerList = self.__handlers[type_]
		except KeyError:
			handlerList = []

		self.__handlers[type_] = handlerList
		# 若要注册的处理器不在该事件的处理器列表中，则注册该事件
		if handler not in handlerList:
			handlerList.append(handler)


	def removeEventListener(self, type_, handler):
		"""移除监听器的处理函数"""


	def sendEvent(self, event):
		"""发送事件，向事件队列中存入事件"""
		self.__eventQueue.put(event)

	def receiveMsg(self, data):
		logging.info("add path receive data: %s type:%s" %(data, type(data)))
		#事件对象
		event = Event(type_ = data["msg_id"])
		event.dict = data["msg_data"]
		#发送事件
		self.sendEvent(event)
		print u'add_path\n'
		return 'yes'


	def fileLoop(self):
		while self.__active == True:
			try:
				event = self.__eventQueue.get(block = False, timeout = 1)
				self.eventProcess(event)
			except Empty:
				pass
			
			try:
				self.__notifier.process_events()
				#当 超时时间 未设置，则select会一直阻塞，直到监听的描述符发生变化
   				#当 超时时间 ＝ 1时，那么如果监听的句柄均无任何变化，则select会阻塞 1 秒，之后返回三个空列表，
   				#如果监听的描述符（fd）有变化，则直接执行。
				if self.__notifier.check_events(timeout=2): 
					self.__notifier.read_events()
			except KeyboardInterrupt:
				self.__notifier.stop()
			 	break
		

	def start(self):
		"""启动"""
		print 'file monitor start'
		# 将事件管理器设为启动
		self.__active = True
		# 启动事件处理线程
		self.__thread.start()

	def stop(self):
		"""停止"""
		# 将事件管理器设为停止
		self.__active = False
		# 等待事件处理线程退出
		self.__thread.join()



if __name__ == "__main__":
	# path = "/home/mei/0103-T-BJ-6A/server/fileprotection/test/"
	mask = IN_DELETE | IN_CREATE |IN_MODIFY

	monitor = FileMonitor()
	monitor.start()

	logging.info("mask: %d" %mask)

	#test
	data = {u'msg_id': 1001, u'msg_data': {u'path': u'/home/mei/0103-T-BJ-6A/server/fileprotection/test/', u'mask': mask}}
	monitor.receiveMsg(data)

	data = {u'msg_id': 1001, u'msg_data': {u'path': u'/home/mei/0103-T-BJ-6A/server/fileprotection/test1/', u'mask': mask}}
	monitor.receiveMsg(data)

	data = {u'msg_id': 2001, u'msg_data': {u'path': u'/home/mei/0103-T-BJ-6A/server/fileprotection/test1/', u'mask': mask}}
	monitor.receiveMsg(data)


