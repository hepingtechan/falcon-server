#!/usr/bin/python


import os
import sql
DB_PATH = 'server/database/user-monitor.db'

#TEST
# import sys
# sys.path.append("..")
# import sql
# DB_PATH = '../database/user-monitor.db'


import json
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s [%(message)s]',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='userinfo.log',
                filemode='a+')



def get_command_record(user_name, db_handle):
	cu = db_handle.select("select command_name, user_name, operation_time from command_operation_record where user_name='%s'"%user_name)
	res =  cu.fetchall()
	res_msg = {}

	if len(res) > 0:
		res_msg["commandrecord_num"] = len(res)
		command_record = []

		for one in res:
			# command_record.append(one)
			one_record =  {}
			one_record["command"] = one[0]
			one_record["time"] = one[2]
			command_record.append(one_record)
		res_msg["command_record"] = command_record		
	else:
		res_msg["commandrecord_num"] = 0
	return res_msg


#3001
def get_all_user_info(data):
	b = sql.DBhandle(DB_PATH)
	cu = b.select("select  user_id, user_name, login_ip, tty_number  from current_login_user ")
	res =  cu.fetchall()
	res_msg = {}
	logging.info("user_id:%s"%str(res))

	if len(res) > 0:
		res_msg["user_num"] = len(res)
		one_record = []

		for one in res:
			one_user = {}
			one_user["userid"] = one[0]
			one_user["name"] = one[1]
			one_user["ip"] = one[2]
			one_user["tty"] = one[3]
			one_record.append(one_user)
		res_msg["userdata"] = one_record		
	else:
		res_msg["user_num"] = 0

	return_msg = json.dumps(res_msg)
	print type(return_msg)
	return return_msg


def get_user_score(user_name ,db_handle):	

	cu = db_handle.select("select  user_name, security_score from user  where user_name='%s'"%user_name)
	res =  cu.fetchall()

	if len(res) > 0:
		print res[0][1]
		return res[0][1]
	else:
		return 0

#3002
def get_one_user_info(data):
	user_id = data["msg_data"]["user_id"]
	logging.info("user_id:%s"%user_id)

	b = sql.DBhandle(DB_PATH)
	cu = b.select("select user_id, user_name, login_time, login_ip, login_method, tty_number from current_login_user where user_id='%s'" % str(user_id))
	res =  cu.fetchall()
	logging.info("sql_res:%s"%str(res))
	res_msg = {}

	if len(res) > 0:	
		one_user = {}
		one = res[0]
		one_user["name"] = one[1]
		one_user["logintime"] = one[2]
		one_user["ip"] = one[3]
		one_user["loginmethod"] = one[4]
		one_user["tty"] = one[5]

		res_msg["userdata"] = one_user

		#get user scrore
		res_msg["score"] = get_user_score(one_user["name"], b)

		#get operation record
		res_msg["record"] = get_command_record(one_user["name"], b)
		logging.info("res_msg2:%s"%str(res_msg))
	else:
		res_msg["user_num"] = 0

	return_msg = json.dumps(res_msg)
	print type(return_msg)
	return return_msg


#3003
def offlineTheUser(data):
	ttyNumber = data["msg_data"]["tty"]
	# pid = os.popen('ps -ef | grep %s' % ttyNumber).readlines()[0].split()[1]
	# print 'pid: %s' % pid
	os.popen('pkill -kill -t %s' % ttyNumber)
	return '{"return_nu":"ok"}'


if __name__ == '__main__':
	user_name = 'mei'
	# get_command_record(user_name)

	# print get_all_user_info("ada")

	# msg={"msg_id":3002,"msg_data":{"user_id":1}}
	# print get_one_user_info(msg)


	msg = {"msg_id":3003,"msg_data":{"tty":"pts/1"}};
	offlineTheUser(msg)



