#!/usr/bin/python

"""
Author:  rockylinux
E-Mail:  Jingzheng.W@gmail.com 
"""
import commands 

#display the users serverhostname 
#return a list containning serverhostname users
class serverhostname:
	def getData(self):
		(status, output) = commands.getstatusoutput('hostname')
		return output.split() 

	def testGetData(self):
		return self.getData()
		
def get_host_name():
	a = serverhostname()    
	return str(a.testGetData())


if __name__ == '__main__':
	print get_host_name()
