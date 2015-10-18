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
exam_id = form.getvalue('eid')
op = form.getvalue('operation')
ppid = form.getvalue('ppid')
filename = ''

sql = "SELECT file_name,language FROM save_code WHERE student_id = '{0}' and assignment_id= {1} and problem_id= {2} and ppid = {3} and exam_id='{4}'".format(c['uid'].value, assignment_id, problem_id, ppid,exam_id)
cursor.execute(sql)
if(cursor.rowcount > 0):
	data = cursor.fetchall()
	filename = data[0][0]
if(filename != ''):
	if (op == 'code'):	
		if(int(exam_id) != -1):
			contents = open("/home/ubuntu/submission/"+ c['uid'].value + "/" +"e"+ exam_id  + "/" + str(filename)).read()	
		elif(int(assignment_id) != -1 and int(problem_id) != -1):
			contents = open("/home/ubuntu/submission/"+ c['uid'].value + "/" +assignment_id + "/" + str(filename)).read()
		else:
			contents = open("/home/ubuntu/submission/"+ c['uid'].value + "/p_problem/" + str(filename)).read()	
		print contents
	elif(op == 'file'):
		print filename
else:
    print 'no file'	
