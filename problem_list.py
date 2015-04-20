#!/usr/bin/python
# -*- coding: utf-8 -*-

print "Cache-Control:no-store, no-cache, must-revalidate"
print "Content-Type: text/html\n\n"

import cgi, cgitb,os, Cookie
from connection import cursor,db
from cookie import c,load_cookie
from jinja2 import Template, Environment, FileSystemLoader
cgitb.enable();
templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
load_cookie()
if c['type'].value == "student" and c['exam'].value == "true":
	student_id = c["uid"].value
   	form = cgi.FieldStorage()
   	exam_id=form.getvalue('eid')
   	query="select * from problem_code where problem_id in (select problem_id from problem_allotment where exam_id='{0}' and student_id='{1}')".format(str(exam_id),c['uid'].value)
   	cursor.execute(query)
   	data=cursor.fetchall();
	TEMPLATE_FILE = "/var/www/html/problem_list.html" 
	template = templateEnv.get_template( TEMPLATE_FILE )
	templateVars={"name":c["name"].value,"problem":data,"eid":exam_id}	
	print template.render( templateVars )
else:
	print "Time for exam is over"
		
