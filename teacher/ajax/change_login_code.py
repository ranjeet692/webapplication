#!/usr/bin/python
# -*- coding: utf-8 -*-

print "Content-Type: text/html\n\n"

import cgi
import cgitb
import Cookie
import os
from connection import db, cursor
import sys
sys.path.insert(0, '/var/www/html/teacher/module/')
import exam

exam_object = exam.Exam()

exam_id = -1
data = cgi.FieldStorage()
exam_id = data.getvalue('eid')

if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)

if c['type'].value == "teacher":
	print exam_object.change_exam_code(exam_id)
else:
	print "Error"	
