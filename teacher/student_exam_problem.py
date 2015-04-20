#!/usr/bin/python
# -*- coding: utf-8 -*-

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

data = cgi.FieldStorage()
course_id = data.getvalue('cid')
title="Problem Allocation"

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
	#sql = "select a.rno, a.email_id, a.name, a.contact from student as a, enrolled as b where b.email = a.email_id and b.course_id = {0} and a.rno like '14%' ORDER BY a.rno".format(course_id)
	#student list reg no and email_id
	sql = "SELECT a.rno, a.email_id from student as a, enrolled as b where a.email_id = b.email and b.course_id = {0}".format(course_id)
	cursor.execute(sql)
	data = cursor.fetchall()
	regno_email_map = {x:y for x,y in data}
	slist = data
	#problem_id and name mapping
	sql = "select a.problem_id, a.title from problem_code as a, exam_code as b where a.problem_id = b.problem_id"
	cursor.execute(sql)
	data = cursor.fetchall()
	problem_name_map = {y:x for x, y in data}
	
	#exam_title_map
	sql = "select exam_id, title from exam"
	cursor.execute(sql)
	data = cursor.fetchall()
	exam_name_map = {y:x for x, y in data}
	
	sql = "select a.exam_id, a.title, b.problem_id, b.title from exam as a, problem_code as b, exam_code as c where a.exam_id = c.exam_id and b.problem_id = c.problem_id and a.course_id = {0}".format(course_id)
	cursor.execute(sql)
	data = cursor.fetchall()
	
	eplist = list(data)
	TEMPLATE_FILE = "/var/www/html/teacher/student_exam_problem.html"
	template = templateEnv.get_template( TEMPLATE_FILE )
	templateVars = {"title":title, "cid":course_id,"name":c['name'].value, "eplist":eplist,"cid":course_id, "slist": slist}
	print template.render( templateVars )
else:
	TEMPLATE_FILE = "/var/www/html/redirect.html"
	template = templateEnv.get_template( TEMPLATE_FILE )
	print template.render()	
