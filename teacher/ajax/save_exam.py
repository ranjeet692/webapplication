#!/usr/bin/python
print "Content-Type: text/html\n\n"
import cgi
import cgitb
import Cookie
import os
import sys
from connection import db, cursor
data = cgi.FieldStorage()
course_id = data.getvalue('cid')
title = data.getvalue('title')
startdate = data.getvalue('start-date-time')
enddate = data.getvalue('end-date-time')
ptype = data.getvalue('type')
exam_id = data.getvalue('eid')
sys.path.insert(0, '/var/www/html/teacher/module/')
import exam

exam_object = exam.Exam()
status = 0
#check whether is teacher type or not.
if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)
	
if c['type'].value == "teacher":
	if int(exam_id) > 0 :
		#update exam data
		status = exam_object.update_exam(exam_id, title, ptype, startdate, enddate)
		print status
	else:
		#new exam_record
		status = exam_object.create_exam(title, ptype, course_id, startdate, enddate)
		print status
		
else:
	print "unauthorised"
	#unauthorised access				
