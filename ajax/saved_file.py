#!/usr/bin/python
print "Content-Type: text/html\n\n"
#creation date : 22/03/2015
import cgi, os,Cookie
import cgitb; cgitb.enable()
from connection import cursor, db

if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)
	
form = cgi.FieldStorage()
assignment_id = form.getvalue('aid')
problem_id = form.getvalue('pid')
op = form.getvalue('operation')
filename = ''

sql = "SELECT file_name,language FROM save_code WHERE student_id = '{0}' and assignment_id= {1} and problem_id= {2}".format(c['uid'].value, assignment_id, problem_id)
cursor.execute(sql)
if(cursor.rowcount > 0):
	data = cursor.fetchall()
	filename = data[0][0]
if(filename != ''):
	if (op == 'code'):	
		contents = open("/home/ubuntu/submission/"+ c['uid'].value + "/" + assignment_id + "/" + str(filename)).read()	
		print contents
	elif(op == 'file'):
		print filename
else:
    print "no file"	
