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
sys.path.insert(0, '/var/www/html/teacher/module/')
import exam

exam_object = exam.Exam()
data = cgi.FieldStorage()
course_id = data.getvalue('cid')
title="Exam Login Code"

if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)

templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )

sql = "SELECT teacher_id FROM courses WHERE course_id = %s"
cursor.execute(sql, (str(course_id)))
data = cursor.fetchone()
if data is not None: 
    teacher_id = data[0]
else:
    teacher_id = ""

if c['type'].value == "teacher" and (c['uid'].value == teacher_id or c['uid'].value == 'vipul@uohyd.ac.in'):
	
	examlist = exam_object.list_exam_login_code(course_id)
	TEMPLATE_FILE = "/var/www/html/teacher/exam_login.html"
	template = templateEnv.get_template( TEMPLATE_FILE )
	templateVars = {"title":title, "cid":course_id,"name":c['name'].value,  "examlist":examlist }
	print template.render( templateVars )
else:
	print "Error"
