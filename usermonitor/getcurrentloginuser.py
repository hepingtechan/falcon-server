#!/usr/bin/python


import sys
sys.path.append("./server")
import sql


def get_current_login_user():
	b = sql.DBhandle('./server/database/user-monitor.db')
	cu = b.select("select user_id, user_name, login_time, login_ip, login_method from current_login_user")
	res =  cu.fetchall()
	res_msg = {}

	if len(res) > 0:
		res_msg["current_login_user_num"] = len(res)
		login_user_info = []

		for one in res:
			login_user_info.append(one)
		res_msg["user_info"] = login_user_info		
	else:
		res_msg["current_login_user_num"] = 0

	print res_msg
	return res_msg

if __name__ == '__main__':
	get_current_login_user()



