#!/usr/bin/python
# -*- coding: utf-8 -*-

print "Cache-Control:no-store, no-cache, must-revalidate"
print "Content-Type: text/html\n\n"

import cgi, cgitb,os, Cookie
from connection import cursor,db
from cookie import c,load_cookie
from jinja2 import Template, Environment, FileSystemLoader
cgitb.enable()
templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
load_cookie()
resp=""
if c['type'].value == "student":
	student_id = c["uid"].value
   	form = cgi.FieldStorage()
   	course_id = form.getvalue('course_id')
   	query="select * from exam where course_id='{0}'".format(str(course_id))
   	cursor.execute(query)
   	data=cursor.fetchall();
   	for row in data:
   		resp=resp+'''<h5>'''+str(row[1])+'''</h5>
   		<div class="input-group">
                              <input type="text" class="form-control" id ="'''+str(row[0])+'''" placeholder="Enter the Exam Key ...">
                              <span class="input-group-btn">
                                <button class="btn btn-default" class="login" onclick="abc('''+str(row[0])+''')" id="'''+str(row[0])+'''" type="button">Login!</button>
                              </span>
                            </div>'''
   	print resp	
