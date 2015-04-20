#!/usr/bin/python
# -*- coding: utf-8 -*-

print "Content-Type: text/html\n\n"

import cgi,cgitb,Cookie, os
from connection import db, cursor
assignment_id = -1
exam_id = -1
data = cgi.FieldStorage()
assignment_id = data.getvalue('aid')
problem_id = data.getvalue('pid')
exam_id = data.getvalue('eid')

if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)

if c['type'].value == "teacher":
	if int(assignment_id) > 0:
		sql = "SELECT type FROM assignment WHERE assignment_id = {0}".format(assignment_id)
		cursor.execute(sql)
		data = cursor.fetchone()
		if data is not None: 
			ptype = data[0]
		else:
			ptype = ""
			
		if ptype == "MCQ":
			sql="DELETE FROM assignment_mcq WHERE assignment_id = {0} and problem_id = {1}".format(assignment_id, problem_id)
			cursor.execute(sql)
			db.commit()
			print "Removed"
		elif ptype == "code":
			sql = "DELETE FROM assignment_code WHERE assignment_id = {0} and problem_id = {1}".format(assignment_id, problem_id)
			cursor.execute(sql)
			db.commit()
			print "Removed"
		else:
			print "error!"
	else:
		sql = "SELECT type FROM exam WHERE exam_id = {0}".format(exam_id)
		cursor.execute(sql)
		data = cursor.fetchone()
		if data is not None: 
			ptype = data[0]
		else:
			ptype = ""
			
		if ptype == "MCQ":
			sql="DELETE FROM exam_mcq WHERE exam_id = {0} and problem_id = {1}".format(exam_id, problem_id)
			cursor.execute(sql)
			db.commit()
			print "Removed"
		elif ptype == "code":
			sql = "DELETE FROM exam_code WHERE exam_id = {0} and problem_id = {1}".format(exam_id, problem_id)
			cursor.execute(sql)
			db.commit()
			print "Removed"
		else:
			print "error!!"
else:
	print "Error"		
