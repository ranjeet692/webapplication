#!/usr/bin/python
# -*- coding: utf-8 -*-
#Description: List all exam and its details of a specific course
#Query String Variables: cid(course_id)
#Operation: Create New Option, Modify Previously Created Exams
#Created: April 18, 2015
#Last Modified: April 18, 2015
#Author: Optimus Prime


print "Content-Type: text/html\n\n"

from jinja2 import Template, Environment, FileSystemLoader
import cgi
import cgitb
import Cookie
import os
import datetime
from connection import db, cursor
import footer
import sys
sys.path.insert(0, '/var/www/html/teacher/module/')
import exam



data = cgi.FieldStorage()
course_id = data.getvalue('cid')
title="Exam"

if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)

templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )

sql = "SELECT teacher_id FROM courses WHERE course_id = %s"
cursor.execute(sql, (course_id))
data = cursor.fetchone()
if data is not None: 
    teacher_id = data[0]
else:
    teacher_id = ""
    
if c['type'].value == "teacher" and (c['uid'].value == teacher_id or c['uid'].value == 'vipul@uohyd.ac.in'):
	sql = "SELECT exam_id, title, startdate, enddate, course_id, type FROM exam WHERE course_id = '{0}' ORDER BY startdate DESC".format(str(course_id))
	cursor.execute(sql)
	examlist = cursor.fetchall()
	i = 0
	assign = []  # list
	now = datetime.datetime.now() #cuurent date time
	for row in examlist:
		if row[5] == "code":
			sql = "SELECT count(*) FROM exam_code WHERE exam_id = '{0}'".format(str(row[0]))
			cursor.execute(sql)
			count = cursor.fetchall() #count variable contains number of problems in an assignment from table assignment_code
			if(row[3] > now):         #if assignment enddate is greater than today's date then enable edit button.
				d = ""
				color = "info"
			else:
				d = "disabled"	
				color = ""
			row = row + (count[0][0],i+1,d,color,)     #adding 3 element in currunt tuple i.e. number of problems, serial no, button disable option
			#assign = assign + (row)
			assign.append(row)    #append each tuple(single row of a table to a list which'll later convert to multidimensional tuple)
		else:	
			sql = "SELECT count(*) FROM exam_mcq WHERE exam_id = '{0}'".format(str(row[0]))
			cursor.execute(sql)
			count = cursor.fetchall()
			if(row[3] > now):
				d = ""
				color = "info"
			else:
				d = "disabled"	
				color = ""
			row = row + (count[0][0],i+1,d,color,)
			#assign = assign + (row)
			assign.append(row)
		i = i + 1	
	assign = tuple(assign)		# converting list to tuple
	#tuple stucture(assignment_id, title, startdate, enddate, course_id, type, problem_count, serial_no, disable option)
	#print assign
	TEMPLATE_FILE = "/var/www/html/teacher/exam.html"
	template = templateEnv.get_template( TEMPLATE_FILE )
	templateVars = {"title":title, "cid":course_id,"name":c['name'].value,  "alist":assign }
	print template.render( templateVars )
else:
	TEMPLATE_FILE = "/var/www/html/redirect.html"
	template = templateEnv.get_template( TEMPLATE_FILE )
	print template.render()	
